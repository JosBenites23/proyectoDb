from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from dataBase.mongo_model_helpers import PyObjectId
from dataBase.modelNews_mongo import TipoContenido # Importamos el Enum

class NewsSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo_contenido: Optional[TipoContenido] = None
    contenido: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    autor_id: Optional[PyObjectId] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str, datetime: lambda dt: dt.isoformat()}
