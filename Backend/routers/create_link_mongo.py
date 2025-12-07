from fastapi import APIRouter, Depends
from typing import List
from client_mongo import get_db
from dataBase.modelLink_mongo import Link
from dataBase.schemaLink_mongo import LinkCreate, LinkSchema
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB_mongo import UserInDb
from utils.logger import create_log_entry

router = APIRouter()

@router.post("/links/")
async def crear_link(
    link: LinkCreate, 
    db=Depends(get_db), 
    current_user: UserInDb = Depends(get_current_user)
):
    nuevo_link_data = link.dict()
    nuevo_link_data['autor_id'] = current_user.id
    
    nuevo_link = Link(**nuevo_link_data)

    link_dict = nuevo_link.dict(by_alias=True)
    result = await db["link"].insert_one(link_dict)
    
    new_id = str(result.inserted_id)
    link_dict["id"] = new_id

    # Log the action
    await create_log_entry(db, user_id=str(current_user.id), action=f"Creó link: '{link.titulo}'", table_name="link", record_id=new_id)

    return link_dict

@router.get("/links/")
async def obtener_links(db=Depends(get_db)):
    links_cursor = db["link"].find({}).sort("fecha_creacion", -1)
    
    lista_links = []
    async for link_dict in links_cursor:
        lista_links.append({
            "id": str(link_dict["_id"]),
            "titulo": link_dict.get("titulo"),
            "url": link_dict.get("url"),
            "fecha_creacion": link_dict.get("fecha_creacion"),
            "autor_id": str(link_dict.get("autor_id"))
        })
    return lista_links
