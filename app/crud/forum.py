from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import models
from app.schemas.forum import ForumCreate


def get_all_forums_db(db: Session):
    stmt = select(models.Forum)
    forums = db.scalars(stmt).all()
    return forums


def get_forum_by_id_db(forum_id: int, db: Session):
    stmt = select(models.Forum).where(models.Forum.id == forum_id)
    forum = db.scalars(stmt).first()
    return forum


def create_forum_db(forum: ForumCreate, db: Session):
    db_forum = models.Forum(name=forum.name)
    db.add(db_forum)
    db.commit()
    db.refresh(db_forum)
    return db_forum


def delete_forum_by_id_db(forum_id: int, db: Session):
    forum = db.get(models.Forum, forum_id)
    db.delete(forum)
    db.commit()
    return {"deleted": forum}

#
# def update_topic_by_id(topic_id: int, topic_update: TopicUpdate, db: Session):
#     topic_db = db.get(models.Topic, topic_id)
#     topic_dict = topic_update.model_dump(exclude_unset=True)
#     for key, value in topic_dict.items():
#         setattr(topic_db, key, value)
#     db.add(topic_db)
#     db.commit()
#     db.refresh(topic_db)
#     return topic_db
