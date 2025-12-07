from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from dataBase.modelinDB_mongo import UserInDb as User
from routers.auth.jwt_handler import verify_token_from_cookie
from client_mongo import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(request: Request, db = Depends(get_db)):
    username = verify_token_from_cookie(request)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = await db["users"].find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return User(**user)
