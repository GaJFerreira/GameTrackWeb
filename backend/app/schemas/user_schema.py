from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):

    email: EmailStr
    password: str
    steam_id: str


class UserCreate(UserBase):

    # Não pedimos o ID na criação.
    pass


class User(UserBase):

    id: str

    class Config:

        from_attributes = True