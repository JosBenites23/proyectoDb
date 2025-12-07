import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional, List
from bson import ObjectId
from client_mongo import get_db
from dataBase.modelTeam_mongo import Team
from dataBase.schemaTeam_mongo import TeamSchema
from config import URLBACK
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB_mongo import UserInDb

router = APIRouter()

# Construct an absolute path to the 'uploads' directory
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/team/", response_model=TeamSchema)
async def crear_Team(
    descripcion: Optional[str] = Form(None, max_length=10000),
    contenido: Optional[UploadFile] = File(None),
    db=Depends(get_db),
    current_user: UserInDb = Depends(get_current_user)
):
    ultimo = await db["team"].find_one({}, sort=[("_id", -1)])

    url_contenido = None
    if contenido:
        file_location = os.path.join(UPLOAD_DIR, contenido.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(contenido.file.read())
        url_contenido = f"{URLBACK}/uploads/{contenido.filename}"
    elif ultimo:
        url_contenido = ultimo.get("contenido")

    if descripcion is None and ultimo:
        descripcion = ultimo.get("descripcion")

    nuevo_Team = Team(
        descripcion=descripcion,
        contenido=url_contenido,
        autor_id=current_user.id
    )

    result = await db["team"].insert_one(nuevo_Team.dict(by_alias=True))
    created_team = await db["team"].find_one({"_id": result.inserted_id})
    return created_team

@router.get("/team/", response_model=List[TeamSchema])
async def obtener_team(db=Depends(get_db)):
    team_cursor = db["team"].find({}).sort("_id", -1)
    return await team_cursor.to_list(length=None)

@router.delete("/eliminar-col/{id}", response_model=TeamSchema)
async def eliminar_col(id: str, db=Depends(get_db)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de colaborador no válido")
    
    object_id = ObjectId(id)

    db_col = await db["team"].find_one_and_delete({"_id": object_id})
    
    if db_col is None:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    
    return db_col
