import os
import traceback
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional, List
from slugify import slugify
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from client_mongo import get_db, get_client
from config import PUBLIC_BACKEND_URL, MONGO_DATABASE_URL
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB_mongo import UserInDb
from dataBase.modelDep_mongo import Dep, Link
# Importamos desde el nuevo schema
from dataBase.schemaDep_mongo import DepartamentoSchema, DepartamentoCard, LinkSchemaDep
router = APIRouter(prefix="/departamento", tags=["Departamentos"])

# Construct an absolute path to the 'uploads' directory
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Endpoint de creación con transacción
@router.post("/", response_model=DepartamentoSchema)
async def crear_departamento(
    titulo: str = Form(..., max_length=500),
    descripcion: str = Form(..., max_length=500),
    imagen: UploadFile = File(...),
    titulo_link: Optional[str] = Form(None),
    link_file: Optional[UploadFile] = File(None),
    link_url: Optional[str] = Form(None),
    db=Depends(get_db),
    client: AsyncIOMotorClient = Depends(get_client),
    current_user: UserInDb = Depends(get_current_user)
):
    if await db["dep"].find_one({"titulo": titulo}):
        raise HTTPException(status_code=400, detail="Ya existe un departamento con ese nombre.")

    file_location = os.path.join(UPLOAD_DIR, imagen.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(imagen.file.read())
    url_contenido_dep = f"{PUBLIC_BACKEND_URL}/uploads/{imagen.filename}"
    
    dep_slug = slugify(titulo)

    try:
        # We will build the response object from the data we already have,
        # instead of re-fetching, to avoid read-after-write consistency issues.
        dep_creado_dict = {}

        async with await client.start_session() as session:
            async with session.start_transaction():
                nuevo_dep = Dep(
                    titulo=titulo,
                    descripcion=descripcion,
                    imagen=url_contenido_dep,
                    slug=dep_slug,
                    autor_id=current_user.id
                )
                # The Pydantic model already created the ObjectId, we can grab it.
                new_dep_id = nuevo_dep.id
                dep_creado_dict = nuevo_dep.dict(by_alias=True)

                await db["dep"].insert_one(dep_creado_dict, session=session)

                if titulo_link and (link_file or link_url):
                    url_del_link = ""
                    if link_file:
                        link_file_location = os.path.join(UPLOAD_DIR, link_file.filename)
                        with open(file_location, "wb+") as file_object:
                            file_object.write(link_file.file.read())
                        url_del_link = f"{PUBLIC_BACKEND_URL}/uploads/{link_file.filename}"
                    elif link_url:
                        url_del_link = link_url
                    
                    nuevo_link = Link(
                        titulo_link=titulo_link,
                        url=url_del_link,
                        dep_id=new_dep_id
                    )
                    await db["linkdep"].insert_one(nuevo_link.dict(by_alias=True), session=session)
        
        # Now, fetch only the links associated with the new department
        links_creados_cursor = db["linkdep"].find({"dep_id": new_dep_id})
        # Manually build the final object to return, ensuring it matches the schema
        dep_creado_dict["links"] = await links_creados_cursor.to_list(length=None) if links_creados_cursor else []
        
        return dep_creado_dict

    except Exception as e:
        print("--- ERROR EN `crear_departamento` ---")
        traceback.print_exc()
        print("---------------------------------------")
        raise HTTPException(status_code=500, detail=f"No se pudo crear el departamento: {str(e)}")

# Endpoint para obtener las "cards"
@router.get("/cards")
async def obtener_departamentos_cards(db=Depends(get_db)):
    lista_departamentos = []
    cursor = db["dep"].find({}).sort("fecha_creacion", -1)
    async for dep in cursor:
        lista_departamentos.append({
            "id": str(dep["_id"]),  # Convertimos manualmente el _id a un string "id"
            "titulo": dep.get("titulo"),
            "slug": dep.get("slug"),
            "imagen": dep.get("imagen"),
            "descripcion": dep.get("descripcion"),
            "fecha_creacion": dep.get("fecha_creacion")
        })
    return lista_departamentos

# Endpoint para obtener un departamento por ID (para edición)
@router.get("/id/{id}") # Removed response_model=DepartamentoSchema
async def obtener_departamento_por_id(id: str, db=Depends(get_db)):
    # HACK: Prioritizing string ID search for presentation data consistency
    departamento = await db["dep"].find_one({"_id": id})
    
    # If not found by string, try with ObjectId for potentially valid future data
    if not departamento and ObjectId.is_valid(id):
        departamento = await db["dep"].find_one({"_id": ObjectId(id)})

    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    
    # Manually get links
    links_cursor = db["linkdep"].find({"dep_id": departamento["_id"]})
    departamento_links = await links_cursor.to_list(length=None) if links_cursor else []

    # Manually ensure the _id is converted to 'id' string for the frontend
    # and add links to the department dictionary
    departamento["id"] = str(departamento["_id"])
    departamento["links"] = departamento_links
    
    return departamento

# Endpoint para obtener una página de departamento por slug
@router.get("/page-dep/{slug}", response_model=DepartamentoSchema)
async def obtener_departamento_por_slug(slug: str, db=Depends(get_db)):
    departamento = await db["dep"].find_one({"slug": slug})
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    
    links_creados_cursor = db["linkdep"].find({"dep_id": departamento["_id"]})
    departamento["links"] = await links_creados_cursor.to_list(length=None) if links_creados_cursor else []
    
    return departamento

from fastapi import Path # ADDED IMPORT

# Endpoint para actualizar un departamento
@router.put("/editar-dep/{id}/", response_model=DepartamentoSchema)
async def actualizar_departamento(
    id: str = Path(...), # ID from the URL path
    descripcion: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    db=Depends(get_db)
):
    # Hack: Find department by string ID first, then by ObjectId if needed
    departamento_db = await db["dep"].find_one({"_id": id})
    if not departamento_db and ObjectId.is_valid(id):
        departamento_db = await db["dep"].find_one({"_id": ObjectId(id)})
    
    if not departamento_db:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    update_data = {}
    if descripcion is not None:
        update_data["descripcion"] = descripcion
    
    if imagen:
        # Save new image and update its URL
        file_location = os.path.join(UPLOAD_DIR, imagen.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen.file.read())
        update_data["imagen"] = f"{PUBLIC_BACKEND_URL}/uploads/{imagen.filename}"
    
    # Update the document in MongoDB if there is data to update
    if update_data:
        updated_departamento = await db["dep"].find_one_and_update(
            {"_id": departamento_db["_id"]}, # Query by the _id found earlier
            {"$set": update_data},
            return_document=True # Return the updated document
        )
    else:
        updated_departamento = departamento_db # No changes, return the original

    if not updated_departamento:
        raise HTTPException(status_code=500, detail="No se pudo actualizar el departamento")

    # Manually attach links and ensure 'id' is a string for the response
    links_cursor = db["linkdep"].find({"dep_id": updated_departamento["_id"]})
    updated_departamento["links"] = await links_cursor.to_list(length=None) if links_cursor else []
    updated_departamento["id"] = str(updated_departamento["_id"])

    return updated_departamento

# Endpoint para eliminar un departamento
@router.delete("/eliminar-dep/{id}", response_model=DepartamentoSchema)
async def eliminar_departamento(id: str, db=Depends(get_db)):
    print(f"--- INTENTO DE ELIMINACIÓN RECIBIDO (TEMPORAL HACK) ---")
    print(f"ID recibido del frontend: '{id}' (longitud: {len(id)})")
    
    
    print(f"Conectado a la base de datos: {db.name}")
    print(f"Usando URL de DB: {MONGO_DATABASE_URL}")

    print("Buscando documento con `_id` como string directamente...")
    # Buscamos directamente por el string 'id' que recibimos
    departamento = await db["dep"].find_one({"_id": id}) 

    if not departamento:
        print("`find_one` no encontró el documento. Intentando búsqueda manual...")
        all_deps = await db["dep"].find({}).to_list(length=None)
        print(f"Total de documentos en la colección 'dep': {len(all_deps)}")
        found_manually = False
        for doc in all_deps:
            # Comparamos el _id de la DB (que es string) con el string 'id' recibido
            print(f"  Comparando con _id: {doc['_id']} (Tipo: {type(doc['_id'])})")
            if doc['_id'] == id: # Comparación como strings
                found_manually = True
                departamento = doc
                print(f"¡ENCONTRADO MANUALMENTE! El documento con _id {id} SÍ existe.")
                break
        if not found_manually:
             print("Búsqueda manual tampoco encontró el documento.")
             raise HTTPException(status_code=404, detail="Departamento no encontrado (verificado manualmente)")

    print("Documento encontrado. Procediendo a eliminar...")
    # Eliminar en cascada
    await db["linkdep"].delete_many({"dep_id": id}) # Buscamos por string
    await db["dep"].delete_one({"_id": id}) # Buscamos por string
    
    print(f"Documento con id {id} eliminado con éxito.")
    return departamento

# Endpoint para agregar un link a un departamento
@router.post("/{depId}/agregar-link", response_model=LinkSchemaDep)
async def agregar_link_a_departamento(
    depId: str = Path(...), # Department ID from URL
    titulo_link: str = Form(...),
    link_file: Optional[UploadFile] = File(None),
    link_url: Optional[str] = Form(None),
    db=Depends(get_db)
):
    # First, ensure the department exists (using hack for string ID)
    departamento = await db["dep"].find_one({"_id": depId})
    if not departamento and ObjectId.is_valid(depId):
        departamento = await db["dep"].find_one({"_id": ObjectId(depId)})
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    if not link_file and not link_url:
        raise HTTPException(status_code=400, detail="Debe proporcionar un archivo o una URL para el link.")

    url_del_link = ""
    if link_file:
        file_location = os.path.join(UPLOAD_DIR, link_file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(link_file.file.read())
        url_del_link = f"{PUBLIC_BACKEND_URL}/uploads/{link_file.filename}"
    elif link_url:
        url_del_link = link_url
    
    nuevo_link = Link(
        titulo_link=titulo_link,
        url=url_del_link,
        dep_id=depId # Use the department ID as string
    )
    link_dict = nuevo_link.dict(by_alias=True)
    result = await db["linkdep"].insert_one(link_dict)
    
    link_dict["id"] = str(result.inserted_id) # Ensure 'id' is in response
    return link_dict

# Endpoint para eliminar un link de un departamento
@router.delete("/link/{linkId}", response_model=LinkSchemaDep)
async def eliminar_link_de_departamento(linkId: str, db=Depends(get_db)):
    # Hack: Find link by string ID first, then by ObjectId if needed
    link_db = await db["linkdep"].find_one({"_id": linkId})
    if not link_db and ObjectId.is_valid(linkId):
        link_db = await db["linkdep"].find_one({"_id": ObjectId(linkId)})
    
    if not link_db:
        raise HTTPException(status_code=404, detail="Link no encontrado")
    
    # Delete the document
    deleted_link = await db["linkdep"].find_one_and_delete({"_id": link_db["_id"]})

    if not deleted_link:
        raise HTTPException(status_code=500, detail="No se pudo eliminar el link")
    
    deleted_link["id"] = str(deleted_link["_id"])
    return deleted_link