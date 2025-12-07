from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum as PyEnum
from .mongo_model_helpers import PyObjectId

# Definir un enum para los tipos de contenido
class TipoContenido(PyEnum):
    texto = "texto"
    imagen = "imagen"
    video = "video"
    mixto = "mixto"

class News(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_contenido: TipoContenido = TipoContenido.texto
    contenido: Optional[str] = None
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    autor_id: Optional[PyObjectId] = None # Reference to the User document

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
