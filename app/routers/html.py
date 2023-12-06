import os

from fastapi import APIRouter, HTTPException
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.crud import forum, topic, post
from app.dependencies import get_db
from app.schemas.exception import ExceptionHandler

router = APIRouter(dependencies=[Depends(get_db)], tags=["Html"])

current_dir = os.path.abspath(os.path.dirname(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, '../templates'))


@router.get("/", response_class=HTMLResponse)
def get_html_index(request: Request, db: Session = Depends(get_db)):
    forums = forum.get_all_forums_db(db)
    if not forums:
        raise ExceptionHandler(status_code=404, detail="There are no forums", headers={"error_place": "forum"})
    return templates.TemplateResponse("index.html", {"request": request, "forums": forums})


@router.get("/add", response_class=HTMLResponse)
def get_html_create_forum(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("forum_add.html", {"request": request})


@router.get("/forum/{forum_id}", response_class=HTMLResponse)
def get_html_forum_by_id(request: Request, forum_id: int, db: Session = Depends(get_db)):
    forum_db = forum.get_forum_by_id_db(forum_id, db)
    if not forum_db:
        raise ExceptionHandler(status_code=404, detail="Forum not found")
    return templates.TemplateResponse("forum.html", {"request": request, "forum": forum_db})


@router.get("/forum/{forum_id}/add", response_class=HTMLResponse)
def get_html_create_topic(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("topic_add.html", {"request": request})


@router.get("/edit/{forum_id}", response_class=HTMLResponse)
def get_html_patch_forum(request: Request, forum_id: int, db: Session = Depends(get_db)):
    forum_db = forum.get_forum_by_id_db(forum_id, db)
    return templates.TemplateResponse("forum_edit.html", {"request": request, "forum": forum_db})


@router.get("/topic/{topic_id}/edit", response_class=HTMLResponse)
def get_html_patch_topic(request: Request, topic_id: int, db: Session = Depends(get_db)):
    topic_db = topic.get_by_topic_id_db(topic_id, db)
    forum_db = forum.get_all_forums_db(db)
    return templates.TemplateResponse("topic_edit.html", {"request": request, "topic": topic_db, "forums": forum_db})


@router.get("/topic/{topic_id}", response_class=HTMLResponse)
def get_html_topic_by_id(request: Request, topic_id: int, db: Session = Depends(get_db)):
    topic_db = topic.get_by_topic_id_db(topic_id, db)
    return templates.TemplateResponse("topic.html", {"request": request, "topic": topic_db})


@router.get("/topic/{topic_id}/add", response_class=HTMLResponse)
def get_html_create_post(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("post_add.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
def get_html_login(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def get_html_register(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/post/{post_id}", response_class=HTMLResponse)
def get_html_patch_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post_db = post.get_by_post_id_db(post_id, db)
    return templates.TemplateResponse("post_edit.html", {"request": request, "post": post_db})


def exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "exception": exc})
