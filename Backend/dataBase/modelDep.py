from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from client import Base

class Dep(Base):
    __tablename__ = 'departamento'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(500), index=True)
    descripcion = Column(Text)
    contenido = Column(String(500))  # Este es el contenido principal de la noticia (puede ser texto, URL de imagen o video)
    pdf = Column(String(500))  # URL del PDF
    fecha_creacion = Column(DateTime, default=func.now())  # Fecha de creación

    class Config:
        orm_mode = True
