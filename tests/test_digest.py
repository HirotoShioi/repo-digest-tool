import pytest
import tempfile
from pathlib import Path
from repo_tool import generate_digest, download_repo
from repo_tool.core.repository import calculate_repo_id
from repo_tool.core.contants import DIGEST_DIR

MOCK_REPO_URL = "https://github.com/HirotoShioi/repo-digest-tool"
MOCK_PROMPT = None  # 必要ならカスタムプロンプトを設定
MAX_DIGEST_SIZE_MB = 1 * 1024 * 1024  # ダイジェストファイルの最大サイズ（MB）
MIN_DIGEST_SIZE = 200 * 1024  # ダイジェストファイルの最小サイズ（バイト）


@pytest.fixture
def temp_repo_dir():
    """一時的なディレクトリを作成して返す"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


def test_digest_file_generation(temp_repo_dir):
    # 一時的なリポジトリIDとパス
    repo_id = calculate_repo_id(MOCK_REPO_URL)
    digest_path = Path(DIGEST_DIR) / f"{repo_id}.txt"

    # ダウンロードとダイジェスト生成の呼び出し
    download_repo(MOCK_REPO_URL, repo_id, branch=None)
    generate_digest(repo_id, MOCK_PROMPT)

    # ダイジェストファイルが生成されたことを確認
    assert digest_path.exists(), "Digest file should be generated."

    # ダイジェストファイルの先頭部分を確認
    with digest_path.open("r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        assert (
            first_line
            == "The following text represents the contents of the repository."
        )

    # ファイルサイズの確認（MB単位）
    file_size = digest_path.stat().st_size
    assert file_size > MIN_DIGEST_SIZE, "Digest file should not be empty."
    assert (
        file_size <= MAX_DIGEST_SIZE_MB
    ), f"Digest file size should be less than {MAX_DIGEST_SIZE_MB}MB"
