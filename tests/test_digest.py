from pathlib import Path

from repo_tool import generate_digest
from repo_tool.core.contants import DIGEST_DIR
from repo_tool.core.github import GitHub

REPO_URL = "https://github.com/HirotoShioi/repo-digest-tool"
PROMPT = None


def test_digest_file_generation() -> None:
    digest_path = Path(DIGEST_DIR) / "repo-digest-tool.txt"
    github = GitHub()
    github.clone(REPO_URL, branch=None, force=True)
    repo_path = GitHub.get_repo_path(REPO_URL)
    generate_digest(repo_path, PROMPT)

    assert digest_path.exists(), "Digest file should be generated."

    with digest_path.open("r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        assert (
            first_line
            == "The following text represents the contents of the repository."
        )

    file_size = digest_path.stat().st_size
    MIN_DIGEST_SIZE = 150 * 1024
    MAX_DIGEST_SIZE_MB = 1 * 1024 * 1024
    assert file_size > MIN_DIGEST_SIZE, "Digest file size should be larger than 200KB."
    assert (
        file_size <= MAX_DIGEST_SIZE_MB
    ), f"Digest file size should be less than {MAX_DIGEST_SIZE_MB}MB"
