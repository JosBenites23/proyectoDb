from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LinkBase(BaseModel):
    name: str
    link: str

class LinkCreate(LinkBase):
    pass

class LinkSchema(LinkBase):
    id: Optional[int] = None
    name: str 
    link: str 
    fecha_creacion: Optional[datetime] = None

    class Config:
        orm_mode = True
