from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from client import get_db
from dataBase.modelinDB import UserInDb
from routers.auth.jwt_handler import create_access_token
from dataBase.schemainDB import UserLogin

router = APIRouter()
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(UserInDb).filter(UserInDb.username == form_data.username).first()
    if not user or not crypt.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    ...
    token = create_access_token(data={"sub": user.username})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,  # importante si usas HTTPS
        samesite="Lax"
    )
    return {"message": "Login exitoso"}

'''
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserInDb).filter(UserInDb.username == form_data.username).first()
    if not user or not crypt.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
'''