from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .mongo_model_helpers import PyObjectId

class Log(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: Optional[str] = None
    action: str
    table_name: str
    record_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
