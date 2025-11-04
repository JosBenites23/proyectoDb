from pydantic import BaseModel

class UserNewsStat(BaseModel):
    name: str
    username: str
    news_count: int

    class Config:
        orm_mode = True
