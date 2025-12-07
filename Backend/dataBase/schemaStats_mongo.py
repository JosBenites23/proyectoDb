from pydantic import BaseModel
from typing import Optional

class UserNewsStat(BaseModel):
    # El _id será un diccionario en el resultado de la agregación
    # Lo mapearemos a campos individuales
    name: Optional[str] = None
    username: Optional[str] = None
    news_count: int

    class Config:
        # Pydantic necesita saber que puede poblar el modelo desde un diccionario
        pass
