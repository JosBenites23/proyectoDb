from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from client import Base

class UserInDb(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(500), unique=True, index=True)
    name = Column(String(500))
    email = Column(String(500), unique=True, index=True)
    hashed_password = Column(String(500))
    disabled = Column(Boolean, default=False)

    # Relación con noticias
    noticias = relationship("Noticia", back_populates="autor")
    
    # Relación con departamentos
    departamentos = relationship("Dep", back_populates="autor")

    # Relación con empresas
    empresas = relationship("CoModel", back_populates="autor")

    # Relación con links de soporte
    links_soporte = relationship("linkModel", back_populates="autor")

    # Relación con fotos de equipo
    fotos_team = relationship("TeamModel", back_populates="autor")

    # Relación con información "About"
    about_info = relationship("About", back_populates="autor")

    class Config:
        orm_mode = True
