from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud import forum as crud_forum
from app.dependencies import get_db
from app.models import models
from app.schemas.exception import ExceptionHandler
from app.schemas.forum import ForumDB, ForumCreate, ForumBase

router = APIRouter(dependencies=[Depends(get_db)], tags=["Forum"], prefix="/crud/forum")


@router.get("/all", response_model=list[ForumDB])
def get_all_forums_db(db: Session = Depends(get_db)):
    forums = crud_forum.get_all_forums_db(db)
    if not forums:
        raise HTTPException(status_code=404, detail="No forums found")
    return crud_forum.get_all_forums_db(db)


@router.get("/{forum_id}", response_model=ForumDB)
def get_forum_by_id(forum_id: int, db: Session = Depends(get_db)):
    forum = crud_forum.get_forum_by_id_db(forum_id, db)
    if not forum:
        raise HTTPException(status_code=404, detail="No forum by that ID found")
    return crud_forum.get_forum_by_id_db(forum_id, db)


@router.post("/add", response_model=ForumDB)
def create_forum(forum: ForumCreate, db: Session = Depends(get_db)):
    stmt = select(models.Forum).where(models.Forum.name == forum.name)
    if db.execute(stmt).first() is not None:
        raise HTTPException(status_code=444, detail="This forum already exists")
    return crud_forum.create_forum_db(forum, db)


@router.delete("/{forum_id}")
def delete_forum_by_id(forum_id: int, db: Session = Depends(get_db)):
    return crud_forum.delete_forum_by_id_db(forum_id, db)


@router.patch("/{forum_id}")
def edit_forum_by_id(forum_id: int, forum: ForumBase, db: Session = Depends(get_db)):
    stmt = select(models.Forum).where(models.Forum.name == forum.name)
    if db.execute(stmt).first() is not None:
        raise HTTPException(status_code=444, detail="This forum already exists")
    return crud_forum.edit_forum_by_id_db(forum_id, forum, db)
