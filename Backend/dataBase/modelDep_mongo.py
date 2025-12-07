from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .mongo_model_helpers import PyObjectId

class Link(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titulo_link: Optional[str] = None
    url: Optional[str] = None
    dep_id: PyObjectId # Reference to the Dep document

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        # A workaround for the issue with Pydantic v1 and ObjectId (Field(default_factory=PyObjectId))
        # This will be handled better in Pydantic v2
        # Example for Pydantic v1:
        # allow_population_by_field_name = True


class Dep(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titulo: Optional[str] = None
    slug: Optional[str] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    autor_id: Optional[PyObjectId] = None # Reference to the User document

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        # allow_population_by_field_name = True
