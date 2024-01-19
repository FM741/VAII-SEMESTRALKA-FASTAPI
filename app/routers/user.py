from typing import Annotated

from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.crud import user as crud_user
from app.dependencies import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserDB, UserCreate, UserBase, UserUpdate

router = APIRouter(dependencies=[Depends(get_db)], tags=["User"],
                   prefix="/crud/user")


@router.get("/all", response_model=list[UserDB])
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users_db(db)


@router.post("/add", response_model=UserDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_conflict = crud_user.get_user_by_username(user.username, db)
    if user_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already exists"
        )
    return crud_user.create_user_db(user, db)


@router.get("/me", response_model=UserBase)
def get_me_user(current_user: Annotated[UserDB, Security(get_current_user, scopes=["user", "admin"])]):
    return current_user


@router.patch("/{user_id}")
def patch_topic_by_id(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = crud_user.get_by_user_id_db(user_id, db)
    user_updated = crud_user.get_by_user_id_db(user_update.id, db)
    if user_updated:
        raise HTTPException(status_code=409, detail="This ID already exists")
    if not user:
        raise HTTPException(status_code=404, detail="Topic not found, cannot patch")
    return crud_user.update_user_by_id(user_id, user_update, db)
