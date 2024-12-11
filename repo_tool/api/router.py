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


@router.get(
    "/repositories",
    summary="Get all repositories",
    description="Get all repositories",
)
def get_repositories() -> List[Repository]:
    return github.list()


@router.get(
    "/repositories/{author}/{repository_name}",
    summary="Get a repository",
    description="Get a repository",
)
def get_repository(author: str, repository_name: str) -> Repository:
    return github.get(author, repository_name)


class CloneRepositoryParams(BaseModel):
    url: str = Field(..., description="The URL of the repository to clone")
    branch: Optional[str] = Field(
        None, description="The branch to clone (default: main)"
    )


# bodyの中にURLを受け取る
@router.post(
    "/repositories",
    response_model=Optional[Repository],
    summary="Clone a repository",
    description="Clone a repository",
)
def clone_repository(request: CloneRepositoryParams) -> Optional[Repository]:
    result = github.clone(request.url, request.branch)
    if result is None:
        return github.getByUrl(request.url)
    return result


class DeleteRepositoryParams(BaseModel):
    url: Optional[str] = Field(None, description="The URL of the repository to delete")


@router.delete(
    "/repositories",
    response_model=Response,
    summary="Delete a repository",
    description="Delete a repository. If the URL is not provided, all repositories will be deleted.",
)
def delete_repository(request: DeleteRepositoryParams) -> Response:
    if request.url:
        github.remove(request.url)
    else:
        github.clean()
    return Response(status="success")


class UpdateRepositoryParams(BaseModel):
    url: Optional[str] = Field(None, description="The URL of the repository to update")
    branch: Optional[str] = Field(
        None, description="The branch to update (default: main)"
    )


@router.put(
    "/repositories",
    response_model=Response,
    summary="Update a repository",
    description="Update a repository. If the URL is not provided, all repositories will be updated.",
)
def update_repository(request: UpdateRepositoryParams) -> Response:
    if request.url:
        if not github.repo_exists(request.url):
            raise HTTPException(
                status_code=404, detail="Repository not found"
            )  # noqa: F821
        github.update(request.url)
    else:
        github.update()
    return Response(status="success")


class CreateSummaryParams(BaseModel):
    url: str = Field(..., description="The URL of the repository to create a summary")
    prompt: Optional[str] = Field(None, description="The prompt to create a summary")


@router.post(
    "/summary",
    response_model=Summary,
    summary="Create a summary of a repository",
    description="Create a summary of a repository",
)
def get_summary_of_repository(request: CreateSummaryParams) -> Summary:
    if not github.repo_exists(request.url):
        raise HTTPException(status_code=404, detail="Repository not found")
    repo_path = GitHub.get_repo_path(request.url)
    filtered_files = filter_files_in_repo(repo_path, request.prompt)
    summary = generate_summary(repo_path, filtered_files)
    return summary


class CreateDigestParams(BaseModel):
    url: str = Field(..., description="The URL of the repository to create a digest")
    prompt: Optional[str] = Field(None, description="The prompt to create a digest")
    branch: Optional[str] = Field(None, description="The branch to generate digest for")


@router.post("/digest", response_model=str)
def get_digest_of_repository(request: CreateDigestParams) -> str:
    repo_path = GitHub.get_repo_path(request.url)
    if not github.repo_exists(request.url):
        github.clone(request.url, request.branch)
    elif request.branch:
        github.checkout(repo_path, request.branch)
    filtered_files = filter_files_in_repo(repo_path, request.prompt)
    digest = generate_digest_content(repo_path, filtered_files)
    return digest
