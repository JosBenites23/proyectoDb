from fastapi import APIRouter, Depends
from routers.auth.dependencies import get_current_user  

router = APIRouter()

@router.get("/protegida")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hola, {current_user.username}. Tienes acceso autorizado."}
