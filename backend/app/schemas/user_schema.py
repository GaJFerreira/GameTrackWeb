# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    steam_id: str 
    
    personaname: Optional[str] = None
    realname: Optional[str] = None
    avatar: Optional[str] = None
    profileurl: Optional[str] = None
    loccountrycode: Optional[str] = None

class UserCreate(UserBase):
    password: str 

class UserUpdate(BaseModel):
    steam_id: Optional[str] = None

class User(UserBase):
    id: str
    
    class Config:
        from_attributes = True