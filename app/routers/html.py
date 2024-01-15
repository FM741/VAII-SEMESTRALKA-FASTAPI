import os
from typing import Annotated

from fastapi import APIRouter, HTTPException, Security
from fastapi import Request, Depends
from fastapi.security import SecurityScopes
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud import forum, topic, post
from app.dependencies import get_db
from app.routers.auth import get_current_user
from app.schemas.exception import ExceptionHandler
from app.schemas.user import UserBase, UserDB

router = APIRouter(dependencies=[Depends(get_db)], tags=["Html"])

current_dir = os.path.abspath(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, '../templates'))


@router.get("/", response_class=HTMLResponse)
def get_html_index(request: Request, current_user: Annotated[UserDB, Security(get_current_user, scopes=["guest"])], db: Session = Depends(get_db)):
    forums = forum.get_all_forums_db(db)
    if not forums:
        raise ExceptionHandler(status_code=404, detail="There are no forums", headers={"error_place": "forum"})
    return templates.TemplateResponse("index.html", {"request": request, "forums": forums, "user": current_user})


@router.get("/add", response_class=HTMLResponse)
def get_html_create_forum(request: Request, current_user: Annotated[UserDB, Security(get_current_user, scopes=["admin"])], db: Session = Depends(get_db)):
    return templates.TemplateResponse("forum_add.html", {"request": request, "user": current_user})


@router.get("/forum/{forum_id}", response_class=HTMLResponse)
def get_html_forum_by_id(request: Request,  forum_id: int, current_user: Annotated[UserDB, Security(get_current_user, scopes=["guest"])], db: Session = Depends(get_db)):
    forum_db = forum.get_forum_by_id_db(forum_id, db)
    if not forum_db:
        raise ExceptionHandler(status_code=404, detail="Forum not found")
    return templates.TemplateResponse("forum.html", {"request": request, "forum": forum_db, "user": current_user})


@router.get("/forum/{forum_id}/add", response_class=HTMLResponse)
def get_html_create_topic(request: Request, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])], db: Session = Depends(get_db)):
    return templates.TemplateResponse("topic_add.html", {"request": request, "user": current_user})


@router.get("/edit/{forum_id}", response_class=HTMLResponse)
def get_html_patch_forum(request: Request, forum_id: int, current_user: Annotated[UserDB, Security(get_current_user, scopes=["admin"])], db: Session = Depends(get_db)):
    forum_db = forum.get_forum_by_id_db(forum_id, db)
    return templates.TemplateResponse("forum_edit.html", {"request": request, "forum": forum_db, "user": current_user})


@router.get("/topic/{topic_id}/edit", response_class=HTMLResponse)
def get_html_patch_topic(request: Request, topic_id: int, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])], db: Session = Depends(get_db)):
    topic_db = topic.get_by_topic_id_db(topic_id, db)
    forum_db = forum.get_all_forums_db(db)
    return templates.TemplateResponse("topic_edit.html", {"request": request, "topic": topic_db, "forums": forum_db, "user": current_user})


@router.get("/topic/{topic_id}", response_class=HTMLResponse)
def get_html_topic_by_id(request: Request, topic_id: int, current_user: Annotated[UserDB, Security(get_current_user, scopes=["guest"])], db: Session = Depends(get_db)):
    topic_db = topic.get_by_topic_id_db(topic_id, db)
    return templates.TemplateResponse("topic.html", {"request": request, "topic": topic_db, "user": current_user})


@router.get("/topic/{topic_id}/add", response_class=HTMLResponse)
def get_html_create_post(request: Request, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])], db: Session = Depends(get_db)):
    return templates.TemplateResponse("post_add.html", {"request": request, "user": current_user})


@router.get("/login", response_class=HTMLResponse)
def get_html_login(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def get_html_register(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/post/{post_id}", response_class=HTMLResponse)
def get_html_patch_post(request: Request, post_id: int, current_user: Annotated[UserDB, Security(get_current_user, scopes=["user"])], db: Session = Depends(get_db)):
    post_db = post.get_by_post_id_db(post_id, db)
    return templates.TemplateResponse("post_edit.html", {"request": request, "post": post_db, "user": current_user})


def exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "exception": exc})
