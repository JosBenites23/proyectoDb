from pydantic import BaseModel

class AboutSchema(BaseModel):
    id: int | None = None
    historia: str | None = None
    mision: str | None = None
    vision: str | None = None
    valores: str | None = None
    imagen: str | None = None

    class Config:
        orm_mode = True