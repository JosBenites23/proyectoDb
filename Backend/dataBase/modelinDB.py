from sqlalchemy import Column, Integer, String, Boolean
from client import Base

class UserInDb(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    class Config:
        orm_mode = True
