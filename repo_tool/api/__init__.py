from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(router)
