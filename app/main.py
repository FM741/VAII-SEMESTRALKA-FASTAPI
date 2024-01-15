import os
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.core.db import engine
from app.crud import user as crud_user
from .dependencies import get_db
from .models import models
from .routers import topic, forum, html, post, user, auth
from .schemas.exception import ExceptionHandler
from .schemas.user import UserDB

models.Base.metadata.create_all(engine)

app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(topic.router, dependencies=[Depends(get_db)])
app.include_router(forum.router, dependencies=[Depends(get_db)])
app.include_router(post.router, dependencies=[Depends(get_db)])
app.include_router(user.router, dependencies=[Depends(get_db)])
app.include_router(html.router, dependencies=[Depends(get_db)])
app.include_router(auth.router, dependencies=[Depends(get_db)])


current_dir = os.path.abspath(os.path.dirname(__file__))
app.mount('/static', StaticFiles(directory=os.path.join(current_dir, 'static')), name='static')
app.add_exception_handler(ExceptionHandler, html.exception_handler)
