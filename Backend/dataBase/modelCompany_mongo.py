from pydantic import BaseModel, Field
from typing import Optional
from .mongo_model_helpers import PyObjectId # Importamos PyObjectId de forma modular

class Company(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    contenido: Optional[str] = None
    imagen: Optional[str] = None
    autor_id: Optional[PyObjectId] = None # Referencia al ID del autor

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str} # Usamos PyObjectId aquí también
