from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import models
from app.schemas.topic import TopicCreate, TopicUpdate


def get_all_topics_db(db: Session):
    stmt = select(models.Topic)
    topics = db.scalars(stmt).all()
    return topics


def get_by_topic_id_db(topic_id: int, db: Session):
    stmt = select(models.Topic).where(models.Topic.id == topic_id)
    topic = db.scalars(stmt).first()
    return topic


def get_topic_user_id(topic_id: int, db: Session):
    stmt = select(models.Topic).where(models.Topic.id == topic_id)
    topic = db.scalars(stmt).first()
    user_id = topic.user_id
    return user_id


def create_topic_db(topic: TopicCreate, user_id: int, db: Session):
    db_topic = models.Topic(name=topic.name, forum_id=topic.forum_id, user_id=user_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def delete_topic_by_id_db(topic_id: int, db: Session):
    topic = db.get(models.Topic, topic_id)
    db.delete(topic)
    db.commit()
    return {"deleted": topic}


def update_topic_by_id(topic_id: int, topic_update: TopicUpdate, db: Session):
    topic_db = db.get(models.Topic, topic_id)
    topic_dict = topic_update.model_dump(exclude_unset=True)
    for key, value in topic_dict.items():
        setattr(topic_db, key, value)
    db.add(topic_db)
    db.commit()
    db.refresh(topic_db)
    return topic_db
