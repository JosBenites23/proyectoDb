from fastapi import APIRouter, status, Depends
from typing import List
from dataBase.schema import UserSchema
from client_mongo import get_db # Import from the new client_mongo.py

router = APIRouter(prefix="/user", tags=["User"], responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

@router.get("/", response_model=List[UserSchema])
async def user_get_all(db=Depends(get_db)):
    users_cursor = db["users"].find({})
    # The response_model will automatically handle the conversion
    # from the list of dicts to a list of UserSchema objects.
    # FastAPI is smart enough to do this as long as the keys match.
    users = await users_cursor.to_list(length=1000)
    return users