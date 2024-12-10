from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from repo_tool.core.digest import generate_digest_content
from repo_tool.core.filter import filter_files_in_repo
from repo_tool.core.github import GitHub, Repository
from repo_tool.core.summary import Summary, generate_summary

app = FastAPI()

load_dotenv()

github = GitHub()


class Response(BaseModel):
    status: str


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


class DeleteRequest(BaseModel):
    url: Optional[str] = None


@app.delete("/repositories", response_model=Response)
def delete_repository(request: DeleteRequest) -> Response:
    if request.url:
        github.remove(request.url)
    else:
        github.clean()
    return Response(status="success")


class UpdateRequest(BaseModel):
    url: Optional[str] = None
    branch: Optional[str] = None


@app.put("/repositories", response_model=Response)
def update_repository(request: UpdateRequest) -> Response:
    if request.url:
        if not github.repo_exists(request.url):
            raise HTTPException(
                status_code=404, detail="Repository not found"
            )  # noqa: F821
        github.update(request.url)
    else:
        github.update()
    return Response(status="success")


class DigestRequest(BaseModel):
    url: str
    prompt: Optional[str] = None


@app.post("/summary", response_model=Summary)
def get_summary_by_repository(request: DigestRequest) -> Summary:
    repo_path = GitHub.get_repo_path(request.url)
    filtered_files = filter_files_in_repo(repo_path, request.prompt)
    summary = generate_summary(repo_path, filtered_files)
    return summary


@app.post("/digest", response_model=str)
def get_digest_by_repository(request: DigestRequest) -> str:
    repo_path = GitHub.get_repo_path(request.url)
    filtered_files = filter_files_in_repo(repo_path, request.prompt)
    digest = generate_digest_content(repo_path, filtered_files)
    return digest
