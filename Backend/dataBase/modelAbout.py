from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from client import Base
from .modelinDB import UserInDb

class About(Base):
    __tablename__ = "about"
    id = Column(Integer, primary_key=True, index=True)
    historia = Column(Text, nullable=True)
    mision = Column(Text, nullable=True)
    vision = Column(Text, nullable=True)
    presencia = Column(Text, nullable=True)
    imagen = Column(Text, nullable=True)
    imagen2 = Column(Text, nullable=True)
    imagen3 = Column(Text, nullable=True)
    anio = Column(Text, nullable=True)
    anio2 = Column(Text, nullable=True)

    autor_id = Column(Integer, ForeignKey('users.id'))
    autor = relationship("UserInDb", back_populates="about_info")