from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelLink import linkModel
from dataBase.schemaLink import LinkSchema
from client import get_db

router = APIRouter()

@router.delete("/eliminar-link/{id}", response_model=LinkSchema)
async def eliminar_link(id: int, db: Session = Depends(get_db)):
    # Buscar la noticia por su ID
    db_link = db.query(linkModel).filter(linkModel.id == id).first()
    
    if db_link is None:
        raise HTTPException(status_code=404, detail="link no encontrado")
    
    # Eliminar la noticia de la base de datos
    db.delete(db_link)
    db.commit()
    
    return db_link