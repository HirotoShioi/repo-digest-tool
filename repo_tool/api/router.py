from typing import List, Optional

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field

from repo_tool.core.digest import generate_digest_content
from repo_tool.core.filter import filter_files_in_repo
from repo_tool.core.github import GitHub, Repository
from repo_tool.core.summary import Summary, generate_summary

router = APIRouter()

load_dotenv(override=True)

github = GitHub()


class Response(BaseModel):
    status: str = Field(..., description="The status of the operation")


@router.get("/repositories")
def get_repositories() -> List[Repository]:
    return github.list()


@router.get("/repositories/{author}/{repository_name}")
def get_repository(author: str, repository_name: str) -> Repository:
    return github.get(author, repository_name)


class CloneRequest(BaseModel):
    url: str = Field(..., description="The URL of the repository to clone")
    branch: Optional[str] = Field(
        None, description="The branch to clone (default: main)"
    )


# bodyの中にURLを受け取る
@router.post("/repositories", response_model=Optional[Repository])
def clone_repository(request: CloneRequest) -> Optional[Repository]:
    result = github.clone(request.url, request.branch)
    if result is None:
        return github.getByUrl(request.url)
    return result


class DeleteRequest(BaseModel):
    url: Optional[str] = Field(None, description="The URL of the repository to delete")


@router.delete("/repositories", response_model=Response)
def delete_repository(request: DeleteRequest) -> Response:
    if request.url:
        github.remove(request.url)
    else:
        github.clean()
    return Response(status="success")


class UpdateRequest(BaseModel):
    url: Optional[str] = Field(None, description="The URL of the repository to update")
    branch: Optional[str] = Field(
        None, description="The branch to update (default: main)"
    )


@router.put("/repositories", response_model=Response)
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


@router.post("/summary", response_model=Summary)
def get_summary_of_repository(request: DigestRequest) -> Summary:
    if not github.repo_exists(request.url):
        raise HTTPException(status_code=404, detail="Repository not found")
    repo_path = GitHub.get_repo_path(request.url)
    filtered_files = filter_files_in_repo(repo_path, request.prompt)
    summary = generate_summary(repo_path, filtered_files)
    return summary


@router.post("/digest", response_model=str)
def get_digest_of_repository(request: DigestRequest) -> str:
    repo_path = GitHub.get_repo_path(request.url)
    filtered_files = filter_files_in_repo(repo_path, request.prompt)
    digest = generate_digest_content(repo_path, filtered_files)
    return digest
