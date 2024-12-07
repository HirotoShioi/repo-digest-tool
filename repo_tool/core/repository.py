import os
import subprocess
from typing import Optional

from dotenv import load_dotenv

from repo_tool.core.contants import REPO_DIR
from repo_tool.core.logger import log_error

load_dotenv()


def download_repo(
    repo_url: str,
    repo_id: str,
    branch: Optional[str] = None,
):
    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR, exist_ok=True)
    # if repo exists, skip cloning
    if os.path.exists(f"{REPO_DIR}/{repo_id}"):
        return
    if not repo_url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub repository URL.")
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        repo_url = repo_url.replace(
            "https://github.com/", f"https://{github_token}@github.com/"
        )
    cmd = ["git", "clone", "--depth=1"]
    if branch:
        cmd.extend(["--branch", branch])
    cmd.extend([repo_url, f"{REPO_DIR}/{repo_id}"])

    try:
        subprocess.run(cmd, check=True, text=True)
    except subprocess.CalledProcessError as e:
        log_error(e)
        raise RuntimeError(f"Error during repository cloning: {e}")


def calculate_repo_id(repo_url: str) -> str:
    return repo_url.split("/")[-1].replace(".git", "").replace("/", "_")
