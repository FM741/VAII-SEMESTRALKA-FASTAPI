from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    gender: str
    date_of_creation: datetime
    id: int


class UserDB(UserBase):
    is_admin: bool


class UserDBPass(BaseModel):
    password: str


class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    gender: str
    date_of_creation: datetime
    password: str


class UserUpdate(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    is_admin: Optional[bool] = None

    class Config:
        orm_mode = True
