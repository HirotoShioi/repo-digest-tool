from contextlib import asynccontextmanager
from typing import AsyncGenerator

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


@asynccontextmanager  # noqa: B902
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    engine = create_engine("sqlite:///repo_tool.db")
    SQLModel.metadata.create_all(engine)
    yield
    engine.dispose()


app.include_router(router)
