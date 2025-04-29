from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelBirthday import birthdayModel
from dataBase.schemaBirthday import BirthdaySchema
from client import get_db
from fastapi import UploadFile, File, Form

router = APIRouter()

@router.post("/birthday/", response_model=BirthdaySchema)
async def crear_cumpleanos(
    descripcion: str = Form(..., max_length=10000),
    contenido: UploadFile = File(...),
    db: Session = Depends(get_db)):

    upload_dir = "uploads"
    file_location = f"{upload_dir}/{contenido.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(contenido.file.read())

    url_contenido = f"http://127.0.0.1:8000/uploads/{contenido.filename}"

    nuevo_cumpleanos = birthdayModel(
        #id=noticia.id,
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