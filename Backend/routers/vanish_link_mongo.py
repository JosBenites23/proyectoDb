from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from client_mongo import get_db
from dataBase.schemaLink_mongo import LinkSchema
from utils.logger import create_log_entry

router = APIRouter()

@router.delete("/eliminar-link/{id}", response_model=LinkSchema)
async def eliminar_link(id: str, db=Depends(get_db)):
    # HACK: First, try to delete by string _id to handle malformed data.
    db_link = await db["link"].find_one_and_delete({"_id": id})
    
    # If that fails, try deleting by a proper ObjectId, just in case
    # some data is in the correct format.
    if db_link is None and ObjectId.is_valid(id):
        object_id = ObjectId(id)
        db_link = await db["link"].find_one_and_delete({"_id": object_id})
    
    if db_link is None:
        raise HTTPException(status_code=404, detail="Link no encontrado")

    # Log the action
    await create_log_entry(db, user_id="Anónimo", action=f"Eliminó link: '{db_link.get('titulo_link')}'", table_name="link", record_id=id)
        
    return db_link
