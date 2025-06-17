from pydantic import BaseModel

class AboutSchema(BaseModel):
    id: int | None = None
    historia: str | None = None
    mision: str | None = None
    vision: str | None = None
    presencia: str | None = None
    imagen: str | None = None
    imagen2: str | None = None
    imagen3: str | None = None
    anio: int | None = None
    anio2: int | None = None

    class Config:
        orm_mode = True