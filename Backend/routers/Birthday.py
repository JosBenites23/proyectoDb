from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelBirthday import birthdayModel
from dataBase.schemaBirthday import BirthdaySchema
from client import get_db
from fastapi import UploadFile, File, Form
from typing import Optional

router = APIRouter()

@router.post("/birthday/", response_model=BirthdaySchema)
async def crear_cumpleanos(
    descripcion: Optional[str] = Form(None, max_length=500),
    contenido: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)):

    ultimo = db.query(birthdayModel).order_by(birthdayModel.id.desc()).first()

    url_contenido = None

    if contenido is not None:
        upload_dir = "uploads"
        file_location = f"{upload_dir}/{contenido.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(contenido.file.read())
        url_contenido = f"http://9.0.1.247:8081/uploads/{contenido.filename}"
    elif ultimo:
        url_contenido = ultimo.contenido

    if descripcion is None and ultimo:
        descripcion = ultimo.descripcion

    nuevo_cumpleanos = birthdayModel(
        descripcion=descripcion,
        contenido=url_contenido
    )

    db.add(nuevo_cumpleanos)
    db.commit()
    db.refresh(nuevo_cumpleanos)
    return nuevo_cumpleanos

@router.get("/birthday/", response_model=list[BirthdaySchema])
async def obtener_cumpleanos(db: Session = Depends(get_db)):
    return db.query(birthdayModel).order_by(birthdayModel.id.desc()).all()