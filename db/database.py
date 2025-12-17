from sqlmodel import SQLModel, create_engine, Session
from core.config import DATABASE_URL
from .base import import_models

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
