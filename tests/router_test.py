from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from repo_tool.api.router import get_github, router
from repo_tool.core.github import GitHub, Repository


class InMemoryGitHub(GitHub):
    """In-memory implementation of GitHub for testing"""

    def __init__(self) -> None:
        self.repos: Dict[str, Repository] = {}

    def list(self) -> List[Repository]:
        return list(self.repos.values())

    def get(self, author: str, repository_name: str) -> Repository:
        repo_id = f"{author}/{repository_name}"
        if repo_id not in self.repos:
            raise ValueError(f"Repository {repo_id} not found")
        return self.repos[repo_id]

    def clone(
        self, url: str, branch: str | None = None, force: bool = False
    ) -> Optional[Repository]:
        try:
            repo_id = GitHub.get_repo_path(url)
        except ValueError as e:
            raise ValueError(f"Invalid repository URL: {str(e)}")

        if str(repo_id) in self.repos and not force:
            # Return existing repo if not force cloning
            return self.repos[str(repo_id)]

        # Remove existing repo if force=True
        if force:
            self.remove(url)

        author, name = str(repo_id).split("/")
        self.repos[str(repo_id)] = Repository(
            id=str(repo_id),
            name=name,
            url=url,
            author=author,
            branch=branch or "main",
            path=Path(f"/mock/path/{repo_id}"),
            updated_at=datetime.now(),
        )
        return self.repos[str(repo_id)]

    def remove(self, url: str) -> None:
        repo_id = GitHub.get_repo_path(url)
        print(f"repo_id: {repo_id}")
        if str(repo_id) in self.repos:
            del self.repos[str(repo_id)]

    def clean(self) -> None:
        self.repos.clear()

    def update(self, url: str | None = None) -> List[Repository]:
        if url:
            repo_id = GitHub.get_repo_path(url)
            if str(repo_id) in self.repos:
                self.repos[str(repo_id)].updated_at = datetime.now()
                return [self.repos[str(repo_id)]]
        else:
            for repo in self.repos.values():
                repo.updated_at = datetime.now()
            return list(self.repos.values())
        return []

    def repo_exists(self, url: str) -> bool:
        repo_id = GitHub.get_repo_path(url)
        return str(repo_id) in self.repos


def sort_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a new dictionary sorted by keys"""
    return dict(sorted(d.items()))


@pytest.fixture
def test_client() -> TestClient:
    """Returns a FastAPI test client with InMemoryGitHub dependency injection"""
    app = FastAPI()
    app.include_router(router)
    # Inject InMemoryGitHub implementation
    app.dependency_overrides[get_github] = InMemoryGitHub
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_github(test_client: TestClient) -> Generator[None, None, None]:
    """Reset GitHub state before each test"""
    test_client.delete("/repositories")
    yield


def test_get_repositories_empty(test_client: TestClient) -> None:
    response = test_client.get("/repositories")
    assert response.status_code == 200
    assert response.json() == []


def test_repository_lifecycle(test_client: TestClient) -> None:
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


def test_delete_all_repositories(test_client: TestClient) -> None:
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
    assert "Invalid repository URL" in response.json()["detail"]


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


def test_clone_repository_with_force(test_client: TestClient) -> None:
    """Test force cloning an existing repository"""
    url = "https://github.com/HirotoShioi/repo-digest-tool"
    # First clone
    response = test_client.post("/repositories", json={"url": url, "branch": "main"})
    assert response.status_code == 200

    # Force clone
    response = test_client.post(
        "/repositories", json={"url": url, "branch": "develop", "force": True}
    )
    assert response.status_code == 200

    # Verify branch was updated
    response = test_client.get("/repositories/HirotoShioi/repo-digest-tool")
    assert response.status_code == 200
    assert response.json()["branch"] == "develop"


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
