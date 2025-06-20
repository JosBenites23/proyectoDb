from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelCompany import CoModel
from dataBase.schemaCompany import CoSchema
from client import get_db
from fastapi import UploadFile, File, Form
from config import URLBACK, URLFRONT
from typing import Optional 

router = APIRouter()

@router.post("/company/", response_model=CoSchema)
async def crear_Empresa(
    contenido: Optional[str] = Form(..., max_length=10000),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)):

    upload_dir = "uploads"
    file_location = f"{upload_dir}/{imagen.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(imagen.file.read())

    url_contenido = contenido if contenido else f"{URLBACK}/uploads/{imagen.filename}"

    nueva_Empresa = CoModel(
        #id=noticia.id,
        contenido=contenido,
        imagen=url_contenido
    )

    db.add(nueva_Empresa)
    db.commit()
    db.refresh(nueva_Empresa)
    return nueva_Empresa

@router.get("/company/", response_model=list[CoSchema])
async def obtener_Co(db: Session = Depends(get_db)):
    return db.query(CoModel).order_by(CoModel.id.desc()).all()

@router.delete("/eliminar-empresa/{id}", response_model=CoSchema)
async def eliminar_Co(id: int, db: Session = Depends(get_db)):
    # Buscar la noticia por su ID
    db_co = db.query(CoModel).filter(CoModel.id == id).first()
    
    if db_co is None:
        raise HTTPException(status_code=404, detail="Departamento no encontrada")
    
    # Eliminar la noticia de la base de datos
    db.delete(db_co)
    db.commit()
    
    return db_co