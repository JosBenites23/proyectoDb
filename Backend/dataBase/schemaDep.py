from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LinkBase(BaseModel):
    titulo: str
    url: str

class LinkCreate(LinkBase):
    pass

class LinkSchema(LinkBase):
    id: Optional[int]
    fecha_creacion: Optional[datetime]

    class Config:
        orm_mode = True


class DepartamentoBase(BaseModel):
    titulo: str
    descripcion: str

class DepartamentoCreate(DepartamentoBase):
    imagen: str  # ruta o nombre del archivo subido
    links: Optional[List[LinkCreate]] = []

class DepartamentoSchema(DepartamentoBase):
    id: int
    slug: str
    imagen: str
    fecha_creacion: datetime
    links: List[LinkSchema] = []

    class Config:
        orm_mode = True

class DepartamentoCard(BaseModel):
    id: int
    titulo: str
    slug: str
    imagen: str
    descripcion: str

    class Config:
        orm_mode = True

