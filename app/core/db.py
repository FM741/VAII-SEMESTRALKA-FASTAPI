from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://postgres:postgres@db:5432/PostgresDB", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
