from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Forum(Base):
    __tablename__ = "forums"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    date_of_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    topics: Mapped[List["Topic"]] = relationship("Topic", back_populates="forum", cascade="all,delete,delete-orphan",
                                                 passive_deletes=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="forums")


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    date_of_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    forum_id: Mapped[int] = mapped_column(ForeignKey("forums.id", ondelete="CASCADE"))
    forum: Mapped["Forum"] = relationship(back_populates="topics")

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="topic", cascade='all,delete,delete-orphan',
                                               passive_deletes=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="topics")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    header: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(String(6000))
    date_of_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"))
    topic: Mapped["Topic"] = relationship(back_populates="posts")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    gender: Mapped[str] = mapped_column(String(10))
    is_admin: Mapped[bool] = mapped_column()
    img_url: Mapped[str] = mapped_column()

    date_of_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    forums: Mapped[List["Forum"]] = relationship("Forum", back_populates="user")
    topics: Mapped[List["Topic"]] = relationship("Topic", back_populates="user")
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")
