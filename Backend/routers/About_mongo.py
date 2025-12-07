import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from client_mongo import get_db
from dataBase.modelAbout_mongo import About
from dataBase.schemaAbout_mongo import AboutSchema
from config import URLBACK
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB_mongo import UserInDb

router = APIRouter()

# Construct an absolute path to the 'uploads' directory
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.put("/about/", response_model=AboutSchema)
async def update_about(
    historia: Optional[str] = Form(None),
    mision: Optional[str] = Form(None),
    vision: Optional[str] = Form(None),
    presencia: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    imagen2: Optional[UploadFile] = File(None),
    imagen3: Optional[UploadFile] = File(None),
    anio: Optional[str] = Form(None),
    anio2: Optional[str] = Form(None),
    db=Depends(get_db),
    current_user: UserInDb = Depends(get_current_user)
):
    # En MongoDB, no es necesario "obtener y luego actualizar".
    # Podemos construir un objeto de actualización y usar find_one_and_update.
    
    update_data = {}
    if historia is not None:
        update_data["historia"] = historia
    if mision is not None:
        update_data["mision"] = mision
    if vision is not None:
        update_data["vision"] = vision
    if presencia is not None:
        update_data["presencia"] = presencia

    # La lógica para subir imágenes permanece igual
    if imagen is not None:
        file_location = os.path.join(UPLOAD_DIR, imagen.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen.file.read())
        update_data["imagen"] = f"{URLBACK}/uploads/{imagen.filename}"
    if imagen2 is not None:
        file_location = os.path.join(UPLOAD_DIR, imagen2.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen2.file.read())
        update_data["imagen2"] = f"{URLBACK}/uploads/{imagen2.filename}"
    if imagen3 is not None:
        file_location = os.path.join(UPLOAD_DIR, imagen3.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen3.file.read())
        update_data["imagen3"] = f"{URLBACK}/uploads/{imagen3.filename}"

    if anio is not None:
        update_data["anio"] = anio
    if anio2 is not None:
        update_data["anio2"] = anio2

    # Siempre actualizamos el autor
    update_data["autor_id"] = current_user.id

    # Usamos find_one_and_update para actualizar el documento.
    # El filtro {} encontrará el único documento (asumiendo que solo hay uno).
    # El operador $set actualiza solo los campos proporcionados.
    # `upsert=True` creará el documento si no existe.
    # `return_document=True` devuelve el documento actualizado.
    updated_about = await db["about"].find_one_and_update(
        {},
        {"$set": update_data},
        upsert=True,
        return_document=True
    )

    if not updated_about:
        raise HTTPException(status_code=500, detail="No se pudo actualizar la información de 'Sobre Nosotros'")

    return updated_about

@router.get("/about/", response_model=AboutSchema)
async def get_about(db=Depends(get_db)):
    about = await db["about"].find_one({})
    if not about:
        raise HTTPException(status_code=404, detail="No hay información de 'Sobre Nosotros'")
    return about
