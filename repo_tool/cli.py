from typing import Optional
from urllib.parse import urlparse

import typer
from git.exc import GitCommandError
from typer import Typer

from repo_tool.core.github import GitHub

app = Typer()

github = GitHub()


def is_valid_repo_url(url: str) -> bool:
    """
    Validate if the given URL is a valid GitHub repository URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.scheme == "https" and "github.com" in parsed_url.netloc


@app.command(name="add")
def add(
    repo_url: str = typer.Argument(..., help="GitHub repository URL"),
    branch: Optional[str] = typer.Option(None, help="Branch to add"),
    force: bool = typer.Option(False, help="Force re-download if exists"),
) -> None:
    """
    Add a GitHub repository to the tool.
    """
    if not is_valid_repo_url(repo_url):
        typer.secho("Invalid GitHub repository URL.", fg=typer.colors.RED)
        raise typer.Abort()
    try:
        typer.secho(f"Adding repository {repo_url}...", fg=typer.colors.YELLOW)
        github.clone(repo_url, branch, force)
        typer.secho(f"Repository {repo_url} added successfully!", fg=typer.colors.GREEN)
    except GitCommandError as e:
        typer.secho(f"Git error: {e}", fg=typer.colors.RED)
        raise typer.Abort() from e
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED)
        raise typer.Abort() from e


if __name__ == "__main__":
    app()
