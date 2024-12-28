import os
import tempfile
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel, Field
from sqlmodel import Session

from repo_tool.api.database import get_session
from repo_tool.api.repositories import (
    FilterSettingsRepository,
    SummaryCacheRepository,
)
from repo_tool.core.digest import (
    RespositoryContent,
    generate_digest_content,
    generate_repository_content,
)
from repo_tool.core.filter import filter_files_in_repo, get_filter_settings_from_env
from repo_tool.core.github import GitHub, Repository
from repo_tool.core.llm import filter_files_with_llm
from repo_tool.core.summary import Summary, generate_summary

router = APIRouter()

load_dotenv(override=True)


class Repositories:
    def __init__(self, session: Session):
        self.session = session
        self.summary_cache_repo = SummaryCacheRepository(session)
        self.filter_settings_repo = FilterSettingsRepository(session)


def get_github() -> GitHub:
    return GitHub()


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
    if not github.repo_exists(f"{author}/{repository_name}"):
        raise HTTPException(status_code=404, detail="Repository not found")
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
        raise HTTPException(status_code=400, detail=str(e))
    return Response(status="success")


@router.delete(
    "/repositories",
    response_model=Response,
    summary="Delete all repositories",
    description="Delete all repositories",
)
def delete_all_repositories(
    session: Session = Depends(get_session), github: GitHub = Depends(get_github)
) -> Response:
    github.clean()
    repositories = Repositories(session)
    filter_settings_repo = repositories.filter_settings_repo
    summary_cache_repo = repositories.summary_cache_repo

    filter_settings_repo.delete_all()
    summary_cache_repo.delete_all()
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
    session: Session = Depends(get_session),
    github: GitHub = Depends(get_github),
) -> Response:
    if not github.repo_exists(f"{author}/{repository_name}"):
        raise HTTPException(status_code=404, detail="Repository not found")
    github.remove(f"{author}/{repository_name}")
    repositories = Repositories(session)
    filter_settings_repo = repositories.filter_settings_repo
    summary_cache_repo = repositories.summary_cache_repo

    filter_settings_repo.delete_by_repository_id(f"{author}/{repository_name}")
    summary_cache_repo.delete_by_repository_id(f"{author}/{repository_name}")
    return Response(status="success")


@router.put(
    "/repositories",
    response_model=Response,
    summary="Update all repositories",
    description="Update all repositories",
)
def update_all_repositories(
    session: Session = Depends(get_session), github: GitHub = Depends(get_github)
) -> Response:
    github.update()
    repositories = Repositories(session)
    summary_cache_repo = repositories.summary_cache_repo
    summary_cache_repo.delete_all()
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
    session: Session = Depends(get_session),
    github: GitHub = Depends(get_github),
) -> Response:
    if not github.repo_exists(f"{author}/{repository_name}"):
        raise HTTPException(status_code=404, detail="Repository not found")
    github.update(f"{author}/{repository_name}")
    repositories = Repositories(session)
    summary_cache_repo = repositories.summary_cache_repo
    summary_cache_repo.delete_by_repository_id(f"{author}/{repository_name}")
    return Response(status="success")


@router.get(
    "/repositories/{author}/{repository_name}/summary",
    response_model=Summary,
    summary="Get a summary of a repository digest",
    description="Get a summary of a repository digest",
)
def get_summary_of_repository(
    author: str,
    repository_name: str,
    session: Session = Depends(get_session),
    github: GitHub = Depends(get_github),
) -> Summary:
    url = f"{author}/{repository_name}"
    if not github.repo_exists(url):
        raise HTTPException(status_code=404, detail="Repository not found")

    repositories = Repositories(session)
    summary_cache_repo = repositories.summary_cache_repo
    filter_settings_repo = repositories.filter_settings_repo

    maybe_cached_summary = summary_cache_repo.get_by_repository_id(url)
    if maybe_cached_summary:
        return maybe_cached_summary

    repo_info = github.get_repo_info(url)
    filter_settings = filter_settings_repo.get_by_repository_id(url)
    filtered_files = filter_files_in_repo(
        repo_info.path, filter_settings=filter_settings
    )
    summary = generate_summary(repo_info, filtered_files)
    summary_cache_repo.upsert(summary, datetime.now().isoformat())
    return summary


class GenerateDigestParams(BaseModel):
    url: str = Field(..., description="The URL of the repository to create a digest")


@router.post(
    "/digest",
    response_class=FileResponse,
    summary="Create a digest of a repository",
    description="Create a digest of a repository. This will create a digest of the repository and return it as a file.",
)
def generate_digest(
    request: GenerateDigestParams,
    session: Session = Depends(get_session),
    github: GitHub = Depends(get_github),
) -> FileResponse:
    repo_info = github.get_repo_info(request.url)
    repositories = Repositories(session)
    filter_settings_repo = repositories.filter_settings_repo
    filter_settings = filter_settings_repo.get_by_repository_id(repo_info.id)
    filtered_files = filter_files_in_repo(
        repo_info.path, filter_settings=filter_settings
    )
    digest = generate_digest_content(repo_info.path, filtered_files)

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


