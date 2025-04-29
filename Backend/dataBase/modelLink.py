from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from client import Base

class linkModel(Base):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    link = Column(String(1500), index=True)
    fecha_creacion = Column(DateTime, default=func.now())

    class Config:
        orm_mode = True
