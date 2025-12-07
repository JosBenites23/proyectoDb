from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .mongo_model_helpers import PyObjectId

class Link(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: Optional[str] = None
    link: Optional[str] = None
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    autor_id: Optional[PyObjectId] = None # Reference to the User document

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
