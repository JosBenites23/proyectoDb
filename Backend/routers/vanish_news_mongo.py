from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from client_mongo import get_db
from dataBase.schemaNews_mongo import NewsSchema
from utils.logger import create_log_entry

router = APIRouter()

@router.delete("/eliminar-noticia/{id}", response_model=NewsSchema)
async def eliminar_noticia(id: str, db=Depends(get_db)):
    # HACK: First, try to delete by string _id to handle malformed data.
    db_noticia = await db["news"].find_one_and_delete({"_id": id})
    
    # If that fails, try deleting by a proper ObjectId for correctly formed data.
    if db_noticia is None and ObjectId.is_valid(id):
        object_id = ObjectId(id)
        db_noticia = await db["news"].find_one_and_delete({"_id": object_id})

    if db_noticia is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    # Log the action
    await create_log_entry(db, user_id="Anónimo", action=f"Eliminó noticia: '{db_noticia.get('titulo')}'", table_name="news", record_id=id)
        
    return db_noticia
