from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from client import Base

# Definir un enum para los tipos de contenido
class TipoContenido(PyEnum):
    texto = "texto"
    imagen = "imagen"
    video = "video"
    mixto = "mixto"  # Para soportar texto + imagen/video

class Noticia(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), index=True)
    descripcion = Column(Text)
    tipo_contenido = Column(Enum(TipoContenido), default=TipoContenido.texto)
    contenido = Column(Text)  # Este es el contenido principal de la noticia (puede ser texto, URL de imagen o video)
    fecha_creacion = Column(DateTime, default=func.now())  # Fecha de creación

    class Config:
        orm_mode = True

