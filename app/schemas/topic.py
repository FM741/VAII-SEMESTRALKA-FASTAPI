from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TopicBase(BaseModel):
    name: str = Field(min_length=5, max_length=32)
    forum_id: int


class TopicCreate(TopicBase):
    pass


class TopicDB(TopicBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int


class TopicUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: Optional[str] = None
    forum_id: Optional[int] = None

