from fastapi import FastAPI

from repo_tool.api.router import router

app = FastAPI()

app.include_router(router)
