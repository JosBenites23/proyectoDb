from sqlalchemy import Column, Integer, String
from client import Base

class About(Base):
    __tablename__ = "about"
    id = Column(Integer, primary_key=True, index=True)
    historia = Column(String, nullable=True)
    mision = Column(String, nullable=True)
    vision = Column(String, nullable=True)
    valores = Column(String, nullable=True)
    imagen = Column(String, nullable=True)