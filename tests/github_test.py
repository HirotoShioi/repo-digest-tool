import shutil
from pathlib import Path
from typing import Generator

import pytest

from repo_tool.core.github import REPO_DIR, GitHub

TEST_REPO_URL = "https://github.com/octocat/hello-world"  # 小規模な公開リポジトリ
TEST_REPO_AUTHOR = "octocat"
TEST_REPO_NAME = "hello-world"
TEST_REPO_PATH = Path(REPO_DIR) / TEST_REPO_AUTHOR / TEST_REPO_NAME


@pytest.fixture(scope="function")
def clean_test_environment() -> Generator[None, None, None]:
    """
    テスト実行前後にリポジトリディレクトリをクリーンアップする。
    """
    if Path(REPO_DIR).exists():
        shutil.rmtree(REPO_DIR)
    yield
    if Path(REPO_DIR).exists():
        shutil.rmtree(REPO_DIR)


def test_clone_repository(clean_test_environment: Generator[None, None, None]) -> None:
    """
    リポジトリをクローンできるかテスト。
    """
    github = GitHub()
    github.clone(TEST_REPO_URL)
    assert TEST_REPO_PATH.exists()  # リポジトリのパスが存在すること
    assert (TEST_REPO_PATH / ".git").exists()  # Git管理されていること


def test_list_repositories(clean_test_environment: Generator[None, None, None]) -> None:
    """
    クローンしたリポジトリがリストに含まれるかテスト。
    """
    github = GitHub()
    github.clone(TEST_REPO_URL)
    repositories = github.list()
    assert len(repositories) == 1
    repository = repositories[0]
    assert repository.name == TEST_REPO_NAME
    assert repository.author == TEST_REPO_AUTHOR
    assert repository.url == TEST_REPO_URL


def test_remove_repository(clean_test_environment: Generator[None, None, None]) -> None:
    """
    リポジトリを削除できるかテスト。
    """
    github = GitHub()
    github.clone(TEST_REPO_URL)
    github.remove(TEST_REPO_URL)
    assert not TEST_REPO_PATH.exists()  # リポジトリが削除されていること
    author_path = Path(REPO_DIR) / TEST_REPO_AUTHOR
    assert not author_path.exists()  # 著者ディレクトリが空なら削除されていること


def test_clean_all_repositories(
    clean_test_environment: Generator[None, None, None]
) -> None:
    """
    すべてのリポジトリを削除するcleanメソッドのテスト。
    """
    github = GitHub()
    github.clone(TEST_REPO_URL)
    github.clean()
    assert not Path(REPO_DIR).exists()  # ベースディレクトリが削除されていること
