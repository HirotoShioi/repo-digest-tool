from typing import Optional
from urllib.parse import urlparse

import typer
from git.exc import GitCommandError
from rich.console import Console
from rich.table import Table
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


@app.command(name="list")
def list() -> None:
    """
    List all added repositories in a pretty table format.
    """
    repos = github.list()
    console = Console()

    if not repos:
        console.print("No repositories added yet.")
        return

    # Create a table
    table = Table()
    table.add_column("Repository Name", justify="left")
    table.add_column("URL", justify="left")
    table.add_column("Author", justify="left")
    table.add_column("Branch", justify="left")
    table.add_column("Last Updated", justify="left", width=20)
    table.add_column("Size", justify="right")

    # Populate the table with repository data
    for repo in repos:
        table.add_row(
            repo.name,
            repo.url,
            repo.author,
            repo.branch or "N/A",
            repo.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            str(repo.size),
        )

    # Print the table
    console.print(table)


if __name__ == "__main__":
    app()
