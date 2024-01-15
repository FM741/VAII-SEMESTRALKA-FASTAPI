from pydantic import BaseModel


class PostBase(BaseModel):
    header: str
    body: str
    user_id: int


class PostCreate(PostBase):
    topic_id: int


class PostDB(PostBase):
    id: int
    topic_id: int

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    pass
