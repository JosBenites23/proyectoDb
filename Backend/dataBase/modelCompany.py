from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from client import Base

class CoModel(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(String(10000))
    imagen = Column(Text, index=True)  # imagen

    class Config:
        orm_mode = True