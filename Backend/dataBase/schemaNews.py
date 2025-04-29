from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
from fastapi import UploadFile, File, Form

class NewsSchema(BaseModel):
    id: Optional[int] = None
    titulo: str 
    descripcion: str 
    tipo_contenido: str 
    contenido: str # Puede ser texto, URL de imagen o URL de video
    fecha_creacion: Optional[datetime] = None

    class Config:
        orm_mode = True
