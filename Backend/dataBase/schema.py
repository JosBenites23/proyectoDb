from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    username: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    disabled: bool = False

    class Config:
        orm_mode = True # I will keep this to avoid breaking other parts of the code for now.