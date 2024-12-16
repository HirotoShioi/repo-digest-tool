import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from repo_tool.api.router import get_github, router
from repo_tool.core.github import GitHub, Repository


def sort_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a new dictionary sorted by keys"""
    return dict(sorted(d.items()))


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

        # Extract repository_id from URL
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


@pytest.fixture
def github() -> InMemoryGitHub:
    """Returns a shared InMemoryGitHub instance"""
    return InMemoryGitHub()


@pytest.fixture
def test_client(github: InMemoryGitHub) -> TestClient:
    """Returns a FastAPI test client with InMemoryGitHub dependency injection"""
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_github] = lambda: github
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_github(github: InMemoryGitHub) -> Generator[None, None, None]:
    """Reset GitHub state before each test"""
    github.repositories.clear()
    yield


def test_get_repositories_empty(test_client: TestClient) -> None:
    response = test_client.get("/repositories")
    assert response.status_code == 200
    assert response.json() == []


def test_repository_lifecycle(test_client: TestClient, github: InMemoryGitHub) -> None:
    # 1. Clone repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = test_client.post("/repositories", json=clone_payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # 2. Get repository list
    response = test_client.get("/repositories")
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
    response = test_client.get("/repositories/HirotoShioi/repo-digest-tool")
    assert response.status_code == 200
    repo = response.json()
    assert repo["id"] == "HirotoShioi/repo-digest-tool"

    # 4. Update repository
    response = test_client.put("/repositories/HirotoShioi/repo-digest-tool")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # 5. Delete repository
    response = test_client.delete(
        "/repositories/HirotoShioi/repo-digest-tool",
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # 6. Verify repository list is empty after deletion
    response = test_client.get("/repositories")
    assert response.status_code == 200
    assert response.json() == []


def test_update_repository_not_found(test_client: TestClient) -> None:
    response = test_client.put("/repositories/HirotoShioi/repo-digest-tool")
    assert response.status_code == 404
    assert response.json() == {"detail": "Repository not found"}


def test_get_summary_not_found(test_client: TestClient) -> None:
    response = test_client.get("/HirotoShioi/repo-digest-tool/summary")
    assert response.status_code == 404
    assert response.json() == {"detail": "Repository not found"}


def test_delete_all_repositories(
    test_client: TestClient, github: InMemoryGitHub
) -> None:
    # First add a repository
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    response = test_client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Delete all repositories
    response = test_client.delete("/repositories")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # Verify repository list is empty
    response = test_client.get("/repositories")
    assert response.status_code == 200
    assert response.json() == []


def test_clone_repository_invalid_url(test_client: TestClient) -> None:
    """Test cloning with invalid URL format"""
    clone_payload = {
        "url": "invalid-url",
        "branch": "main",
    }
    response = test_client.post("/repositories", json=clone_payload)
    assert response.status_code == 400


def test_clone_repository_duplicate(test_client: TestClient) -> None:
    """Test cloning same repository twice without force flag"""
    clone_payload = {
        "url": "https://github.com/HirotoShioi/repo-digest-tool",
        "branch": "main",
    }
    # First clone should succeed
    response = test_client.post("/repositories", json=clone_payload)
    assert response.status_code == 200

    # Second clone should return success (idempotent behavior)
    response = test_client.post("/repositories", json=clone_payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}


def test_get_repository_invalid_author_repo(test_client: TestClient) -> None:
    """Test getting repository with invalid author/repo format"""
    response = test_client.get("/repositories/invalid-format")
    assert response.status_code == 404


def test_update_all_repositories(test_client: TestClient) -> None:
    """Test updating all repositories"""
    # Add two repositories
    repos = [
        "https://github.com/HirotoShioi/repo-digest-tool",
        "https://github.com/HirotoShioi/query-cache",
    ]

    for url in repos:
        response = test_client.post("/repositories", json={"url": url})
        assert response.status_code == 200

    # Update all repositories
    response = test_client.put("/repositories")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    # Verify all repositories were updated
    response = test_client.get("/repositories")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_nonexistent_repository(test_client: TestClient) -> None:
    """Test deleting a repository that doesn't exist"""
    response = test_client.delete("/repositories/nonexistent/repo")
    assert response.status_code == 404
    assert "Repository not found" in response.json()["detail"]


def test_clone_repository_missing_url(test_client: TestClient) -> None:
    """Test cloning with missing URL"""
    response = test_client.post("/repositories", json={"branch": "main"})
    assert response.status_code == 422  # FastAPI validation error
