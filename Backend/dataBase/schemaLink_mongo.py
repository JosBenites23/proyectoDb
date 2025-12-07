from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .mongo_model_helpers import PyObjectId

class LinkSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: Optional[str] = None
    link: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    autor_id: Optional[PyObjectId] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str, datetime: lambda dt: dt.isoformat()}

class LinkCreate(BaseModel):
    name: str
    link: str
