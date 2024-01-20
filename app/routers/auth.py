from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, Cookie
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from app.crud import user as crud_user
from ..dependencies import get_db
from ..schemas.exception import ExceptionHandler
from ..schemas.post import PostDB
from ..schemas.token import TokenData, Token
from ..schemas.topic import TopicDB
from ..schemas.user import UserDB, UserAll

SECRET_KEY = "fc9e8a02e0908115305c0bfba8f99b794b7d7200da92ec4ac4cb18a5d418298b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(dependencies=[Depends(get_db)], tags=["Auth"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_username(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(security_scopes: SecurityScopes, access_token: str = Cookie(None),
                     db: Session = Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    exception = ExceptionHandler(status_code=403, detail="Not enough permissions",
                                 headers={"error_place": "permissions"})
    try:
        if access_token is None:
            token_data = TokenData(scopes=["guest"])
        else:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise exception
            token_scopes = payload.get("scopes", [])
            token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise exception
    user = crud_user.get_user_by_username(token_data.username, db)
    if user is None:
        return None
    return UserAll(id=user.id, username=user.username, gender=user.gender, date_of_creation=user.date_of_creation,
                   is_admin=user.is_admin, topics=[TopicDB.model_validate(t) for t in user.topics],
                   posts=[PostDB.model_validate(t) for t in user.posts], img_url=user.img_url)


@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response = None,
                           db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_admin:
        form_data.scopes = ["guest", "user", "admin"]
    else:
        form_data.scopes = ["guest", "user"]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token, max_age=int(access_token_expires.total_seconds()))
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "success"}
