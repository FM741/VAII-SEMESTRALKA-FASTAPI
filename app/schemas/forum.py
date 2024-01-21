from pydantic import BaseModel, ConfigDict, Field

from .topic import TopicBase


class ForumBase(BaseModel):
    name: str = Field(min_length=3, max_length=16)


class ForumCreate(ForumBase):
    pass


class ForumDB(ForumBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    topics: list[TopicBase] = []
