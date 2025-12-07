from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import text # ¡Importante añadir text!
from client import get_db
from config import URLBACK
from routers.auth.dependencies import get_current_user
from dataBase.modelinDB import UserInDb
# Ya no necesitamos importar Noticia y NewsSchema para la creación
# from dataBase.modelNews import Noticia
# from dataBase.schemaNews import NewsSchema

router = APIRouter()

# El response_model podría cambiar a un simple diccionario de éxito
@router.post("/subir-noticia")
async def crear_noticia(
    titulo: str = Form(..., max_length=600),
    descripcion: str = Form(..., max_length=100000),
    tipo_contenido: str = Form(...),
    contenido: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserInDb = Depends(get_current_user)
):
    # lógica para guardar el archivo no cambia
    upload_dir = "uploads"
    file_location = f"{upload_dir}/{contenido.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(contenido.file.read())

    url_contenido = f"{URLBACK}/uploads/{contenido.filename}"
    '''
    # --- Bloque Original ---
    nueva_noticia = Noticia(
        titulo=titulo,
        descripcion=descripcion,
        tipo_contenido=tipo_contenido,
        contenido=url_contenido,
        autor_id=current_user.id
    )
    db.add(nueva_noticia)
    db.commit()
    db.refresh(nueva_noticia)
    return nueva_noticia
    # --- Fin del Bloque Original ---
    '''

    # --- Bloque Modificado ---
    # Ya no creamos un objeto Noticia( ... )
    # En su lugar, llamamos al Stored Procedure
    db.execute(
        text("CALL sp_create_news(:titulo, :descripcion, :tipo_contenido, :contenido_url, :autor_id)"),
        {
            "titulo": titulo,
            "descripcion": descripcion,
            "tipo_contenido": tipo_contenido,
            "contenido_url": url_contenido,
            "autor_id": current_user.id
        }
    )
    db.commit()
    # --- Fin del Bloque Modificado ---

    # Como el SP no devuelve el objeto creado, retornamos un mensaje de éxito.
    # Opcionalmente, podríamos hacer un SELECT para devolver la noticia recién creada.
    return {"message": "Noticia creada con éxito"}