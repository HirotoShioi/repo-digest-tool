import shutil
from pathlib import Path
from typing import Generator

import pytest
from git import GitCommandError

from repo_tool.core.github import REPO_DIR, GitHub

# Constants for testing
TEST_REPO_URL = "https://github.com/octocat/hello-world"  # Small public repository
TEST_REPO_AUTHOR = "octocat"
TEST_REPO_NAME = "hello-world"
TEST_REPO_PATH = Path(REPO_DIR) / TEST_REPO_AUTHOR / TEST_REPO_NAME


@pytest.fixture(scope="function")
def clean_test_environment() -> Generator[None, None, None]:
    """
    Fixture to clean the repository directory before and after each test.
    """
    if Path(REPO_DIR).exists():
        shutil.rmtree(REPO_DIR)
    yield
    if Path(REPO_DIR).exists():
        shutil.rmtree(REPO_DIR)


def test_clone_repository(clean_test_environment: Generator[None, None, None]) -> None:
    """
    Test if a repository can be cloned successfully.
    """
    github = GitHub()
    github.clone(TEST_REPO_URL)
    assert TEST_REPO_PATH.exists()  # Check if the repository path exists
    assert (TEST_REPO_PATH / ".git").exists()  # Check if the repository is Git-managed


def test_clone_repository_invalid_url(
    clean_test_environment: Generator[None, None, None]
) -> None:
    """
    Test cloning a repository with an invalid URL.
    """
    github = GitHub()
    with pytest.raises(GitCommandError):
        github.clone("https://github.com/octocat/invalid-repo")


def test_update_nonexistent_repository(
    clean_test_environment: Generator[None, None, None]
) -> None:
    """
    Test updating a repository that does not exist locally.
    """
    github = GitHub()
    with pytest.raises(ValueError, match="Repository does not exist"):
        github.update(TEST_REPO_URL)


def test_list_repositories(clean_test_environment: Generator[None, None, None]) -> None:
    """
    Test if cloned repositories are listed correctly.
    """
    github = GitHub()
    github.clone(TEST_REPO_URL)
    repositories = github.list()
    assert len(repositories) == 1  # Verify there is one repository
    repository = repositories[0]
    assert repository.name == TEST_REPO_NAME  # Verify repository name
    assert repository.author == TEST_REPO_AUTHOR  # Verify repository author
    assert repository.url == TEST_REPO_URL  # Verify repository URL


def test_list_repositories_empty_directory(
    clean_test_environment: Generator[None, None, None]
) -> None:
    """
    Test listing repositories when no repositories exist.
    """
    github = GitHub()
    repositories = github.list()
    assert len(repositories) == 0  # Should return an empty list


def test_remove_repository(clean_test_environment: Generator[None, None, None]) -> None:
    """
    Test if a repository can be removed successfully.
    """
    github = GitHub()
    github.clone(TEST_REPO_URL)
    github.remove(TEST_REPO_URL)
    assert not TEST_REPO_PATH.exists()  # Check if the repository is removed
    author_path = Path(REPO_DIR) / TEST_REPO_AUTHOR
    assert not author_path.exists()  # Check if the author directory is removed


def test_remove_nonexistent_repository(
    clean_test_environment: Generator[None, None, None]
) -> None:
    """
    Test removing a repository that does not exist.
    """
    github = GitHub()
    github.remove(
        "https://github.com/octocat/nonexistent-repo"
    )  # Should not raise an exception


def test_clean_all_repositories(
    clean_test_environment: Generator[None, None, None]
) -> None:
    """
    Test if all repositories can be cleaned at once.
    """
    github = GitHub()
    github.clone(TEST_REPO_URL)
    github.clean()
    assert not Path(REPO_DIR).exists()  # Check if the base directory is removed


def test_is_valid_repo_url_valid_urls() -> None:
    """
    Test valid repository URLs.
    """
    assert GitHub.is_valid_repo_url("https://github.com/octocat/hello-world") is True
    assert (
        GitHub.is_valid_repo_url("https://github.com/octocat/hello-world.git") is True
    )


def test_is_valid_repo_url_invalid_urls() -> None:
    """
    Test invalid repository URLs.
    """
    assert (
        GitHub.is_valid_repo_url("http://github.com/octocat/hello-world") is False
    )  # Not HTTPS
    assert (
        GitHub.is_valid_repo_url("https://github.com/octocat") is False
    )  # Missing repository name
    assert (
        GitHub.is_valid_repo_url("https://github.com/") is False
    )  # Missing author and repository
    assert (
        GitHub.is_valid_repo_url("https://bitbucket.org/octocat/hello-world") is False
    )  # Not GitHub
    assert GitHub.is_valid_repo_url("invalid_url") is False  # Invalid format


