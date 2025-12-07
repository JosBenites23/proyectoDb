from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from .mongo_model_helpers import PyObjectId

class UserInDb(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: str
    disabled: bool = False

    class Config:
        arbitrary_types_allowed = True  
        json_encoders = {PyObjectId: str}
