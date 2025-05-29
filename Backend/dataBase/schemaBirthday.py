from pydantic import BaseModel
from typing import Optional

class BirthdaySchema(BaseModel):
    id: Optional[int] = None 
    descripcion: str | None = None
    contenido: str | None = None

    class Config:
        orm_mode = True