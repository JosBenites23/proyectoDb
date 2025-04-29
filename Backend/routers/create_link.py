from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dataBase.modelLink import linkModel as Link
from dataBase.schemaLink import LinkCreate, LinkSchema
from client import get_db

router = APIRouter()

@router.post("/links/", response_model=LinkSchema)
async def crear_link(link: LinkCreate, db: Session = Depends(get_db)):
    nuevo_link = Link(**link.model_dump())
    db.add(nuevo_link)
    db.commit()
    db.refresh(nuevo_link)
    return nuevo_link

@router.get("/links/", response_model=list[LinkSchema])
async def obtener_links(db: Session = Depends(get_db)):
    return db.query(Link).order_by(Link.fecha_creacion.desc()).all()
