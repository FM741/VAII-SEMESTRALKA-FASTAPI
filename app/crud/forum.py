from fastapi_pagination import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import models
from app.schemas.forum import ForumCreate, ForumBase


def get_all_forums_db(db: Session):
    stmt = select(models.Forum)
    forums = db.scalars(stmt).all()
    return forums


def get_forum_by_id_db(forum_id: int, db: Session):
    stmt = select(models.Forum).where(models.Forum.id == forum_id)
    forum = db.scalars(stmt).first()
    return forum


def create_forum_db(forum: ForumCreate, user_id: int, db: Session):
    db_forum = models.Forum(name=forum.name, user_id=user_id)
    db.add(db_forum)
    db.commit()
    db.refresh(db_forum)
    return db_forum


def delete_forum_by_id_db(forum_id: int, db: Session):
    forum = db.get(models.Forum, forum_id)
    db.delete(forum)
    db.commit()
    return {"deleted": forum}


def edit_forum_by_id_db(forum_id: int, forum_update: ForumBase, db: Session):
    forum_db = db.get(models.Forum, forum_id)
    forum_dict = forum_update.model_dump(exclude_unset=True)
    for key, value in forum_dict.items():
        setattr(forum_db, key, value)
    db.add(forum_db)
    db.commit()
    db.refresh(forum_db)
    return forum_db

