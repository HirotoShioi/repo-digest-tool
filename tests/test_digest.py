from pathlib import Path
from repo_tool import generate_digest, download_repo
from repo_tool.core.repository import calculate_repo_id
from repo_tool.core.contants import DIGEST_DIR

REPO_URL = "https://github.com/HirotoShioi/repo-digest-tool"
PROMPT = None


def test_digest_file_generation():
    repo_id = calculate_repo_id(REPO_URL)
    digest_path = Path(DIGEST_DIR) / f"{repo_id}.txt"

    download_repo(REPO_URL, repo_id, branch=None)
    generate_digest(repo_id, PROMPT)

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
