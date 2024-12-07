import os
from typing import Optional

from dotenv import load_dotenv
from git import GitCommandError, Repo

from repo_tool.core.contants import REPO_DIR
from repo_tool.core.logger import log_error

load_dotenv()


def download_repo(
    repo_url: str,
    repo_id: str,
    branch: Optional[str] = None,
) -> None:
    """
    Download a GitHub repository using GitPython.

    Args:
        repo_url: GitHub repository URL
        repo_id: Unique identifier for the repository
        branch: Optional branch name to clone

    Raises:
        ValueError: If the repository URL is invalid
        RuntimeError: If there's an error during cloning
    """
    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR, exist_ok=True)

    repo_path = os.path.join(REPO_DIR, repo_id)
    if os.path.exists(repo_path):
        return

    if not repo_url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub repository URL.")

    # Add GitHub token if available
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        repo_url = repo_url.replace(
            "https://github.com/", f"https://{github_token}@github.com/"
        )

    try:
        Repo.clone_from(
            url=repo_url,
            to_path=repo_path,
            depth=1,
            branch=branch if branch else None,
        )
    except GitCommandError as e:
        log_error(e)
        raise RuntimeError(f"Error during repository cloning: {e}")


def calculate_repo_id(repo_url: str) -> str:
    return repo_url.split("/")[-1].replace(".git", "").replace("/", "_")
