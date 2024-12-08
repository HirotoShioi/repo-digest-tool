from typing import Optional

import typer
from typer import Typer

from repo_tool.core.github import GitHub

app = Typer()


github = GitHub()


@app.command()
def add(
    repo_url: str = typer.Argument(..., help="GitHub repository URL"),
    branch: Optional[str] = typer.Option(None, help="Branch to add"),
    force: bool = typer.Option(False, help="Force re-download if exists"),
) -> None:
    """
    Add a GitHub repository to the tool.
    """
    try:
        typer.secho(f"Adding repository {repo_url}...", fg=typer.colors.YELLOW)
        github.clone(repo_url, branch, force)
        typer.secho(f"Repository {repo_url} added successfully", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Error adding repository: {e}", fg=typer.colors.RED)
        raise typer.Abort() from e


if __name__ == "__main__":
    app()
