from pydantic import BaseModel, Field
from typing import Optional
from .mongo_model_helpers import PyObjectId

class About(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    historia: Optional[str] = None
    mision: Optional[str] = None
    vision: Optional[str] = None
    presencia: Optional[str] = None
    imagen: Optional[str] = None
    imagen2: Optional[str] = None
    imagen3: Optional[str] = None
    anio: Optional[str] = None
    anio2: Optional[str] = None
    autor_id: Optional[PyObjectId] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
