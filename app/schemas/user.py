from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.post import PostDB
from app.schemas.topic import TopicDB


class UserBase(BaseModel):
    username: str
    gender: str
    date_of_creation: datetime
    id: int


class UserDB(UserBase):
    is_admin: bool


class UserAll(UserDB):
    model_config = ConfigDict(from_attributes=True)
    topics: list[TopicDB]
    posts: list[PostDB]
    img_url: str


class UserDBPass(BaseModel):
    password: str


class UserCreate(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    gender: str
    date_of_creation: datetime
    password: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    username: Optional[str] = None
    is_admin: Optional[bool] = None
