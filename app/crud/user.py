import datetime

from fastapi import UploadFile, File
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import models
from app.routers.auth import get_password_hash
from app.schemas.user import UserCreate, UserUpdate
from passlib.hash import pbkdf2_sha256


def get_all_users_db(db: Session):
    stmt = select(models.User)
    users = db.scalars(stmt).all()
    return users


def get_by_user_id_db(user_id: int, db: Session):
    stmt = select(models.User).where(models.User.id == user_id)
    user = db.scalars(stmt).first()
    return user


def create_user_db(user: UserCreate, db: Session):
    hashed = get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed, gender=user.gender,
                          date_of_creation=datetime.datetime.now().isoformat(), is_admin=False, img_url="/static/img/user.png")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username_db(username: str, db: Session):
    stmt = select(models.User).where(models.User.username == username)
    user = db.scalars(stmt).first()
    return user


def update_user_by_id(user_id: int, user_update: UserUpdate, db: Session):
    user_db = db.get(models.User, user_id)
    if user_update.password:
        hashed = get_password_hash(user_update.password)
        user_update.password = hashed
    user_dict = user_update.model_dump(exclude_unset=True)
    for key, value in user_dict.items():
        setattr(user_db, key, value)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def save_image(user_id: int, file: UploadFile, db: Session):
    file_path = f"/app/app/static/img/user_image/{str(user_id)}.png"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    user_db = db.get(models.User, user_id)
    user_db.img_url = f"/static/img/user_image/{str(user_id)}.png"
    db.commit()
    return file_path
