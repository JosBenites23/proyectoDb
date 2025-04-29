from pydantic import BaseModel
from typing import Optional

class CoSchema(BaseModel):
    id: Optional[int] = None 
    contenido: str 
    imagen: str # Puede ser texto, URL de imagen o URL de video

    class Config:
        orm_mode = True