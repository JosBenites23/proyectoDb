import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional, List
from bson import ObjectId
from client_mongo import get_db
from dataBase.modelCompany_mongo import Company
from dataBase.schemaCompany_mongo import CoSchema
from config import URLBACK
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB_mongo import UserInDb

router = APIRouter()

# Construct an absolute path to the 'uploads' directory, which is ../uploads from this file's perspective
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/company/", response_model=CoSchema)
async def crear_Empresa(
    contenido: Optional[str] = Form(..., max_length=10000),
    imagen: UploadFile = File(...),
    db=Depends(get_db),
    current_user: UserInDb = Depends(get_current_user)
):
    file_location = os.path.join(UPLOAD_DIR, imagen.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(imagen.file.read())

    url_contenido = contenido if contenido else f"{URLBACK}/uploads/{imagen.filename}"
    url_imagen = f"{URLBACK}/uploads/{imagen.filename}"

    nueva_Empresa = Company(
        contenido=url_contenido,
        imagen=url_imagen,
        autor_id=current_user.id
    )

    result = await db["company"].insert_one(nueva_Empresa.dict(by_alias=True))
    created_empresa = await db["company"].find_one({"_id": result.inserted_id})
    return created_empresa

@router.get("/company/", response_model=List[CoSchema])
async def obtener_Co(db=Depends(get_db)):
    empresas_cursor = db["company"].find({}).sort("_id", -1)
    return await empresas_cursor.to_list(length=None)

@router.delete("/eliminar-empresa/{id}", response_model=CoSchema)
async def eliminar_Co(id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de empresa no válido")
    
    object_id = ObjectId(id)

    db_co = await db["company"].find_one_and_delete({"_id": object_id})
    
    if db_co is None:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    
    return db_co
