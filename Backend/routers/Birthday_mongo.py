import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional, List
from client_mongo import get_db
from dataBase.modelBirthday_mongo import Birthday
from dataBase.schemaBirthday_mongo import BirthdaySchema
from config import URLBACK

router = APIRouter()

# Construct an absolute path to the 'uploads' directory
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/birthday/", response_model=BirthdaySchema)
async def crear_cumpleanos(
    descripcion: Optional[str] = Form(None, max_length=500),
    contenido: Optional[UploadFile] = File(None),
    db=Depends(get_db)
):
    # Obtener el último cumpleaños para replicar campos si no se proporcionan
    ultimo = await db["birthday"].find_one({}, sort=[("_id", -1)])

    url_contenido = None
    if contenido:
        file_location = os.path.join(UPLOAD_DIR, contenido.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(contenido.file.read())
        url_contenido = f"{URLBACK}/uploads/{contenido.filename}"
    elif ultimo:
        url_contenido = ultimo.get("contenido")

    if descripcion is None and ultimo:
        descripcion = ultimo.get("descripcion")

    # Crear el nuevo documento como un diccionario
    nuevo_cumpleanos = Birthday(
        descripcion=descripcion,
        contenido=url_contenido
    )
    
    # Insertar en la base de datos
    result = await db["birthday"].insert_one(nuevo_cumpleanos.dict(by_alias=True))
    
    # Obtener el documento insertado para devolverlo
    created_cumpleanos = await db["birthday"].find_one({"_id": result.inserted_id})
    
    return created_cumpleanos

@router.get("/birthday/", response_model=List[BirthdaySchema])
async def obtener_cumpleanos(db=Depends(get_db)):
    cumpleanos_cursor = db["birthday"].find({}).sort("_id", -1)
    return await cumpleanos_cursor.to_list(length=None) # Obtener todos
