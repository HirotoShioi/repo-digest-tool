import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from repo_tool import generate_digest
from repo_tool.core.contants import DIGEST_DIR
from repo_tool.core.github import GitHub

REPO_URL = "https://github.com/HirotoShioi/repo-digest-tool"
PROMPT = None


@pytest.fixture(autouse=True)
def cleanup() -> Generator[None, None, None]:
    # Setup - ensure clean state
    if Path(DIGEST_DIR).exists():
        shutil.rmtree(DIGEST_DIR)
    Path(DIGEST_DIR).mkdir(parents=True, exist_ok=True)

    yield

    # Teardown
    if Path(DIGEST_DIR).exists():
        shutil.rmtree(DIGEST_DIR)


@pytest.fixture(name="github_dir")
def github_dir_fixture() -> Generator[Path, None, None]:
    """Create a temporary directory for GitHub operations"""
    tmp_dir = tempfile.mkdtemp()
    yield Path(tmp_dir)
    # Clean up after all tests
    try:
        shutil.rmtree(tmp_dir)
    except FileNotFoundError:
        pass


@pytest.fixture(name="github")
def github_fixture(github_dir: Path) -> GitHub:
    return GitHub(directory=str(github_dir))


def test_digest_file_generation(github: GitHub) -> None:
    digest_path = Path(DIGEST_DIR) / "repo-digest-tool.txt"
    github.clone(REPO_URL, branch=None, force=True)

    repo_info = github.get_repo_info(REPO_URL)
    generate_digest(repo_info, PROMPT)

    assert digest_path.exists(), "Digest file should be generated."

    with digest_path.open("r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        assert (
            first_line
            == "The following text represents the contents of the repository."
        )

    file_size = digest_path.stat().st_size
    MIN_DIGEST_SIZE = 40 * 1024
    MAX_DIGEST_SIZE_MB = 1 * 1024 * 1024
    assert file_size > MIN_DIGEST_SIZE, "Digest file size should be larger than 40KB."
    assert (
        file_size <= MAX_DIGEST_SIZE_MB
    ), f"Digest file size should be less than {MAX_DIGEST_SIZE_MB}MB"

    summary_path = Path(DIGEST_DIR) / "repo-digest-tool_report.html"
    assert summary_path.exists(), "Summary file should be generated."