@router.get(
    "/repositories/{author}/{repository_name}/digest",
    response_model=RespositoryContent,
    summary="Get a digest of a repository",
    description="Get a digest of a repository",
)
def get_digest_of_repository(
    author: str,
    repository_name: str,
    session: Session = Depends(get_session),
    github: GitHub = Depends(get_github),
) -> RespositoryContent:
    repo_info = github.get_repo_info(f"{author}/{repository_name}")
    repositories = Repositories(session)
    filter_settings_repo = repositories.filter_settings_repo
    filter_settings = filter_settings_repo.get_by_repository_id(repo_info.id)
    filtered_files = filter_files_in_repo(
        repo_info.path, filter_settings=filter_settings
    )
    digest = generate_repository_content(repo_info, filtered_files)
    return digest


class Settings(BaseModel):
    include_files: List[str] = Field(
        ..., description="The files to include in the digest"
    )
    exclude_files: List[str] = Field(
        ..., description="The files to exclude from the digest"
    )
    max_tokens: int = Field(
        ..., description="The maximum tokens to include in the digest"
    )


@router.get("/settings")
def get_settings() -> Settings:
    settings = get_filter_settings_from_env()
    return Settings(
        include_files=settings.exclude_patterns,
        exclude_files=settings.include_patterns,
        max_tokens=settings.max_tokens,
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
        max_tokens=request.max_tokens,
    )


@router.get("/repositories/{author}/{repository_name}/settings")
def get_settings_of_repository(
    author: str, repository_name: str, session: Session = Depends(get_session)
) -> Settings:
    filter_settings_repo = FilterSettingsRepository(session)
    maybe_settings = filter_settings_repo.get_by_repository_id(
        f"{author}/{repository_name}"
    )
    if maybe_settings:
        return Settings(
            include_files=maybe_settings.include_patterns,
            exclude_files=maybe_settings.exclude_patterns,
            max_tokens=maybe_settings.max_tokens,
        )
    default_settings = get_filter_settings_from_env()
    return Settings(
        include_files=default_settings.include_patterns,
        exclude_files=default_settings.exclude_patterns,
        max_tokens=default_settings.max_tokens,
    )


@router.put("/repositories/{author}/{repository_name}/settings")
def update_settings_of_repository(
    author: str,
    repository_name: str,
    request: Settings,
    session: Session = Depends(get_session),
) -> Settings:
    repositories = Repositories(session)
    summary_cache_repo = repositories.summary_cache_repo
    filter_settings_repo = repositories.filter_settings_repo

    summary_cache_repo.delete_by_repository_id(f"{author}/{repository_name}")
    filter_settings_repo.upsert(
        f"{author}/{repository_name}",
        request.include_files,
        request.exclude_files,
        request.max_tokens,
    )
    return request


class AiFilterParams(BaseModel):
    prompt: str = Field(..., description="The prompt to filter the files")


@router.post("/repositories/{author}/{repository_name}/filter/ai")
def get_ai_filter_of_repository(
    author: str,
    repository_name: str,
    request: AiFilterParams,
    session: Session = Depends(get_session),
    github: GitHub = Depends(get_github),
) -> Settings:
    if not github.repo_exists(f"{author}/{repository_name}"):
        raise HTTPException(status_code=404, detail="Repository not found")
    repo_info = github.get_repo_info(f"{author}/{repository_name}")
    repositories = Repositories(session)
    summary_cache_repo = repositories.summary_cache_repo
    filter_settings_repo = repositories.filter_settings_repo
    filter_settings = filter_settings_repo.get_by_repository_id(
        f"{author}/{repository_name}"
    )
    if not filter_settings:
        filter_settings = get_filter_settings_from_env()
    filtered_files = filter_files_in_repo(
        repo_info.path,
        filter_settings=filter_settings,
    )
    include_patterns = filter_files_with_llm(filtered_files, request.prompt)
    include_patterns_str = [
        str(pattern.relative_to(repo_info.path)) for pattern in include_patterns
    ]
    all_include_patterns = set(filter_settings.include_patterns + include_patterns_str)
    filter_settings_repo.upsert(
        f"{author}/{repository_name}",
        include_patterns=list(all_include_patterns),
        exclude_patterns=filter_settings.exclude_patterns,
        max_tokens=filter_settings.max_tokens,
    )
    summary_cache_repo.delete_by_repository_id(f"{author}/{repository_name}")
    return Settings(
        include_files=list(all_include_patterns),
        exclude_files=filter_settings.exclude_patterns,
        max_tokens=filter_settings.max_tokens,
    )
