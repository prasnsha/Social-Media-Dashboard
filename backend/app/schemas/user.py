from typing import List, Optional
from pydantic import BaseModel, EmailStr
from schemas.post import Post

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    username: str
    password: str

class User(UserBase):
    id: int
    full_name: Optional[str] = None
    is_active: bool
    posts: List['Post'] = []

    class Config:
        orm_mode = True