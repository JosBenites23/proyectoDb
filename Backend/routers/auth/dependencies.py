from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from routers.auth.jwt_handler import verify_token_from_cookie
from sqlalchemy.orm import Session
from client import get_db
from dataBase.modelinDB import UserInDb as User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    username = verify_token_from_cookie(request)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
