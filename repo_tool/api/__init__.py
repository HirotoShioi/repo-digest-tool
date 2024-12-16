from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlmodel import SQLModel

from repo_tool.api.router import router

app = FastAPI(title="Repo Tool API", version="1.0.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db() -> None:
    engine = create_engine("sqlite:///repo_tool.db")
    SQLModel.metadata.create_all(engine)


init_db()
app.include_router(router)
