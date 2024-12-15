from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from repo_tool.api.router import router
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
        repo_id = self._get_repo_id_from_url(url)
        author, name = repo_id.split("/")
        self.repos[repo_id] = Repository(
            id=repo_id,
            name=name,
            url=url,
            author=author,
            branch=branch or "main",
            path=Path(f"/mock/path/{repo_id}"),
            updated_at=datetime.now(),
        )
        return self.repos[repo_id]

    def remove(self, url: str) -> None:
        repo_id = self._get_repo_id_from_url(url)
        print(f"repo_id: {repo_id}")
        if repo_id in self.repos:
            del self.repos[repo_id]

    def clean(self) -> None:
        self.repos.clear()

    def update(self, url: str | None = None) -> List[Repository]:
        if url:
            repo_id = self._get_repo_id_from_url(url)
            if repo_id in self.repos:
                self.repos[repo_id].updated_at = datetime.now()
                return [self.repos[repo_id]]
        else:
            for repo in self.repos.values():
                repo.updated_at = datetime.now()
            return list(self.repos.values())
        return []

    def repo_exists(self, url: str) -> bool:
        repo_id = self._get_repo_id_from_url(url)
        return repo_id in self.repos

    @staticmethod
    def _get_repo_id_from_url(url: str) -> str:
        # https://github.com/user/repo -> user/repo
        return "/".join(url.rstrip("/").split("/")[-2:])


def sort_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    """Returns a new dictionary sorted by keys"""
    return dict(sorted(d.items()))


@pytest.fixture
def test_client() -> TestClient:
    """Returns a FastAPI test client with InMemoryGitHub dependency injection"""
    app = FastAPI()
    app.include_router(router)
    # Inject InMemoryGitHub implementation
    app.dependency_overrides[GitHub] = InMemoryGitHub
    return TestClient(app)


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
