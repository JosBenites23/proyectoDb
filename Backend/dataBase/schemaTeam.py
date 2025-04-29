from pydantic import BaseModel
from typing import Optional

class TeamSchema(BaseModel):
    id: Optional[int] = None 
    descripcion: str 
    contenido: str # Puede ser texto, URL de imagen o URL de video

    class Config:
        orm_mode = True