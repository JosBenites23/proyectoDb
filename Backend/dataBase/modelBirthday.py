from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from client import Base

class birthdayModel(Base):
    __tablename__ = "birthday"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text)
    contenido = Column(String(500))  # texto, imagen, video, mixto

    class Config:
        orm_mode = True