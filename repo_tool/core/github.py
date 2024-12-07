import os
import shutil
from pathlib import Path
from typing import Optional

from git import GitCommandError, Repo

from repo_tool.core.contants import REPO_DIR
from repo_tool.core.logger import log_error


class GitHub:
    def __init__(self, github_token: Optional[str] = None) -> None:
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")

    def clone(
        self, repo_url: str, branch: Optional[str] = None, force: bool = False
    ) -> None:
        try:
            repo_path = os.path.join(REPO_DIR, self.calculate_repo_id(repo_url))
            if force:
                shutil.rmtree(repo_path, ignore_errors=True)
            if not os.path.exists(repo_path):
                Repo.clone_from(
                    url=self.replace_repo_url(repo_url),
                    to_path=repo_path,
                    depth=1,
                    branch=branch if branch else None,
                )
        except GitCommandError as e:
            log_error(e)
            raise e

    @staticmethod
    def calculate_repo_id(repo_url: str) -> str:
        return repo_url.split("/")[-1].replace(".git", "").replace("/", "_")

    @staticmethod
    def get_repo_path(repo_url: str) -> Path:
        if not GitHub.is_valid_repo_url(repo_url):
            raise ValueError("Invalid repository URL")
        author = repo_url.split("/")[-2]
        repo_id = repo_url.split("/")[-1].replace(".git", "")
        return Path(REPO_DIR) / author / repo_id

    @staticmethod
    def is_valid_repo_url(repo_url: str) -> bool:
        is_valid_url = repo_url.startswith("https://github.com/")
        author = repo_url.split("/")[-2]
        repo_id = repo_url.split("/")[-1].replace(".git", "")
        return all([is_valid_url, author, repo_id])

    def replace_repo_url(self, repo_url: str) -> str:
        return repo_url.replace(
            "https://github.com/", f"https://{self.github_token}@github.com/"
        )
