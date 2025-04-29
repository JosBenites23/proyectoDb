from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from client import get_db
from dataBase.schemaNews import NewsSchema
from dataBase.modelinDB import UserInDb as User
from dataBase.modelNews import Noticia

router = APIRouter()

@router.delete("/eliminar-noticia/{id}", response_model=NewsSchema)
async def eliminar_noticia(id: int, db: Session = Depends(get_db)):
    # Buscar la noticia por su ID
    db_noticia = db.query(Noticia).filter(Noticia.id == id).first()
    
    if db_noticia is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    
    # Eliminar la noticia de la base de datos
    db.delete(db_noticia)
    db.commit()
    
    return db_noticia
