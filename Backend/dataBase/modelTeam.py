from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from client import Base

class TeamModel(Base):
    __tablename__ = "Team"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(10000))
    contenido = Column(Text, index=True)  # texto, imagen, video, mixto

    class Config:
        orm_mode = True