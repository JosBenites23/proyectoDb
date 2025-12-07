from fastapi import APIRouter, Depends
from typing import List
from client_mongo import get_db
from dataBase.schemaNews_mongo import NewsSchema
from bson import ObjectId # Add import for ObjectId

router = APIRouter()

@router.get("/noticias") # Removed response_model
async def obtener_noticias(db=Depends(get_db)):
    noticias_cursor = db["news"].find({}).sort("fecha_creacion", -1)
    
    lista_noticias = []
    async for noticia_dict in noticias_cursor:
        # Manually construct the dictionary for each news item
        lista_noticias.append({
            "id": str(noticia_dict["_id"]), # Convert _id to string "id"
            "titulo": noticia_dict.get("titulo"),
            "descripcion": noticia_dict.get("descripcion"),
            "tipo_contenido": noticia_dict.get("tipo_contenido"),
            "contenido": noticia_dict.get("contenido"),
            "fecha_creacion": noticia_dict.get("fecha_creacion"),
            "autor_id": str(noticia_dict.get("autor_id")) # Ensure autor_id is also a string
        })
    return lista_noticias