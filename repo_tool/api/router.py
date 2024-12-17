import os
import tempfile
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlmodel import Session

from repo_tool.api.repositories import (
    FilterSettingsRepository,
    SummaryCacheRepository,
)
from repo_tool.core.digest import generate_digest_content
from repo_tool.core.filter import filter_files_in_repo, get_filter_settings_from_env
from repo_tool.core.github import GitHub, Repository
from repo_tool.core.summary import Summary, generate_summary

router = APIRouter()

load_dotenv(override=True)


def get_github() -> GitHub:
    return GitHub()


def get_db() -> Session:
    engine = create_engine("sqlite:///repo_tool.db")
    return Session(engine)


def get_summary_cache_repository(session: Session) -> SummaryCacheRepository:
    return SummaryCacheRepository(session)


def get_filter_settings_repository(session: Session) -> FilterSettingsRepository:
    return FilterSettingsRepository(session)


class Response(BaseModel):
    status: str = Field(..., description="The status of the operation")


@router.get(
    "/repositories",
    summary="Get all repositories",
    description="Get all repositories",
)
def get_repositories(github: GitHub = Depends(get_github)) -> List[Repository]:
    return github.list()


@router.get(
    "/repositories/{author}/{repository_name}",
    summary="Get a repository",
    description="Get a repository",
)
def get_repository(
    author: str, repository_name: str, github: GitHub = Depends(get_github)
) -> Repository:
    return github.get(author, repository_name)


class CloneRepositoryParams(BaseModel):
    url: str = Field(..., description="The URL of the repository to clone")
    branch: Optional[str] = Field(None, description="The branch to clone")


@router.post(
    "/repositories",
    response_model=Response,
    summary="Clone a repository",
    description="Clone a repository. If the URL is not provided, all repositories will be cloned.",
)
def clone_repository(
    request: CloneRepositoryParams, github: GitHub = Depends(get_github)
) -> Response:
    try:
        github.clone(request.url, request.branch)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    return Response(status="success")


@router.delete(
    "/repositories",
    response_model=Response,
    summary="Delete all repositories",
    description="Delete all repositories",
)
def delete_all_repositories(
    session: Session = Depends(get_db), github: GitHub = Depends(get_github)
) -> Response:
    github.clean()
    get_filter_settings_repository(session).delete_all()
    get_summary_cache_repository(session).delete_all()
    return Response(status="success")


@router.delete(
    "/repositories/{author}/{repository_name}",
    response_model=Response,
    summary="Delete a repository",
    description="Delete a repository. If the URL is not provided, all repositories will be deleted.",
)
def delete_repository(
    author: str,
    repository_name: str,
    session: Session = Depends(get_db),
    github: GitHub = Depends(get_github),
) -> Response:
    if not github.repo_exists(f"{author}/{repository_name}"):
        raise HTTPException(status_code=404, detail="Repository not found")
    github.remove(f"{author}/{repository_name}")
    get_filter_settings_repository(session).delete_by_repository_id(
        f"{author}/{repository_name}"
    )
    get_summary_cache_repository(session).delete_by_repository_id(
        f"{author}/{repository_name}"
    )
    return Response(status="success")


@router.put(
    "/repositories",
    response_model=Response,
    summary="Update all repositories",
    description="Update all repositories",
)
def update_all_repositories(github: GitHub = Depends(get_github)) -> Response:
    github.update()
    return Response(status="success")


@router.put(
    "/repositories/{author}/{repository_name}",
    response_model=Response,
    summary="Update a repository",
    description="Update a repository. If the URL is not provided, all repositories will be updated.",
)
def update_repository(
    author: str,
    repository_name: str,
    session: Session = Depends(get_db),
    github: GitHub = Depends(get_github),
) -> Response:
    if not github.repo_exists(f"{author}/{repository_name}"):
        raise HTTPException(status_code=404, detail="Repository not found")
    github.update(f"{author}/{repository_name}")
    get_summary_cache_repository(session).delete_by_repository_id(
        f"{author}/{repository_name}"
    )
    return Response(status="success")


