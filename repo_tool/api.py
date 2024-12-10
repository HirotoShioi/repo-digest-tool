from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from repo_tool.core.github import GitHub, Repository

app = FastAPI()

load_dotenv()

github = GitHub()


@app.get("/repositories")
def get_repositories() -> List[Repository]:
    return github.list()


@app.get("/repositories/{author}/{repository_name}")
def get_repository(author: str, repository_name: str) -> Repository:
    return github.get(author, repository_name)


class CloneRequest(BaseModel):
    url: str
    branch: Optional[str] = None


# bodyの中にURLを受け取る
@app.post("/repositories", response_model=Optional[Repository])
def clone_repository(request: CloneRequest) -> Optional[Repository]:
    result = github.clone(request.url, request.branch)
    if result is None:
        return github.getByUrl(request.url)
    return result


@app.get("/digest")
def get_digest() -> str:
    return "digest"
