import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel

from repo_tool.api.router import get_github, router
from repo_tool.core.github import GitHub, Repository


class InMemoryGitHub(GitHub):
    def __init__(self) -> None:
        self.repositories: Dict[str, Repository] = {}

    def clone(
        self, repo_url: str, branch: Optional[str] = None, force: bool = False
    ) -> Repository:
        # Extract author and repo_name from URL
        author, repo_name = repo_url.split("/")[-2:]
        repository_id = f"{author}/{repo_name}"

        # Use repository_id as key instead of full URL
        if force or repository_id not in self.repositories:
            repository = Repository(
                id=repository_id,
                url=repo_url,
                branch=branch,
                path=Path(f"/tmp/{author}/{repo_name}"),
                updated_at=datetime.datetime.now(),
                name=repo_name,
                author=author,
                size=0,
            )
            self.repositories[repository_id] = repository

        return self.repositories[repository_id]

    def list(self) -> List[Repository]:
        return list(self.repositories.values())

    def remove(self, repo_url: str) -> None:
        """Remove repository(ies) from storage.

        Args:
            repo_url: If None or empty string, clear all repositories.
                     Otherwise, remove the specific repository.
        """
        try:
            author, repo_name = repo_url.split("/")[-2:]
            repository_id = f"{author}/{repo_name}"
            if repository_id in self.repositories:
                del self.repositories[repository_id]
        except (ValueError, IndexError):
            pass

    def clean(self) -> None:
        self.repositories.clear()

    def repo_exists(self, repo_url: str) -> bool:
        # Extract author and repo_name from URL
        author, repo_name = repo_url.split("/")[-2:]
        repository_id = f"{author}/{repo_name}"
        return repository_id in self.repositories.keys()

    def update(self, repo_url: Optional[str] = None) -> List[Repository]:
        if repo_url:
            # Extract repository_id from URL
            author, repo_name = repo_url.split("/")[-2:]
            repository_id = f"{author}/{repo_name}"
            if repository_id in self.repositories:
                self.repositories[repository_id].updated_at = datetime.datetime.now()
                return [self.repositories[repository_id]]
            return []
        else:
            for repo in self.repositories.values():
                repo.updated_at = datetime.datetime.now()
            return list(self.repositories.values())


@pytest.fixture(name="engine")
def engine_fixture() -> Generator[Engine, None, None]:
    """Create a new in-memory database for each test."""
    # Initialize the global engine for the database module
    from repo_tool.api.database import init_db

    test_engine = create_engine(
        "sqlite:///file:memdb?mode=memory&cache=shared&uri=true",
        connect_args={"check_same_thread": False},
    )

    # Set the global engine
    init_db("sqlite:///file:memdb?mode=memory&cache=shared&uri=true")

    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="session")
def session_fixture(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine: Engine, github: InMemoryGitHub) -> TestClient:
    """Create a new FastAPI test client with the in-memory database."""
    app = FastAPI()
    app.include_router(router)

    # Only override the GitHub dependency since database is initialized
    app.dependency_overrides[get_github] = lambda: github

    return TestClient(app)


