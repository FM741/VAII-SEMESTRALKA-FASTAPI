from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str = None
    gender: str = None
    date_of_creation: datetime = None
    id: int


class UserDB(UserBase):
    password: str
    is_admin: bool


class UserCreate(BaseModel):
    username: str = None
    gender: str = None
    date_of_creation: datetime = None
    password: str
