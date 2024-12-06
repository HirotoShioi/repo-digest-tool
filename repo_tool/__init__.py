"""
repo-digest-tool: リポジトリの内容を要約・分析するCLIツール
"""

__version__ = "0.1.0"

from repo_tool.core.repository import download_repo
from repo_tool.core.digest import generate_digest

__all__ = ["download_repo", "generate_digest"]

# デフォルトのディレクトリパス
REPO_DIR = "repo"
DIGEST_DIR = "digests"

# パッケージ全体で使用する設定のデフォルト値
DEFAULT_BRANCH = "main"
DEFAULT_PROMPT = "リポジトリの内容を簡潔に要約してください。"
