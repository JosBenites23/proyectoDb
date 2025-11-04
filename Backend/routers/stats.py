from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from client import get_db
from typing import List

from dataBase.modelinDB import UserInDb
from dataBase.modelNews import Noticia
from dataBase.schemaStats import UserNewsStat 

router = APIRouter(prefix="/stats", tags=["Estadísticas"])

@router.get("/news_per_user", response_model=List[UserNewsStat])
def get_news_stats_per_user(db: Session = Depends(get_db)):
    """
    Devuelve una lista de usuarios y la cantidad de noticias que cada uno ha publicado.
    Demuestra el uso de JOIN, funciones de agregación (COUNT) y GROUP BY.
    """
    
    results = db.query(
        UserInDb.name,
        UserInDb.username,
        func.count(Noticia.id).label("news_count")
    ).join(
        Noticia, UserInDb.id == Noticia.autor_id
    ).group_by(
        UserInDb.id, UserInDb.name, UserInDb.username # Agrupar por todas las columnas no agregadas
    ).order_by(
        func.count(Noticia.id).desc()
    ).all()

    return results
