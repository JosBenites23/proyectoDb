from fastapi import APIRouter, Response, status

router = APIRouter()

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):

    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,  # importante si usas HTTPS
        samesite="Lax",  # Permite cookies en solicitudes de origen cruzado
    )
    return {"message": "Sesión cerrada correctamente"}