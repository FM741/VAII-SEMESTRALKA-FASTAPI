from typing import Optional

from pydantic import BaseModel


class TopicBase(BaseModel):
    name: str
    forum_id: int


class TopicCreate(TopicBase):
    pass


class TopicDB(TopicBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True


class TopicUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    forum_id: Optional[int] = None

    class Config:
        orm_mode = True
