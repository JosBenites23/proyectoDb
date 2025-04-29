from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DepSchema(BaseModel):
    id: Optional[int] = None
    titulo: str 
    descripcion: str 
    contenido: str # Puede ser texto, URL de imagen o URL de video
    fecha_creacion: Optional[datetime] = None

    class Config:
        orm_mode = True
