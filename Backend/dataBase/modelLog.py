from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from client import Base

class Log(Base):
    __tablename__ = 'logsdb'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    action = Column(String(50), nullable=False)
    table_name = Column(String(50), nullable=False)
    record_id = Column(Integer)
    timestamp = Column(DateTime, default=func.now())

    class Config:
        orm_mode = True