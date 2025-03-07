from schemas.base import UserBase

        
class UserRegisterIn(UserBase):
    password: str
    first_name: str
    last_name : str
    phone: str
    iban: str

class UserLoginIn(UserBase):
    password: str