import datetime
import os
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse, urlunparse

from git import GitCommandError, Repo

from repo_tool.core.logger import log_error

REPO_DIR = "repo"


@dataclass
class Repository:
    url: str
    branch: Optional[str]
    path: Path
    updated_at: datetime.datetime
    name: str
    author: str
    size: int = 0

    def has_update(self) -> bool:
        repo = Repo(self.path)
        origin = repo.remotes.origin
        origin.fetch()
        local_commit = repo.head.commit.hexsha
        remote_commit: str = origin.refs[repo.active_branch.name].commit.hexsha
        return local_commit != remote_commit


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
            repo_url = GitHub.resolve_repo_url(repo_url)
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
        shutil.rmtree(repo_path, ignore_errors=True)
        author_path = repo_path.parent

        # Check if the author directory exists before attempting to list its contents
        if os.path.exists(author_path) and not os.listdir(author_path):
            shutil.rmtree(author_path, ignore_errors=True)

    def clean(self) -> None:
        """
        Delete all repositories.
        """
        shutil.rmtree(REPO_DIR, ignore_errors=True)

    def update(self, repo_url: Optional[str] = None) -> List[Repository]:
        """
        Update one or all repositories.

        Args:
            repo_url (Optional[str]): Specific repository URL to update. If None, updates all repositories.

        Returns:
            List[Repository]: List of updated repositories
        """
        if repo_url:
            # Update single repository
            repo_url = self.resolve_repo_url(repo_url)
            self._update_single(repo_url)
            return [repo for repo in self.list() if repo.url == repo_url]
        else:
            # Update all repositories in parallel
            repositories = self.list()
            repositories = [repo for repo in repositories if repo.has_update()]
            if not repositories:
                return repositories

            print(f"Updating {len(repositories)} repositories...")
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(self._update_single, repo.url)
                    for repo in repositories
                ]
                for future in futures:
                    try:
                        future.result()  # Wait for each task to complete
                    except Exception as e:
                        print(f"Error updating repository: {e}")
            return repositories

    def _update_single(self, repo_url: str) -> None:
        """
        Update a single repository.
        """
        repo_path = self.get_repo_path(repo_url)
        if not os.path.exists(repo_path):
            raise ValueError(f"Repository does not exist: {repo_url}")
        repo = Repo(repo_path)
        repo.remotes.origin.pull()
        print(f"Updated repository: {repo_url}")

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
    def get_repo_path(url: str) -> Path:
        """
        Generate the local repository path from a GitHub URL.

        Args:
            url: GitHub repository URL

        Returns:
            Path object representing the local repository path

        Raises:
            ValueError: If the URL is invalid
        """
        url = GitHub.resolve_repo_url(url)
        if not GitHub.is_valid_repo_url(url):
            raise ValueError("Invalid repository URL")

        # Extract author and repo name from URL
        # Remove .git extension if present
        match = re.match(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?$", url)
        if not match:
            raise ValueError("Invalid repository URL")

        author, repo_name = match.groups()

        # Create path using the REPO_DIR constant
        return Path(REPO_DIR) / author / repo_name

    @staticmethod
    def is_valid_repo_url(url: str) -> bool:
        """
        Validate if the given URL is a valid GitHub repository URL.

        Args:
            url: URL to validate

        Returns:
            bool: True if URL is valid, False otherwise
        """
        # First check basic URL structure
        if not url.startswith("https://github.com/"):
            return False

        # Extract path after github.com/
        path = url.replace("https://github.com/", "")

        # Split into author and repo parts
        parts = path.split("/")
        if len(parts) != 2:
            return False

        author, repo = parts

        # Remove .git extension if present
        repo = repo.removesuffix(".git")

        # Check for security issues and valid characters
        if (
            ".." in author
            or ".." in repo  # Prevent directory traversal
            or "?" in author
            or "?" in repo  # Prevent query strings
            or "*" in author
            or "*" in repo  # Prevent wildcards
            or "[" in author
            or "[" in repo  # Prevent special characters
            or "]" in author
            or "]" in repo
            or "\\" in author
            or "\\" in repo
            or not author
            or not repo  # Ensure non-empty strings
            or not re.match(r"^[a-zA-Z0-9][-\w.]*$", author)  # Validate author format
            or not re.match(r"^[-\w.]+$", repo)  # Validate repo format
        ):
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

    def repo_exists(self, repo_url: str) -> bool:
        """
        Check if a repository exists.
        """
        repo_path = self.get_repo_path(repo_url)
        return os.path.exists(repo_path)

    def checkout(self, repo_path: Path, branch: Optional[str] = None) -> None:
        """
        Checkout a branch in a repository.
        """
        repo = Repo(repo_path)
        repo.git.checkout(branch if branch else repo.active_branch.name)

    @staticmethod
    def resolve_repo_url(repo_url: str) -> str:
        """
        Resolves a short-form GitHub repository URL (e.g., "author/repo-name")
        to a full URL (e.g., "https://github.com/author/repo-name").

        Args:
            repo_url (str): The short-form or full repository URL.

        Returns:
            str: The full repository URL.
        """
        if repo_url.startswith("https://github.com"):
            # 完全なURLはそのまま返す
            return repo_url

        # 正規表現で短縮形式を検証
        short_url_pattern = r"^(?!.*\.\.)[a-zA-Z0-9][a-zA-Z0-9\-\.]{0,38}/[a-zA-Z0-9][a-zA-Z0-9\-\.]{0,100}(\.git)?$"
        if re.match(short_url_pattern, repo_url):
            return f"https://github.com/{repo_url}"
        else:
            raise ValueError(
                "Invalid short-form repository URL. Must match 'author/repo-name' format."
            )
