from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    name: str
    email: str
    disabled: bool

