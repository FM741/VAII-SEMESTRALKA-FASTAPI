from typing import Annotated

from fastapi import APIRouter, Security, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud import post as crud_post
from app.dependencies import get_db, auth_scheme
from app.routers.auth import get_current_user
from app.schemas.post import PostCreate, PostDB, PostUpdate
from app.schemas.user import UserDB

router = APIRouter(dependencies=[Depends(get_db), Security(get_current_user, scopes=["user"])], tags=["Post"],
                   prefix="/crud/post")


@router.post("/add", response_model=PostDB)
def create_post(post: PostCreate, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])],
                db: Session = Depends(get_db)):
    return crud_post.create_post_db(post, current_user.id, db)


@router.get("/all", response_model=list[PostDB])
def get_all_posts(db: Session = Depends(get_db)):
    return crud_post.get_all_posts_db(db)


@router.delete("/{post_id}")
def remove_post_by_id(post_id: int, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])],
                      db: Session = Depends(get_db)):
    post = crud_post.get_by_post_id_db(post_id, db)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found, cannot delete")
    if current_user.is_admin:
        return crud_post.delete_post_by_id_db(post_id, db)
    if current_user.id != post.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized!")
    return crud_post.delete_post_by_id_db(post_id, db)


@router.patch("/{post_id}")
def remove_post_by_id(post_id: int, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])],
                      post_update: PostUpdate, db: Session = Depends(get_db)):
    post = crud_post.get_by_post_id_db(post_id, db)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found, cannot edit")
    if current_user.is_admin:
        return crud_post.update_post_by_id(post_id, post_update, db)
    if current_user.id != post.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized!")
    return crud_post.update_post_by_id(post_id, post_update, db)
