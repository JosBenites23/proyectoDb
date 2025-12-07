from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from client_mongo import get_db
from dataBase.modelinDB_mongo import UserInDb
from routers.auth.jwt_handler import create_access_token

router = APIRouter()
crypt = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = await db["users"].find_one({"username": form_data.username})
    if not user or not crypt.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    if user["disabled"]:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    access_token = create_access_token(data={"sub": user["username"]})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True if using HTTPS in production
        samesite="Lax",
    )
    return {"message": "Login exitoso"}
