from typing import Optional
import os
import subprocess
from lib.logger import log_error
from dotenv import load_dotenv

load_dotenv()


def download_repo(
    repo_url: str,
    repo_id: str,
    branch: Optional[str] = None,
):
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
    cmd.extend([repo_url, f"tmp/{repo_id}"])

    try:
        subprocess.run(cmd, check=True, text=True)
    except subprocess.CalledProcessError as e:
        log_error(e)
        raise RuntimeError(f"Error during repository cloning: {e}")
