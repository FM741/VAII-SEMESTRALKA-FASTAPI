from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Forum(Base):
    __tablename__ = "forums"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    topics: Mapped[List["Topic"]] = relationship("Topic", back_populates="forum", cascade="all,delete,delete-orphan", passive_deletes=True)


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))

    forum_id: Mapped[int] = mapped_column(ForeignKey("forums.id", ondelete="CASCADE"))
    forum: Mapped["Forum"] = relationship(back_populates="topics")

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="topic", cascade='all,delete,delete-orphan',
                                               passive_deletes=True)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    header: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(String(10000))

    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))
    topic: Mapped["Topic"] = relationship(back_populates="posts")
