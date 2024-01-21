from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import models
from app.schemas.post import PostCreate, PostDB, PostUpdate


def get_all_posts_db(db: Session):
    stmt = select(models.Post)
    posts = db.scalars(stmt).all()
    return posts


def get_by_post_id_db(post_id: int, db: Session):
    stmt = select(models.Post).where(models.Post.id == post_id)
    post = db.scalars(stmt).first()
    return post


def create_post_db(post: PostCreate, user_id: int, db: Session):
    db_post = models.Post(header=post.header, body=post.body, topic_id=post.topic_id, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post_by_id_db(post_id: int, db: Session):
    post = db.get(models.Post, post_id)
    db.delete(post)
    db.commit()
    return {"deleted": post}


def update_post_by_id(post_id: int, post_update: PostUpdate, db: Session):
    post_db = db.get(models.Post, post_id)
    post_dict = post_update.model_dump(exclude_unset=True)
    for key, value in post_dict.items():
        setattr(post_db, key, value)
    db.add(post_db)
    db.commit()
    db.refresh(post_db)
    return post_db
