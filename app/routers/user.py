from typing import Annotated

from fastapi import APIRouter, Depends, Security, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from app.crud import user as crud_user
from app.dependencies import get_db
from app.routers.auth import get_current_user
from app.schemas.exception import ExceptionHandler
from app.schemas.user import UserDB, UserCreate, UserBase, UserUpdate, UserAll

router = APIRouter(dependencies=[Depends(get_db)], tags=["User"],
                   prefix="/crud/user")


@router.get("/all", response_model=list[UserDB])
def get_all_users(current_user: Annotated[UserDB, Security(get_current_user, scopes=["admin"])],
                  db: Session = Depends(get_db)):
    return crud_user.get_all_users_db(db)


@router.post("/add", response_model=UserDB)
def create_user(user: UserCreate, current_user: Annotated[UserDB, Security(get_current_user, scopes=["guest"])],
                db: Session = Depends(get_db)):
    user_conflict = crud_user.get_user_by_username_db(user.username, db)
    if user_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already exists"
        )
    return crud_user.create_user_db(user, db)


@router.get("/me", response_model=UserBase)
def get_me_user(current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])]):
    return current_user


@router.get("/{username}", response_model=UserAll)
def get_user_by_username(username: str,
                         current_user: Annotated[UserDB, Security(get_current_user, scopes=["user", "admin"])],
                         db: Session = Depends(get_db)):
    user = crud_user.get_user_by_username_db(username, db)
    if not user:
        raise ExceptionHandler(status_code=404, detail="Specified user does not exist")
    return user


@router.patch("/edit")
def patch_user_by_id(current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])],
                     user_update: UserUpdate, db: Session = Depends(get_db)):
    user_conflict = crud_user.get_user_by_username_db(user_update.username, db)
    if user_conflict:
        raise HTTPException(status_code=409, detail="Username already exists!!")
    return crud_user.update_user_by_id(current_user.id, user_update, db)


@router.post("/uploadimage/")
def create_upload_file(current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])], file: UploadFile,
                       db: Session = Depends(get_db)):
    if file.content_type == "image/jpeg" or file.content_type == "image/png":
        return crud_user.save_image(current_user.id, file, db)
    raise HTTPException(status_code=409, detail="The selected file is not supported!")
