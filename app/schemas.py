import uuid
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    USER = "USER"
    PROFESSEUR = "PROFESSEUR"
    DECANAT = "DECANAT"
    
   



class registerSchema(BaseModel):
    username: str
    name: str
    password: str
    phone: str
    active: Optional[bool] = True
    admin: Optional[bool] = False
    role: UserRole = UserRole.USER

    class Config:
        from_attributes = True


class userResponse(registerSchema):
    password: str = Field(exclude=True)
    id: uuid.UUID = Field(primary_key=True)

    class Config:
        from_attributes = True


class loginSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class tokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    current_user: userResponse


class tokenResponseSchema(BaseModel):
    id: uuid.UUID = Field(primary_key=True)
    username: Optional[str] = None