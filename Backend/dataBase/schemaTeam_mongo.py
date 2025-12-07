from pydantic import BaseModel, Field
from typing import Optional
from .mongo_model_helpers import PyObjectId

class TeamSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    descripcion: Optional[str] = None
    contenido: Optional[str] = None
    autor_id: Optional[PyObjectId] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
