from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    header: str = Field(min_length=3, max_length=64)
    body: str = Field(min_length=1, max_length=6000)


class PostCreate(PostBase):
    topic_id: int


class PostDB(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    topic_id: int
    user_id: int


class PostUpdate(PostBase):
    pass
