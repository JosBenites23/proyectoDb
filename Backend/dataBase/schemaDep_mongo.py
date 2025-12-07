from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .mongo_model_helpers import PyObjectId

# --- Schemas para Links (asociados a Departamentos) ---

class LinkSchemaDep(BaseModel): # Renombrado para evitar conflicto con el otro LinkSchema
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titulo_link: Optional[str] = None
    url: Optional[str] = None
    dep_id: PyObjectId

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}

# --- Schemas para Departamentos ---

class DepartamentoSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titulo: Optional[str] = None
    slug: Optional[str] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    autor_id: Optional[PyObjectId] = None
    links: List[LinkSchemaDep] = [] # Se poblará manualmente después de la consulta

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str, datetime: lambda dt: dt.isoformat()}

class DepartamentoCard(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    titulo: str
    slug: str
    imagen: str
    descripcion: str

    class Config:
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}