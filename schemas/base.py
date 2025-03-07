from email_validator import EmailNotValidError, validate_email as validate_e
from pydantic import BaseModel, validator


class UserBase(BaseModel):
    email: str
   

    @validator("email")
    def validate_email(cls,v):
        try:
            validate_e(v)
            return v
        except EmailNotValidError:
            raise ValueError("Email not valid")


class BaseComplaint(BaseModel):
    title: str
    description: str
    photo_url: str
    amount: float