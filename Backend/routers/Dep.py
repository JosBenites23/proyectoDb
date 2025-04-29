from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from client import get_db
from dataBase.modelDep import Dep
from dataBase.schemaDep import DepSchema
from fastapi import UploadFile, File, Form

router = APIRouter()

@router.post("/departamento", response_model=DepSchema)
async def crear_departamento(
    titulo: str = Form(..., max_length=600),
    descripcion: str = Form(..., max_length=100000),
    contenido: UploadFile = File(...),
    db: Session = Depends(get_db)):
    

    upload_dir = "uploads"
    file_location = f"{upload_dir}/{contenido.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(contenido.file.read())

    url_contenido = f"http://127.0.0.1:8000/uploads/{contenido.filename}"
 
    db_departamento = Dep(
        #id=noticia.id,
        titulo=titulo,
        descripcion=descripcion,
        contenido=url_contenido
    )

    db.add(db_departamento)
    db.commit()
    db.refresh(db_departamento)
    return db_departamento

@router.get("/departamento", response_model=list[DepSchema])
def obtener_departamento(db: Session = Depends(get_db)):
    noticias = db.query(Dep).order_by(Dep.fecha_creacion.desc()).all()
    return noticias

@router.delete("/eliminar-dep/{id}", response_model=DepSchema)
async def eliminar_dep(id: int, db: Session = Depends(get_db)):
    # Buscar la noticia por su ID
    db_dep = db.query(Dep).filter(Dep.id == id).first()
    
    if db_dep is None:
        raise HTTPException(status_code=404, detail="Departamento no encontrada")
    
    # Eliminar la noticia de la base de datos
    db.delete(db_dep)
    db.commit()
    
    return db_dep
