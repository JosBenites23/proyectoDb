from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from client import Base

class Dep(Base):
    __tablename__ = 'dep'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(500), unique=True, index=True)
    slug = Column(String(500), unique=True, index=True)  # Slug para la URL de la pagina dinamica
    descripcion = Column(Text)
    imagen = Column(String(500))  # Este es el contenido principal de la noticia (puede ser texto, URL de imagen o video)
    fecha_creacion = Column(DateTime, default=func.now())  # Fecha de creación

    links = relationship("Link", back_populates="departamento", cascade="all, delete")  # URL del link relacion con la tabla link

class Link(Base):
    __tablename__ = 'linkdep'

    id = Column(Integer, primary_key=True, index=True)
    titulo_link = Column(String(500), index=True)
    url = Column(String(500))  # Este es el link de la noticia puede ser pdf o word o link externo
    dep_id=Column(Integer, ForeignKey("dep.id")) #relacion con la tabla departamento (dep)
    fecha_creacion = Column(DateTime, default=func.now())  # Fecha de creación

    departamento = relationship("Dep", back_populates="links")
