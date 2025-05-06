from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from client import get_db
from dataBase.modelNews import Noticia
from dataBase.schemaNews import NewsSchema
from fastapi import UploadFile, File, Form

router = APIRouter()

@router.post("/subir-noticia", response_model=NewsSchema)
async def crear_noticia(
    titulo: str = Form(..., max_length=600),
    descripcion: str = Form(..., max_length=100000),
    tipo_contenido: str = Form(...),
    contenido: UploadFile = File(...),
    db: Session = Depends(get_db)):
    

    upload_dir = "uploads"
    file_location = f"{upload_dir}/{contenido.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(contenido.file.read())

    url_contenido = f"http://9.0.1.247:8081/uploads/{contenido.filename}"
 
    db_noticia = Noticia(
        #id=noticia.id,
        titulo=titulo,
        descripcion=descripcion,
        tipo_contenido=tipo_contenido,
        contenido=url_contenido
    )

    db.add(db_noticia)
    db.commit()
    db.refresh(db_noticia)
    return db_noticia
