import os
from fastapi import APIRouter, Depends, UploadFile, File, Form
from client_mongo import get_db
from config import PUBLIC_BACKEND_URL
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB_mongo import UserInDb
from dataBase.modelNews_mongo import News, TipoContenido
from utils.logger import create_log_entry

router = APIRouter()

# Construct an absolute path to the 'uploads' directory
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/subir-noticia")
async def crear_noticia(
    titulo: str = Form(..., max_length=600),
    descripcion: str = Form(..., max_length=100000),
    tipo_contenido: TipoContenido = Form(...),
    contenido: UploadFile = File(...),
    db=Depends(get_db),
    current_user: UserInDb = Depends(get_current_user)
):
    # Save file
    file_location = os.path.join(UPLOAD_DIR, contenido.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(contenido.file.read())

    url_contenido = f"{PUBLIC_BACKEND_URL}/uploads/{contenido.filename}"

    # Create Pydantic model instance
    nueva_noticia = News(
        titulo=titulo,
        descripcion=descripcion,
        tipo_contenido=tipo_contenido,
        contenido=url_contenido,
        autor_id=current_user.id
    )

    # Convert to dict for DB insertion
    noticia_dict = nueva_noticia.dict(by_alias=True)
    noticia_dict['tipo_contenido'] = noticia_dict['tipo_contenido'].value
    result = await db["news"].insert_one(noticia_dict)
    
    # Log the action
    new_id = str(result.inserted_id)
    await create_log_entry(db, user_id=str(current_user.id), action=f"Creó noticia: '{titulo}'", table_name="news", record_id=new_id)

    # Build and return response
    noticia_dict["id"] = new_id
    return noticia_dict
