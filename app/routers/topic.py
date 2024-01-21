from typing import Annotated

from fastapi import APIRouter, HTTPException, Security
from fastapi import Depends
from fastapi_pagination import Params, paginate, Page
from sqlalchemy.orm import Session

from app.crud import topic as crud_topic, forum as crud_forum
from app.dependencies import get_db, auth_scheme
from app.routers.auth import get_current_user
from app.schemas.exception import ExceptionHandler
from app.schemas.post import PostDB
from app.schemas.topic import TopicCreate, TopicDB, TopicUpdate
from app.schemas.user import UserDB

router = APIRouter(dependencies=[Depends(get_db), Security(get_current_user, scopes=["user"])], tags=["Topic"],
                   prefix="/crud/topic")


@router.get("/all", response_model=list[TopicDB])
def get_all_topics(current_user: Annotated[UserDB, Security(get_current_user, scopes=["admin"])],
                   db: Session = Depends(get_db)):
    return crud_topic.get_all_topics_db(db)


@router.get("/{topic_id}", response_model=Page[PostDB])
def get_topic_by_id(topic_id: int, page: int, db: Session = Depends(get_db)):
    topic = crud_topic.get_by_topic_id_db(topic_id, db)
    if not topic:
        raise ExceptionHandler(status_code=404, detail="Topic not found")
    if not topic.posts:
        raise ExceptionHandler(status_code=404, detail="No posts found in this topic",
                               headers={"error_place": "nopost"})
    params = Params(page=page, size=6)
    return paginate(topic.posts, params)


@router.post("/add", response_model=TopicDB)
def create_topic(topic: TopicCreate, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])],
                 db: Session = Depends(get_db)):
    forum = crud_forum.get_forum_by_id_db(topic.forum_id, db)
    if not forum:
        raise HTTPException(status_code=404,
                            detail="Forum with id: " + str(topic.forum_id) + " does not exists, can't add topic")
    return crud_topic.create_topic_db(topic, current_user.id, db)


@router.delete("/{topic_id}")
def remove_topic_by_id(topic_id: int, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])],
                       db: Session = Depends(get_db)):
    topic = crud_topic.get_by_topic_id_db(topic_id, db)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found, cannot delete")
    if current_user.is_admin:
        return crud_topic.delete_topic_by_id_db(topic_id, db)
    if current_user.id != topic.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized!")
    return crud_topic.delete_topic_by_id_db(topic_id, db)


@router.patch("/{topic_id}")
def patch_topic_by_id(topic_id: int, topic_update: TopicUpdate,
                      current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])],
                      db: Session = Depends(get_db)):
    topic = crud_topic.get_by_topic_id_db(topic_id, db)
    topic_updated = crud_topic.get_by_topic_id_db(topic_update.id, db)
    if topic_updated:
        raise HTTPException(status_code=409, detail="This ID already exists")
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found, cannot patch")
    if current_user.is_admin:
        return crud_topic.update_topic_by_id(topic_id, topic_update, db)
    if current_user.id != topic.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized!")
    return crud_topic.update_topic_by_id(topic_id, topic_update, db)
