import os
import re
import shutil
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from git import GitCommandError, Repo

from repo_tool.core.logger import log_error

REPO_DIR = "repositories"


class GitHub:
    def __init__(self, github_token: Optional[str] = None) -> None:
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")

    def clone(
        self, repo_url: str, branch: Optional[str] = None, force: bool = False
    ) -> None:
        try:
            repo_path = self.get_repo_path(repo_url)
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

    # @staticmethod
    # def calculate_repo_id(repo_url: str) -> str:
    #     return repo_url.split("/")[-1].replace(".git", "").replace("/", "_")

    @staticmethod
    def get_repo_path(repo_url: str) -> Path:
        if not GitHub.is_valid_repo_url(repo_url):
            raise ValueError("Invalid repository URL")
        # Parse URL to extract author and repo name
        parsed_url = urlparse(repo_url)
        repo_pattern = r"^/([\w-]+)/([\w.-]+)(\.git)?$"
        match = re.match(repo_pattern, parsed_url.path)

        if not match:
            raise ValueError("Repository URL does not match the expected pattern.")

        author, repo = match.groups()[:2]
        return Path(REPO_DIR) / author / repo

    @staticmethod
    def is_valid_repo_url(repo_url: str) -> bool:
        """
        Validate if the given URL is a valid GitHub repository URL.

        Args:
            repo_url: The repository URL to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        # Check URL structure
        parsed_url = urlparse(repo_url)
        if parsed_url.scheme != "https" or parsed_url.netloc != "github.com":
            return False

        # Match GitHub repository pattern (e.g., https://github.com/author/repo.git)
        repo_pattern = r"^/([\w-]+)/([\w.-]+)(\.git)?$"
        match = re.match(repo_pattern, parsed_url.path)
        if not match:
            return False

        # Validate author and repository names
        author, repo = match.groups()[:2]
        if not author or not repo:
            return False

        # Additional checks for invalid characters (optional)
        invalid_chars = re.compile(r"[^\w.-]")
        if invalid_chars.search(author) or invalid_chars.search(repo):
            return False

        return True

    def replace_repo_url(self, repo_url: str) -> str:
        return repo_url.replace(
            "https://github.com/", f"https://{self.github_token}@github.com/"
        )
