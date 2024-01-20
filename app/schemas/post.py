from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    header: str
    body: str


class PostCreate(PostBase):
    topic_id: int


class PostDB(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    topic_id: int
    user_id: int


class PostUpdate(PostBase):
    pass
