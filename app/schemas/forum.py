from pydantic import BaseModel

from .topic import TopicBase


class ForumBase(BaseModel):
    name: str


class ForumCreate(ForumBase):
    pass


class ForumDB(ForumBase):
    id: int
    user_id: int
    topics: list[TopicBase] = []

    class Config:
        orm_mode = True
