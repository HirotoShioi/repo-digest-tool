# test_github.py
import datetime
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from git import GitCommandError

# テスト対象のモジュールをインポート
from repo_tool.core.github import REPO_DIR, GitHub  # 適宜修正

repo_url = "https://github.com/HirotoShioi/repo-digest-tool"


@pytest.fixture
def mock_repo_dir(tmp_path: Path) -> Generator[Path, None, None]:
    # 一時ディレクトリをREPO_DIRとして使用
    original_repo_dir = REPO_DIR
    test_repo_dir = tmp_path / "repositories"
    test_repo_dir.mkdir()
    with patch("repo_tool.core.github.REPO_DIR", str(test_repo_dir)):
        yield test_repo_dir


@pytest.fixture
def github_instance() -> GitHub:
    # トークンありなし双方をテスト可能だが、ここでは簡略化
    return GitHub(github_token="dummy_token")


def create_dummy_repo_dir(
    base_dir: Path, author: str = "testuser", repo: str = "testrepo"
) -> Path:
    author_path = base_dir / author
    author_path.mkdir(parents=True, exist_ok=True)
    repo_path = author_path / repo
    repo_path.mkdir(exist_ok=True)
    git_path = repo_path / ".git"
    git_path.mkdir()
    return repo_path


@patch("repo_tool.core.logger.log_error")
@patch("repo_tool.core.shutil.rmtree")
@patch("repo_tool.core.git.Repo.clone_from")
def test_clone_success(
    mock_clone_from: MagicMock,
    mock_rmtree: MagicMock,
    mock_log_error: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    github_instance.clone(repo_url)
    mock_clone_from.assert_called_once_with(
        url=f"https://dummy_token@github.com/{repo_url}",
        to_path=str(mock_repo_dir / "HirotoShioi" / "repo-digest-tool"),
        depth=1,
        branch=None,
    )
    mock_log_error.assert_not_called()
    mock_rmtree.assert_not_called()


@patch("repo_tool.core.logger.log_error")
@patch("repo_tool.core.shutil.rmtree")
@patch(
    "repo_tool.core.git.Repo.clone_from",
    side_effect=GitCommandError("cmd", "err"),
)
def test_clone_failure(
    mock_clone_from: MagicMock,
    mock_rmtree: MagicMock,
    mock_log_error: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    with pytest.raises(GitCommandError):
        github_instance.clone(repo_url)
    mock_log_error.assert_called_once()
    mock_rmtree.assert_not_called()


@patch("repo_tool.core.shutil.rmtree")
def test_clone_force(
    mock_rmtree: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    # force=Trueのときに既存ディレクトリを削除するか
    create_dummy_repo_dir(mock_repo_dir, "testuser", "testrepo")
    github_instance.clone(repo_url, force=True)
    mock_rmtree.assert_called_once_with(
        mock_repo_dir / "testuser" / "testrepo", ignore_errors=True
    )


@patch("repo_tool.core.shutil.rmtree")
def test_remove_success(
    mock_rmtree: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    repo_path = create_dummy_repo_dir(mock_repo_dir, "testuser", "testrepo")
    github_instance.remove(repo_url)
    mock_rmtree.assert_called_once_with(repo_path, ignore_errors=True)
    # 著者ディレクトリが空なら削除
    assert not (mock_repo_dir / "testuser").exists()


@patch("repo_tool.core.shutil.rmtree")
def test_remove_author_not_empty(
    mock_rmtree: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    # 著者ディレクトリに別のリポジトリがある場合はauthor_dirは削除されない
    create_dummy_repo_dir(mock_repo_dir, "testuser", "testrepo")
    other_repo = create_dummy_repo_dir(mock_repo_dir, "testuser", "another_repo")
    github_instance.remove(repo_url)
    mock_rmtree.assert_called_once()
    assert (mock_repo_dir / "testuser").exists()
    assert other_repo.exists()


@patch("repo_tool.core.shutil.rmtree")
def test_clean_success(
    mock_rmtree: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    github_instance.clean()
    mock_rmtree.assert_called_once_with("repositories", ignore_errors=True)


@patch("repo_tool.core.git.Repo")
def test_update_success(
    mock_repo: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    repo_path = create_dummy_repo_dir(mock_repo_dir, "testuser", "testrepo")
    mock_repo_instance = MagicMock()
    mock_repo.return_value = mock_repo_instance
    github_instance.update(repo_url)
    mock_repo.assert_called_once_with(repo_path)
    mock_repo_instance.remotes.origin.pull.assert_called_once()


def test_update_invalid_url(github_instance: GitHub) -> None:
    with pytest.raises(ValueError):
        github_instance.update("https://example.com/foo/bar.git")


def test_update_missing_repo(
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    with pytest.raises(ValueError):
        github_instance.update("https://github.com/testuser/doesnotexist.git")


@patch("your_module_path.Repo")
@patch("your_module_path.log_error")
def test_list_success(
    mock_log_error: MagicMock,
    mock_repo: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    # 複数の正しいリポジトリを作り、listを確認
    repo1 = create_dummy_repo_dir(mock_repo_dir, "testuser", "repo1")
    repo2 = create_dummy_repo_dir(mock_repo_dir, "anotheruser", "repo2")

    mock_repo_instance_1 = MagicMock()
    mock_repo_instance_1.remotes.origin.url = "https://github.com/testuser/repo1.git"
    mock_repo_instance_1.active_branch.name = "main"
    mock_repo_instance_1.head.commit.committed_date = (
        datetime.datetime.now().timestamp()
    )

    mock_repo_instance_2 = MagicMock()
    mock_repo_instance_2.remotes.origin.url = "https://github.com/anotheruser/repo2.git"
    mock_repo_instance_2.active_branch.name = "dev"
    mock_repo_instance_2.head.commit.committed_date = (
        datetime.datetime.now().timestamp()
    )

    # 呼ばれた順に返すためにside_effectを使用
    mock_repo.side_effect = [mock_repo_instance_1, mock_repo_instance_2]

    repos = github_instance.list()
    assert len(repos) == 2
    assert any(r.name == "repo1" and r.author == "testuser" for r in repos)
    assert any(r.name == "repo2" and r.author == "anotheruser" for r in repos)
    mock_log_error.assert_not_called()


@patch("your_module_path.Repo", side_effect=Exception("Some error"))
@patch("your_module_path.log_error")
def test_list_error(
    mock_log_error: MagicMock,
    mock_repo: MagicMock,
    github_instance: GitHub,
    mock_repo_dir: Path,
) -> None:
    create_dummy_repo_dir(mock_repo_dir, "testuser", "repo1")
    repos = github_instance.list()
    assert len(repos) == 0
    mock_log_error.assert_called_once()


def test_get_repo_path_success() -> None:
    url = "https://github.com/testuser/testrepo.git"
    path = GitHub.get_repo_path(url)
    assert str(path) == "repositories/testuser/testrepo"


def test_get_repo_path_invalid() -> None:
    with pytest.raises(ValueError):
        GitHub.get_repo_path("https://github.com/invalid_url")


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://github.com/testuser/testrepo.git", True),
        ("https://github.com/testuser/testrepo", True),
        ("http://github.com/testuser/testrepo.git", False),
        ("https://github.com/testuser/", False),
        ("https://example.com/testuser/testrepo.git", False),
    ],
)
def test_is_valid_repo_url(url: str, expected: bool) -> None:
    assert GitHub.is_valid_repo_url(url) == expected


@pytest.mark.parametrize(
    "url,expected",
    [
        (
            "https://token@github.com/testuser/testrepo.git",
            "https://github.com/testuser/testrepo.git",
        ),
        (
            "https://github.com/testuser/testrepo.git",
            "https://github.com/testuser/testrepo.git",
        ),
    ],
)
def test_remove_github_token(url: str, expected: str) -> None:
    assert GitHub.remove_github_token(url) == expected


def test_replace_repo_url(github_instance: GitHub) -> None:
    url = "https://github.com/testuser/testrepo.git"
    replaced = github_instance.replace_repo_url(url)
    assert replaced == "https://dummy_token@github.com/testuser/testrepo.git"
