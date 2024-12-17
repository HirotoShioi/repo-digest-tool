from typing import Any, Dict, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel

from repo_tool.api.repositories import FilterSettingsRepository, SummaryCacheRepository
from repo_tool.api.router import get_github, router
from repo_tool.core.github import GitHub


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
def client_fixture(engine: Engine) -> TestClient:
    """Create a new FastAPI test client with the in-memory database."""
    app = FastAPI()
    app.include_router(router)

    # Only override the GitHub dependency since database is initialized
    app.dependency_overrides[get_github] = lambda: GitHub(directory="./tmp")

    return TestClient(app)


def sort_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a new dictionary sorted by keys"""
    return dict(sorted(d.items()))


@pytest.fixture
def github() -> GitHub:
    """Returns a shared InMemoryGitHub instance"""
    return GitHub(directory="./tmp")


@pytest.fixture(autouse=True)
def reset_github(github: GitHub) -> Generator[None, None, None]:
    """Reset GitHub state before each test"""
    github.clean()
    yield


def test_get_repositories_empty(client: TestClient) -> None:
    response = client.get("/repositories")
    assert response.status_code == 200
    assert response.json() == []


def test_repository_lifecycle(client: TestClient, github: GitHub) -> None:
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


def test_delete_all_repositories(client: TestClient, github: GitHub) -> None:
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


def test_get_repository_settings_default(client: TestClient, github: GitHub) -> None:
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


def test_update_repository_settings(client: TestClient, github: GitHub) -> None:
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


def test_update_settings_validation(client: TestClient, github: GitHub) -> None:
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


def test_settings_persistence_in_db(client: TestClient, session: Session) -> None:
    """Test that repository settings are correctly persisted in the database"""
    # Setup repositories
    filter_settings_repo = FilterSettingsRepository(session)

    # First add a repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Update settings via API
    new_settings = {
        "include_files": ["*.py", "*.md"],
        "exclude_files": ["tests/*", "*.pyc"],
        "max_file_size": 500000,
    }
    response = client.put("/HirotoShioi/repo-digest-tool/settings", json=new_settings)
    assert response.status_code == 200

    # Verify settings in database directly
    db_settings = filter_settings_repo.get_by_repository_id(
        "HirotoShioi/repo-digest-tool"
    )
    count = filter_settings_repo.count()
    assert count == 1
    assert db_settings is not None
    assert db_settings.include_patterns == ["*.py", "*.md"]
    assert db_settings.exclude_patterns == ["tests/*", "*.pyc"]
    assert db_settings.max_file_size == 500000


def test_summary_cache_persistence(
    client: TestClient, session: Session, github: GitHub
) -> None:
    """Test that repository summary is correctly cached in the database"""
    # Setup repositories
    summary_cache_repo = SummaryCacheRepository(session)

    # Add a repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Generate summary via API (assuming this endpoint exists)
    response = client.get("/HirotoShioi/repo-digest-tool/summary")
    assert response.status_code == 200

    # Verify summary cache in database directly
    cached_summary = summary_cache_repo.get_by_repository_id(
        "HirotoShioi/repo-digest-tool"
    )
    count = summary_cache_repo.count()
    assert count == 1
    assert cached_summary is not None
    assert cached_summary.author == "HirotoShioi"
    assert cached_summary.repository == "repo-digest-tool"


def test_summary_cache_deletion_in_db(client: TestClient, session: Session) -> None:
    """Test that repository summary cache is correctly deleted from the database"""
    # Setup repositories
    summary_cache_repo = SummaryCacheRepository(session)

    # Add a repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Generate summary to create cache entry
    response = client.get("/HirotoShioi/repo-digest-tool/summary")
    assert response.status_code == 200
    count = summary_cache_repo.count()
    assert count == 1
    # Update settings via API
    new_settings = {
        "include_files": ["*.py", "*.md"],
        "exclude_files": ["tests/*", "*.pyc"],
        "max_file_size": 500000,
    }
    response = client.put("/HirotoShioi/repo-digest-tool/settings", json=new_settings)
    assert response.status_code == 200
    count = summary_cache_repo.count()
    assert count == 0


def test_settings_deletion_in_db(client: TestClient, session: Session) -> None:
    """Test that repository settings are correctly deleted from the database"""
    # Setup repositories
    filter_settings_repo = FilterSettingsRepository(session)
    # First add a repository and its settings
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Add settings
    settings = {
        "include_files": ["*.py"],
        "exclude_files": [],
        "max_file_size": 500000,
    }
    response = client.put("/HirotoShioi/repo-digest-tool/settings", json=settings)
    assert response.status_code == 200

    # Delete repository via API
    response = client.delete("/repositories/HirotoShioi/repo-digest-tool")
    assert response.status_code == 200

    # Verify settings were deleted from database
    db_settings = filter_settings_repo.get_by_repository_id(
        "HirotoShioi/repo-digest-tool"
    )
    assert db_settings is None


def test_bulk_delete_db_cleanup(client: TestClient, session: Session) -> None:
    """Test that bulk delete properly cleans up database entries"""
    # Setup repositories
    filter_settings_repo = FilterSettingsRepository(session)
    summary_cache_repo = SummaryCacheRepository(session)

    # Add multiple repositories
    repos = [
        "https://github.com/HirotoShioi/repo-digest-tool",
        "https://github.com/HirotoShioi/query-cache",
    ]

    for url in repos:
        response = client.post("/repositories", json={"url": url})
        assert response.status_code == 200

        # Add settings for each
        settings = {
            "include_files": ["*.py"],
            "exclude_files": [],
            "max_file_size": 500000,
        }
        repo_id = url.split("/")[-2] + "/" + url.split("/")[-1]
        response = client.put(f"/{repo_id}/settings", json=settings)
        assert response.status_code == 200

    # Delete all repositories
    response = client.delete("/repositories")
    assert response.status_code == 200

    # Verify all database entries were cleaned up
    for url in repos:
        repo_id = url.split("/")[-2] + "/" + url.split("/")[-1]
        assert filter_settings_repo.get_by_repository_id(repo_id) is None
        assert summary_cache_repo.get_by_repository_id(repo_id) is None
