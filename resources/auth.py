from fastapi import APIRouter, Depends

from managers.user import UserManager
from schemas.request.user import UserLoginIn, UserRegisterIn


router = APIRouter(tags=["Auth"],)


@router.post("/register/", status_code=201)
async def register(user_data: UserRegisterIn):
    token = await UserManager.register(user_data.dict())
    return {"token":token}


@router.post("/login/", status_code=201)
async def login(user_data: UserLoginIn):
    token = await UserManager.login(user_data.dict())
    return {"token":token}


