from fastapi import HTTPException
from passlib.context import CryptContext
from db import database
from managers.auth import AuthManager
from models import user
from asyncpg import UniqueViolationError

from models.enums import RoleType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        if user_data["email"].endswith("@gmail.com"):
            user_data["role"] = RoleType.admin
        elif user_data["email"].endswith("@yahoo.com"):
            user_data["role"] = RoleType.approver
        else:
            user_data["role"] = RoleType.complainer
        try:
           id_ =await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        user_do = await database.fetch_one(user.select().where(user.c.id==id_))
        return AuthManager.create_access_token(user_do)
    
    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(user.select().where(user.c.email == user_data["email"]))
        if not user_do:
           raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong email or password")
        return AuthManager.create_access_token(user_do)
    
    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user.select())
    

    @staticmethod
    async def get_user_by_email(email):
        return await database.fetch_one(user.select().where(user.c.email == email))
    
    @staticmethod
    async def change_role(role: RoleType, user_id):
        await database.execute(user.update().where(user.c.id == user_id).values(role=role))

    
