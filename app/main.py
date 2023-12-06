import os

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from app.core.db import engine
from .dependencies import get_db
from .models import models
from .routers import topic, forum, html, post
from .schemas.exception import ExceptionHandler

models.Base.metadata.create_all(engine)

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(topic.router, dependencies=[Depends(get_db)])
app.include_router(forum.router, dependencies=[Depends(get_db)])
app.include_router(post.router, dependencies=[Depends(get_db)])
app.include_router(html.router, dependencies=[Depends(get_db)])

current_dir = os.path.abspath(os.path.dirname(__file__))
app.mount('/static', StaticFiles(directory=os.path.join(current_dir, 'static')), name='static')
app.add_exception_handler(ExceptionHandler, html.exception_handler)
# @app.post("/forum/add", response_model=ForumBase)
# def create_forum_item(forum: ForumBase, db: Session = Depends(get_db)):
#     db_forum = models.Forum(name=forum.name)
#     db.add(db_forum)
#     db.commit()
#     db.refresh(db_forum)
#     return db_forum
#
#
# @app.get("/forums", response_model=list[ForumBase])
# def get_forums(db: Session = Depends(get_db)):
#     sau = select(models.Forum)
#     forums = db.scalars(sau).all()
#     return forums
#
#

#
#
# @app.get("/login", response_class=HTMLResponse)
# async def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})
#
#
# @app.exception_handler(404)
# async def custom_404_handler(_, __):
#     return RedirectResponse("/")
#
#
# @app.get("/db", response_model=Forum)
# async def get_users():
#     forum = await Forum(id=40, name="Science").save()
#     topic = Topic(id=10, name="Math", forum=forum)
#     return forum
#
#
# @app.get("/dbF")
# async def get_forums():
#     forum = await Forum.objects.all()
#     return forum
#
#
# @app.on_event("startup")
# async def startup():
#     if not database.is_connected:
#         await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     if database.is_connected:
#         await database.disconnect()
