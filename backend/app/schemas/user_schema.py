from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr
    password: str
    steam_id: Optional[int] = None

class UserCreate(UserBase):
    id: str

    pass

class User(UserBase):
    id: int

    class Config:
        from_atributes = True
