from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelTeam import TeamModel
from dataBase.schemaTeam import TeamSchema
from client import get_db
from fastapi import UploadFile, File, Form

router = APIRouter()

@router.post("/team/", response_model=TeamSchema)
async def crear_Team(
    descripcion: str = Form(..., max_length=10000),
    contenido: UploadFile = File(...),
    db: Session = Depends(get_db)):

    upload_dir = "uploads"
    file_location = f"{upload_dir}/{contenido.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(contenido.file.read())

    url_contenido = f"http://9.0.1.247:8081/uploads/{contenido.filename}"

    nuevo_Team = TeamModel(
        #id=noticia.id,
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