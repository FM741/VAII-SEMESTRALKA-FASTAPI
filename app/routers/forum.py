from typing import Annotated

from fastapi import APIRouter, HTTPException, Security, Query
from fastapi import Depends
from fastapi_pagination import Page, paginate, Params
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud import forum as crud_forum
from app.dependencies import get_db, auth_scheme
from app.models import models
from app.routers.auth import get_current_user
from app.schemas.exception import ExceptionHandler
from app.schemas.forum import ForumDB, ForumCreate, ForumBase
from app.schemas.topic import TopicDB
from app.schemas.user import UserDB

router = APIRouter(dependencies=[Depends(get_db), Security(get_current_user, scopes=["admin"])], tags=["Forum"], prefix="/crud/forum")


@router.get("/all", response_model=Page[ForumDB])
def get_all_forums(page: int, db: Session = Depends(get_db)):
    forums = crud_forum.get_all_forums_db(db)
    if not forums:
        raise ExceptionHandler(status_code=404, detail="There are no forums", headers={"error_place": "forum"})
    params = Params(page=page, size=10)
    return paginate(forums, params)


@router.get("/{forum_id}", response_model=Page[TopicDB])
def get_forum_by_id(forum_id: int, page: int, db: Session = Depends(get_db)):
    forum = crud_forum.get_forum_by_id_db(forum_id, db)
    if not forum:
        raise ExceptionHandler(status_code=404, detail="Forum not found")
    params = Params(page=page, size=12)
    return paginate(forum.topics, params)


@router.post("/add", response_model=ForumDB)
def create_forum(forum: ForumCreate, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])], db: Session = Depends(get_db)):
    stmt = select(models.Forum).where(models.Forum.name == forum.name)
    if db.execute(stmt).first() is not None:
        raise HTTPException(status_code=444, detail="This forum already exists")
    return crud_forum.create_forum_db(forum, current_user.id, db)


@router.delete("/{forum_id}")
def delete_forum_by_id(forum_id: int, db: Session = Depends(get_db)):
    return crud_forum.delete_forum_by_id_db(forum_id, db)


@router.patch("/{forum_id}")
def edit_forum_by_id(forum_id: int, forum: ForumBase, db: Session = Depends(get_db)):
    stmt = select(models.Forum).where(models.Forum.name == forum.name)
    if db.execute(stmt).first() is not None:
        raise HTTPException(status_code=444, detail="This forum already exists")
    return crud_forum.edit_forum_by_id_db(forum_id, forum, db)
