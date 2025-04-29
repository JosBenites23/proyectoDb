from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    name: str
    email: str
    disabled: bool

    class Config:
        orm_mode = True

