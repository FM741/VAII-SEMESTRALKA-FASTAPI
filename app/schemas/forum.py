from pydantic import BaseModel, ConfigDict

from .topic import TopicBase


class ForumBase(BaseModel):
    name: str


class ForumCreate(ForumBase):
    pass


class ForumDB(ForumBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    topics: list[TopicBase] = []
