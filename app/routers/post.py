from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud import post as crud_post
from app.dependencies import get_db, auth_scheme
from app.schemas.post import PostCreate, PostDB, PostUpdate

router = APIRouter(dependencies=[Depends(get_db)], tags=["Post"], prefix="/crud/post")


@router.post("/add", response_model=PostDB)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return crud_post.create_post_db(post, db)


@router.get("/all", response_model=list[PostDB])
def get_all_posts(db: Session = Depends(get_db)):
    return crud_post.get_all_posts_db(db)


@router.delete("/{post_id}")
def remove_post_by_id(post_id: int, db: Session = Depends(get_db)):
    # post = crud_post.delete_post_by_id_db(post_id, db)
    # if not topic:
    #     raise HTTPException(status_code=404, detail="Topic not found, cannot delete")
    return crud_post.delete_post_by_id_db(post_id, db)


@router.patch("/{post_id}")
def remove_post_by_id(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    # post = crud_post.delete_post_by_id_db(post_id, db)
    # if not topic:
    #     raise HTTPException(status_code=404, detail="Topic not found, cannot delete")
    return crud_post.update_post_by_id(post_id, post_update, db)

# @router.get("/{topic_id}", response_model=TopicDB)
# def get_topic_by_id(topic_id: int, db: Session = Depends(get_db)):
#     topic = crud_post.get_by_topic_id_db(topic_id, db)
#     if not topic:
#         raise HTTPException(status_code=404, detail="Topic not found")
#     return crud_post.get_by_topic_id_db(topic_id, db)

#
# @router.patch("/{topic_id}")
# def patch_topic_by_id(topic_id: int, topic_update: TopicUpdate, db: Session = Depends(get_db)):
#     topic = crud_post.get_by_topic_id_db(topic_id, db)
#     topic_updated = crud_post.get_by_topic_id_db(topic_update.id, db)
#     if topic_updated:
#         raise HTTPException(status_code=409, detail="This ID already exists")
#     if not topic:
#         raise HTTPException(status_code=404, detail="Topic not found, cannot patch")
#     return crud_post.update_topic_by_id(topic_id, topic_update, db)