def sort_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a new dictionary sorted by keys"""
    return dict(sorted(d.items()))


@pytest.fixture
def github() -> InMemoryGitHub:
    """Returns a shared InMemoryGitHub instance"""
    return InMemoryGitHub()


@pytest.fixture(autouse=True)
def reset_github(github: InMemoryGitHub) -> Generator[None, None, None]:
    """Reset GitHub state before each test"""
    github.repositories.clear()
    yield


def test_get_repositories_empty(client: TestClient) -> None:
    response = client.get("/repositories")
    assert response.status_code == 200
    assert response.json() == []


def test_repository_lifecycle(client: TestClient, github: InMemoryGitHub) -> None:
    # 1. Clone repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # 2. Get repository list
    response = client.get("/repositories")
    assert response.status_code == 200
    repos = response.json()
    assert len(repos) == 1
    repo = repos[0]
    assert repo["id"] == "HirotoShioi/repo-digest-tool"
    assert repo["name"] == "repo-digest-tool"
    assert repo["author"] == "HirotoShioi"
    assert repo["branch"] == "main"
    assert "updated_at" in repo

    # 3. Get single repository
    response = client.get("/repositories/HirotoShioi/repo-digest-tool")
    assert response.status_code == 200
    repo = response.json()
    assert repo["id"] == "HirotoShioi/repo-digest-tool"

    # 4. Update repository
    response = client.put("/repositories/HirotoShioi/repo-digest-tool")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # 5. Delete repository
    response = client.delete(
        "/repositories/HirotoShioi/repo-digest-tool",
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # 6. Verify repository list is empty after deletion
    response = client.get("/repositories")
    assert response.status_code == 200
    assert response.json() == []


def test_update_repository_not_found(client: TestClient) -> None:
    response = client.put("/repositories/HirotoShioi/repo-digest-tool")
    assert response.status_code == 404
    assert response.json() == {"detail": "Repository not found"}


def test_get_summary_not_found(client: TestClient) -> None:
    response = client.get("/HirotoShioi/repo-digest-tool/summary")
    assert response.status_code == 404
    assert response.json() == {"detail": "Repository not found"}


def test_delete_all_repositories(client: TestClient, github: InMemoryGitHub) -> None:
    # First add a repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Delete all repositories
    response = client.delete("/repositories")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # Verify repository list is empty
    response = client.get("/repositories")
    assert response.status_code == 200
    assert response.json() == []


def test_clone_repository_invalid_url(client: TestClient) -> None:
    """Test cloning with invalid URL format"""
    clone_payload = {
        "url": "invalid-url",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 400


def test_clone_repository_duplicate(client: TestClient) -> None:
    """Test cloning same repository twice without force flag"""
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    # First clone should succeed
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Second clone should return success (idempotent behavior)
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_get_repository_invalid_author_repo(client: TestClient) -> None:
    """Test getting repository with invalid author/repo format"""
    response = client.get("/repositories/invalid-format")
    assert response.status_code == 404


def test_update_all_repositories(client: TestClient) -> None:
    """Test updating all repositories"""
    # Add two repositories
    repos = [
        "https://github.com/HirotoShioi/repo-digest-tool",
        "https://github.com/HirotoShioi/query-cache",
    ]

    for url in repos:
        response = client.post("/repositories", json={"url": url})
        assert response.status_code == 200

    # Update all repositories
    response = client.put("/repositories")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # Verify all repositories were updated
    response = client.get("/repositories")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_nonexistent_repository(client: TestClient) -> None:
    """Test deleting a repository that doesn't exist"""
    response = client.delete("/repositories/nonexistent/repo")
    assert response.status_code == 404
    assert "Repository not found" in response.json()["detail"]


def test_clone_repository_missing_url(client: TestClient) -> None:
    """Test cloning with missing URL"""
    response = client.post("/repositories", json={"branch": "main"})
    assert response.status_code == 422  # FastAPI validation error


def test_get_repository_settings_default(
    client: TestClient, github: InMemoryGitHub
) -> None:
    """Test getting repository settings when no custom settings exist"""
    # First add a repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Get default settings
    response = client.get("/HirotoShioi/repo-digest-tool/settings")
    assert response.status_code == 200
    settings = response.json()

    # Verify default settings structure
    assert "include_files" in settings
    assert "exclude_files" in settings
    assert "max_file_size" in settings
    assert settings["max_file_size"] == 1000000
    assert isinstance(settings["include_files"], list)
    assert isinstance(settings["exclude_files"], list)


def test_update_repository_settings(client: TestClient, github: InMemoryGitHub) -> None:
    """Test updating repository settings"""
    # First add a repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Update settings
    new_settings = {
        "include_files": ["*.py", "*.md"],
        "exclude_files": ["tests/*", "*.pyc"],
        "max_file_size": 500000,
    }
    response = client.put("/HirotoShioi/repo-digest-tool/settings", json=new_settings)
    assert response.status_code == 200
    updated_settings = response.json()
    assert updated_settings == new_settings

    # Verify settings were persisted
    response = client.get("/HirotoShioi/repo-digest-tool/settings")
    assert response.status_code == 200
    persisted_settings = response.json()
    assert persisted_settings == new_settings


def test_get_settings_nonexistent_repository(client: TestClient) -> None:
    """Test getting settings for a repository that doesn't exist"""
    response = client.get("/nonexistent/repo/settings")
    assert response.status_code == 200  # Returns default settings
    settings = response.json()
    assert "include_files" in settings
    assert "exclude_files" in settings
    assert "max_file_size" in settings


def test_update_settings_validation(client: TestClient, github: InMemoryGitHub) -> None:
    """Test settings validation during update"""
    # First add a repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Test with invalid settings structure
    invalid_settings = {
        "include_files": "not_a_list",  # Should be a list
        "exclude_files": ["tests/*"],
        "max_file_size": 500000,
    }
    response = client.put(
        "/HirotoShioi/repo-digest-tool/settings", json=invalid_settings
    )
    assert response.status_code == 422  # Validation error