@router.get(
    "/{author}/{repository_name}/summary",
    response_model=Summary,
    summary="Get a summary of a repository digest",
    description="Get a summary of a repository digest",
)
def get_summary_of_repository(
    author: str,
    repository_name: str,
    session: Session = Depends(get_db),
    github: GitHub = Depends(get_github),
) -> Summary:
    url = f"{author}/{repository_name}"
    if not github.repo_exists(url):
        raise HTTPException(status_code=404, detail="Repository not found")
    maybe_cached_summary = get_summary_cache_repository(session).get_by_repository_id(
        url
    )
    if maybe_cached_summary:
        return maybe_cached_summary
    repo_path = GitHub.get_repo_path(url)
    filter_settings = get_filter_settings_repository(session).get_by_repository_id(url)
    filtered_files = filter_files_in_repo(repo_path, filter_settings=filter_settings)
    summary = generate_summary(repo_path, filtered_files)
    get_summary_cache_repository(session).upsert(summary, datetime.now().isoformat())
    return summary


class GenerateDigestParams(BaseModel):
    url: str = Field(..., description="The URL of the repository to create a digest")
    branch: Optional[str] = Field(None, description="The branch to generate digest for")


@router.post(
    "/digest",
    response_class=FileResponse,
    summary="Create a digest of a repository",
    description="Create a digest of a repository. This will create a digest of the repository and return it as a file.",
)
def get_digest_of_repository(
    request: GenerateDigestParams, github: GitHub = Depends(get_github)
) -> FileResponse:
    repo_path = GitHub.get_repo_path(request.url)
    if not github.repo_exists(request.url):
        github.clone(request.url, request.branch)
    elif request.branch:
        github.checkout(repo_path, request.branch)

    filtered_files = filter_files_in_repo(repo_path)
    digest = generate_digest_content(repo_path, filtered_files)

    # Create temporary file
    fd, temp_path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as tmp:
            tmp.write(digest)

        # Get repository name for the filename
        repo_name = request.url.rstrip("/").split("/")[-1]
        filename = f"{repo_name}_digest.txt"

        return FileResponse(
            path=temp_path,
            filename=filename,
            media_type="text/plain",
            background=None,  # This ensures the temp file is removed after the response
        )
    except Exception as e:
        os.unlink(temp_path)  # Clean up the temp file in case of error
        raise HTTPException(status_code=500, detail=str(e))


class Settings(BaseModel):
    include_files: List[str] = Field(
        ..., description="The files to include in the digest"
    )
    exclude_files: List[str] = Field(
        ..., description="The files to exclude from the digest"
    )
    max_file_size: int = Field(
        ..., description="The maximum file size to include in the digest"
    )


@router.get("/settings")
def get_settings() -> Settings:
    settings = get_filter_settings_from_env()
    return Settings(
        include_files=settings.exclude_patterns,
        exclude_files=settings.include_patterns,
        max_file_size=1000000,
    )


@router.put("/settings")
def update_settings(request: Settings) -> Settings:
    with open(".gptignore", "w") as f:
        f.write("\n".join(request.exclude_files))
    with open(".gptinclude", "w") as f:
        f.write("\n".join(request.include_files))
    return Settings(
        include_files=request.include_files,
        exclude_files=request.exclude_files,
        max_file_size=request.max_file_size,
    )


@router.get("/{author}/{repository_name}/settings")
def get_settings_of_repository(
    author: str, repository_name: str, session: Session = Depends(get_db)
) -> Settings:
    maybe_settings = get_filter_settings_repository(session).get_by_repository_id(
        f"{author}/{repository_name}"
    )
    if maybe_settings:
        return Settings(
            include_files=maybe_settings.include_patterns,
            exclude_files=maybe_settings.exclude_patterns,
            max_file_size=maybe_settings.max_file_size,
        )
    default_settings = get_filter_settings_from_env()
    return Settings(
        include_files=default_settings.include_patterns,
        exclude_files=default_settings.exclude_patterns,
        max_file_size=1000000,
    )


@router.put("/{author}/{repository_name}/settings")
def update_settings_of_repository(
    author: str,
    repository_name: str,
    request: Settings,
    session: Session = Depends(get_db),
) -> Settings:
    get_summary_cache_repository(session).delete_by_repository_id(
        f"{author}/{repository_name}"
    )
    get_filter_settings_repository(session).upsert(
        f"{author}/{repository_name}",
        request.include_files,
        request.exclude_files,
        request.max_file_size,
    )
    return request
