"""
repo-digest-tool: リポジトリの内容を要約・分析するCLIツール
"""

__version__ = "0.1.0"

from repo_tool.core.contants import DIGEST_DIR, REPO_DIR
from repo_tool.core.digest import generate_digest
from repo_tool.core.repository import download_repo

__all__ = ["generate_digest", "download_repo", "DIGEST_DIR", "REPO_DIR"]
