from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from client import get_db
from dataBase.modelNews import Noticia
from dataBase.schemaNews import NewsSchema

router = APIRouter()

@router.get("/noticias", response_model=list[NewsSchema])
def obtener_noticias(db: Session = Depends(get_db)):
    noticias = db.query(Noticia).order_by(Noticia.fecha_creacion.desc()).all()
    return noticias
