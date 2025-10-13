from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import TypedDict
from sqlmodel import Field, SQLModel, Session, create_engine, select

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur FastAPI!"}