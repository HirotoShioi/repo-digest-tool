from fastapi import FastAPI

from repo_tool.api.router import router

app = FastAPI(title="Repo Tool API", version="1.0.0")

app.include_router(router)
