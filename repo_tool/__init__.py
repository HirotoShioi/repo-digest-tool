"""
repo-digest-tool: CLI tool to generate a summary of a repository
"""

__version__ = "0.1.0"

from repo_tool.core.contants import DIGEST_DIR
from repo_tool.core.digest import generate_digest
from repo_tool.core.github import GitHub

__all__ = ["generate_digest", "GitHub", "DIGEST_DIR"]
