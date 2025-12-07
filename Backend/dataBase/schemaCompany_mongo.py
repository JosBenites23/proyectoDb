from pydantic import BaseModel, Field
from typing import Optional
from .mongo_model_helpers import PyObjectId

class CoSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    contenido: Optional[str] = None
    imagen: Optional[str] = None
    autor_id: Optional[PyObjectId] = None # Agregamos el autor_id que faltaba

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
