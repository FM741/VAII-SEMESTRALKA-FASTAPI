from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.dependencies import get_db
from app.routers.auth import get_current_user
from app.schemas.user import UserDB, UserCreate, UserBase

router = APIRouter(dependencies=[Depends(get_db)], tags=["User"], prefix="/crud/user")


@router.get("/all", response_model=list[UserDB])
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users_db(db)


@router.post("/add", response_model=UserDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user_db(user, db)


@router.get("/me", response_model=UserBase)
def get_me_user(current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])]):
    return current_user