def test_is_valid_repo_url_edge_cases() -> None:
    """
    Test edge cases for repository URLs.
    """
    assert (
        GitHub.is_valid_repo_url("https://github.com/octocat/hello-world-123") is True
    )
    assert GitHub.is_valid_repo_url("https://github.com/octo-cat_/repo.name") is True
    assert (
        GitHub.is_valid_repo_url("https://github.com/octo-cat-/repo-name.git") is True
    )


def test_get_repo_path_valid_urls() -> None:
    """
    Test repository path generation for valid URLs.
    """
    assert (
        GitHub.get_repo_path("https://github.com/octocat/hello-world")
        == Path(REPO_DIR) / "octocat" / "hello-world"
    )
    assert (
        GitHub.get_repo_path("https://github.com/octocat/hello-world.git")
        == Path(REPO_DIR) / "octocat" / "hello-world"
    )


def test_get_repo_path_invalid_urls() -> None:
    """
    Test repository path generation for invalid URLs.
    """
    with pytest.raises(ValueError, match="Invalid repository URL"):
        GitHub.get_repo_path("http://github.com/octocat/hello-world")  # Not HTTPS
    with pytest.raises(ValueError, match="Invalid repository URL"):
        GitHub.get_repo_path("https://github.com/octocat")  # Missing repository name
    with pytest.raises(ValueError, match="Invalid repository URL"):
        GitHub.get_repo_path("invalid_url")  # Invalid format


def test_get_repo_path_edge_cases() -> None:
    """
    Test repository path generation for edge cases.
    """
    assert (
        GitHub.get_repo_path("https://github.com/octocat-123/repo-name.git")
        == Path(REPO_DIR) / "octocat-123" / "repo-name"
    )


def test_remove_github_token_valid_cases() -> None:
    """
    Test removal of GitHub tokens from valid repository URLs.
    """
    assert (
        GitHub.remove_github_token("https://ghp_abc123@github.com/octocat/hello-world")
        == "https://github.com/octocat/hello-world"
    )
    assert (
        GitHub.remove_github_token("https://github.com/octocat/hello-world")
        == "https://github.com/octocat/hello-world"
    )  # No token


def test_remove_github_token_invalid_cases() -> None:
    """
    Test removal of GitHub tokens for invalid URLs.
    """
    assert (
        GitHub.remove_github_token("http://ghp_abc123@github.com/octocat/hello-world")
        == "http://github.com/octocat/hello-world"
    )  # Not HTTPS
    assert (
        GitHub.remove_github_token("invalid_url") == "invalid_url"
    )  # Invalid format remains unchanged


def test_remove_github_token_edge_cases() -> None:
    """
    Test removing GitHub tokens for malformed token cases.
    """
    assert (
        GitHub.remove_github_token("https://partial_token@github.com/octocat/repo")
        == "https://github.com/octocat/repo"
    )
    assert (
        GitHub.remove_github_token("https://token@github.com@github.com/octocat/repo")
        == "https://github.com/octocat/repo"
    )


def test_get_repo_path_security_cases() -> None:
    """
    Test repository path generation for security edge cases.
    """
    with pytest.raises(ValueError, match="Invalid repository URL"):
        GitHub.get_repo_path("https://github.com/../../malicious/repo")

    with pytest.raises(ValueError, match="Invalid repository URL"):
        GitHub.get_repo_path("https://github.com/octocat/hello-world?.git")


def test_resolve_repo_url() -> None:
    # 有効な完全URL
    assert (
        GitHub.resolve_repo_url("https://github.com/author/repo")
        == "https://github.com/author/repo"
    )
    assert (
        GitHub.resolve_repo_url("https://github.com/author/repo.git")
        == "https://github.com/author/repo.git"
    )

    # 有効な短縮形式
    assert GitHub.resolve_repo_url("author/repo") == "https://github.com/author/repo"
    assert (
        GitHub.resolve_repo_url("author/repo.git")
        == "https://github.com/author/repo.git"
    )

    # 無効な形式
    try:
        GitHub.resolve_repo_url("author//repo")
    except ValueError as e:
        assert (
            str(e)
            == "Invalid short-form repository URL. Must match 'author/repo-name' format."
        )

    try:
        GitHub.resolve_repo_url("author/repo/extra")
    except ValueError as e:
        assert (
            str(e)
            == "Invalid short-form repository URL. Must match 'author/repo-name' format."
        )

    try:
        GitHub.resolve_repo_url("author/re..po")
    except ValueError as e:
        assert (
            str(e)
            == "Invalid short-form repository URL. Must match 'author/repo-name' format."
        )

    try:
        GitHub.resolve_repo_url("invalid-url")
    except ValueError as e:
        assert (
            str(e)
            == "Invalid short-form repository URL. Must match 'author/repo-name' format."
        )
