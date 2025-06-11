from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelAbout import About
from dataBase.schemaAbout import AboutSchema
from client import get_db
from fastapi import UploadFile, File, Form
from typing import Optional
from config import URLBACK

router = APIRouter()

@router.put("/about/", response_model=AboutSchema)
async def update_about(
    historia: Optional[str] = Form(None),
    mision: Optional[str] = Form(None),
    vision: Optional[str] = Form(None),
    valores: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    about = db.query(About).first()
    if not about:
        raise HTTPException(status_code=404, detail="No existe información de Sobre Nosotros")

    if historia is not None:
        about.historia = historia
    if mision is not None:
        about.mision = mision
    if vision is not None:
        about.vision = vision
    if valores is not None:
        about.valores = valores
    if imagen is not None:
        upload_dir = "uploads"
        file_location = f"{upload_dir}/{imagen.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen.file.read())
        about.imagen = f"{URLBACK}/uploads/{imagen.filename}"

    db.commit()
    db.refresh(about)
    return about

@router.get("/about/", response_model=AboutSchema)
def get_about(db: Session = Depends(get_db)):
    about = db.query(About).first()
    if not about:
        raise HTTPException(status_code=404, detail="No hay información de Sobre Nosotros")
    return about