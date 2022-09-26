from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class Base(BaseModel):
    class Config:
        orm_mode = True


class ResponseUser(Base):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    id: str


class User(Base):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserLogin(Base):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class Token(Base):
    access_token: str
    token_type: str


class TokenData(Base):
    username: Optional[str] = None
