from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from client import Base

class TeamModel(Base):
    __tablename__ = "Team"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text)
    contenido = Column(String(500))  # texto, imagen, video, mixto

    autor_id = Column(Integer, ForeignKey('users.id'))
    autor = relationship("UserInDb", back_populates="fotos_team")

    class Config:
        orm_mode = True