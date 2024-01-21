from datetime import datetime
from typing import Optional, Literal

from fastapi import HTTPException
from pydantic import BaseModel, Field, ConfigDict, field_validator
from starlette import status

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
    gender: Literal["Male", "Female", "Other"]
    password: str = Field(min_length=5)


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: Optional[str] = Field(None, min_length=5)
    password: Optional[str] = Field(None, min_length=5)
    is_admin: Optional[bool] = None
