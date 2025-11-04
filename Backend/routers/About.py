from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelAbout import About
from dataBase.schemaAbout import AboutSchema
from client import get_db
from fastapi import UploadFile, File, Form
from typing import Optional
from config import URLBACK
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB import UserInDb

router = APIRouter()

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
    db: Session = Depends(get_db),
    current_user: UserInDb = Depends(get_current_user)
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
    if presencia is not None:
        about.presencia = presencia
    if imagen is not None:
        upload_dir = "uploads"
        file_location = f"{upload_dir}/{imagen.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen.file.read())
        about.imagen = f"{URLBACK}/uploads/{imagen.filename}"
    if imagen2 is not None:
        upload_dir = "uploads"
        file_location = f"{upload_dir}/{imagen2.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen2.file.read())
        about.imagen2 = f"{URLBACK}/uploads/{imagen2.filename}"
    if imagen3 is not None:
        upload_dir = "uploads"
        file_location = f"{upload_dir}/{imagen3.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen3.file.read())
        about.imagen3 = f"{URLBACK}/uploads/{imagen3.filename}"
    if anio is not None:
        about.anio = anio
    if anio2 is not None:
        about.anio2 = anio2
        
    autor_id = current_user.id

    db.commit()
    db.refresh(about)
    return about

@router.get("/about/", response_model=AboutSchema)
def get_about(db: Session = Depends(get_db)):
    about = db.query(About).first()
    if not about:
        raise HTTPException(status_code=404, detail="No hay información de Sobre Nosotros")
    return about