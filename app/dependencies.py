from fastapi.security import OAuth2PasswordBearer

from app.core.db import SessionLocal

auth_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes={"user": "Regular user",
                                                             "admin": "User with elevated rights"})


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
