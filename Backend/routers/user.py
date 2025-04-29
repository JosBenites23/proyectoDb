from fastapi import APIRouter, HTTPException, status, Depends
from dataBase.modelinDB import UserInDb as User
from dataBase.schema import UserSchema
from sqlalchemy.orm import Session
from client import get_db

router = APIRouter(prefix="/user", tags=["User"], responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

@router.get("/", response_model=list[UserSchema])
async def user_get_all(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

