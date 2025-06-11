from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelTeam import TeamModel
from dataBase.schemaTeam import TeamSchema
from client import get_db
from fastapi import UploadFile, File, Form
from typing import Optional
from config import URLBACK

router = APIRouter()

@router.post("/team/", response_model=TeamSchema)
async def crear_Team(
    descripcion: Optional[str] = Form(None, max_length=10000),
    contenido: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)):

    ultimo = db.query(TeamModel).order_by(TeamModel.id.desc()).first()

    url_contenido = None

    if contenido is not None:
        upload_dir = "uploads"
        file_location = f"{upload_dir}/{contenido.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(contenido.file.read())
        url_contenido = f"{URLBACK}/uploads/{contenido.filename}"
    elif ultimo:
        url_contenido = ultimo.contenido

    if descripcion is None and ultimo:
        descripcion = ultimo.descripcion

    nuevo_Team = TeamModel(
        descripcion=descripcion,
        contenido=url_contenido
    )

    db.add(nuevo_Team)
    db.commit()
    db.refresh(nuevo_Team)
    return nuevo_Team

@router.get("/team/", response_model=list[TeamSchema])
async def obtener_cumpleanos(db: Session = Depends(get_db)):
    return db.query(TeamModel).order_by(TeamModel.id.desc()).all()