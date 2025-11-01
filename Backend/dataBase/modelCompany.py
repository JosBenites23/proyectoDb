from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from client import Base
from .modelinDB import UserInDb

class CoModel(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(String(500))
    imagen = Column(String(500))  # imagen

    autor_id = Column(Integer, ForeignKey('users.id'))
    autor = relationship("UserInDb", back_populates="empresas")

    class Config:
        orm_mode = True