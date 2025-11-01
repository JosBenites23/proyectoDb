from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from client import get_db
from dataBase.modelNews import Noticia
from dataBase.schemaNews import NewsSchema
from fastapi import UploadFile, File, Form
from config import URLBACK
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB import UserInDb

router = APIRouter()

@router.post("/subir-noticia", response_model=NewsSchema)
async def crear_noticia(
    titulo: str = Form(..., max_length=600),
    descripcion: str = Form(..., max_length=100000),
    tipo_contenido: str = Form(...),
    contenido: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserInDb = Depends(get_current_user)
    ):
    

    upload_dir = "uploads"
    file_location = f"{upload_dir}/{contenido.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(contenido.file.read())

    url_contenido = f"{URLBACK}/uploads/{contenido.filename}"

    db_noticia = Noticia(
        titulo=titulo,
        descripcion=descripcion,
        tipo_contenido=tipo_contenido,
        contenido=url_contenido,
        autor_id=current_user.id
    )

    db.add(db_noticia)
    db.commit()
    db.refresh(db_noticia)
    return db_noticia