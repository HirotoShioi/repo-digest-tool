import datetime
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse, urlunparse

from git import GitCommandError, Repo

from repo_tool.core.logger import log_error

REPO_DIR = "repositories"


@dataclass
class Repository:
    url: str
    branch: Optional[str]
    path: Path
    updated_at: datetime.datetime
    name: str
    author: str
    size: int = 0


class GitHub:
    def __init__(self, github_token: Optional[str] = None) -> None:
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")

    def clone(
        self, repo_url: str, branch: Optional[str] = None, force: bool = False
    ) -> None:
        """
        Clone a repository.

        Args:
            repo_url (str): Repository URL.
            branch (Optional[str], optional): Branch to clone. Defaults to None.
            force (bool, optional): Force re-clone a repository. Defaults to False.

        Raises:
            e: GitCommandError
        """
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

    def remove(self, repo_url: str) -> None:
        """
        Delete a repository.

        Args:
            repo_url (str): The repository URL.
        """
        repo_path = self.get_repo_path(repo_url)
        print(repo_path)
        shutil.rmtree(repo_path, ignore_errors=True)
        author_path = repo_path.parent
        if not os.listdir(author_path):
            os.rmdir(author_path)

    def clean(self) -> None:
        """
        Delete all repositories.
        """
        shutil.rmtree(REPO_DIR, ignore_errors=True)

    def update(self, repo_url: str) -> None:
        """
        Update a repository.

        Args:
            repo_url (str): Repository URL.

        Raises:
            ValueError: Invalid repository URL
        """
        if not self.is_valid_repo_url(repo_url):
            raise ValueError("Invalid repository URL")
        repo_path = self.get_repo_path(repo_url)
        if not os.path.exists(repo_path):
            raise ValueError("Repository does not exist")
        repo = Repo(repo_path)
        repo.remotes.origin.pull()

    def list(self) -> List[Repository]:
        """
        List all repositories.

        Returns:
            List[Repository]: List of repositories with their information
        """
        try:
            # Get only the repository root directories
            repo_paths = []
            if Path(REPO_DIR).exists():
                for author_dir in Path(REPO_DIR).iterdir():
                    if author_dir.is_dir():
                        for repo_dir in author_dir.iterdir():
                            if repo_dir.is_dir() and (repo_dir / ".git").exists():
                                repo_paths.append(repo_dir)

            repositories = []
            for repo_path in repo_paths:
                try:
                    repo = Repo(repo_path)
                    name = repo_path.name
                    author = repo_path.parent.name
                    size = repo_path.stat().st_size
                    repositories.append(
                        Repository(
                            url=GitHub.remove_github_token(repo.remotes.origin.url),
                            branch=repo.active_branch.name,
                            path=repo_path,
                            updated_at=datetime.datetime.fromtimestamp(
                                repo.head.commit.committed_date
                            ),
                            name=name,
                            author=author,
                            size=size,
                        )
                    )
                except Exception as e:
                    log_error(e)
                    continue

            return repositories
        except Exception as e:
            log_error(e)
            return []

    @staticmethod
    def get_repo_path(repo_url: str) -> Path:
        """
        Get the path of a repository.
        The path is `repositories/author/repository_name`.

        Args:
            repo_url (str): The repository URL.

        Returns:
            Path: The path of the repository.
        """
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

    @staticmethod
    def remove_github_token(repo_url: str) -> str:
        """
        Remove GitHub token from the repository URL if present.

        Args:
            repo_url (str): The repository URL.

        Returns:
            str: The sanitized repository URL.
        """
        parsed_url = urlparse(repo_url)
        if "@" in parsed_url.netloc:
            # Split on `@` to remove token part
            sanitized_netloc = parsed_url.netloc.split("@")[-1]
            sanitized_url = urlunparse(parsed_url._replace(netloc=sanitized_netloc))
            return sanitized_url
        return repo_url

    def replace_repo_url(self, repo_url: str) -> str:
        return repo_url.replace(
            "https://github.com/", f"https://{self.github_token}@github.com/"
        )
