from datetime import datetime
from typing import Optional

import humanize
import typer
from git.exc import GitCommandError
from rich import box
from rich.console import Console
from rich.table import Table
from typer import Typer

from repo_tool.core.digest import generate_digest
from repo_tool.core.github import GitHub

app = Typer()

github = GitHub()


@app.command(name="add")
def add(
    repo_url: str = typer.Argument(..., help="GitHub repository URL"),
    branch: Optional[str] = typer.Option(None, help="Branch to add"),
    force: bool = typer.Option(False, help="Force re-download if exists"),
) -> None:
    """
    Add a GitHub repository to the tool.
    """
    try:
        typer.secho(f"Adding repository {repo_url}...")
        github.clone(repo_url, branch, force)
        typer.secho(f"Repository {repo_url} was successfully added!")
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
    table = Table(box=box.SIMPLE)
    table.add_column("Repository Name", justify="left")
    table.add_column("Author", justify="left")
    table.add_column("URL", justify="left")
    table.add_column("Branch", justify="left")
    table.add_column("Last Updated", justify="left", width=20)
    table.add_column("Size", justify="right")

    # Populate the table with repository data
    for repo in repos:
        formatted_time = humanize.naturaltime(datetime.now() - repo.updated_at)
        size = humanize.naturalsize(repo.size)
        table.add_row(
            repo.name,
            repo.author,
            repo.url,
            repo.branch or "N/A",
            formatted_time,
            size,
        )

    # Print the table
    console.print(table)


@app.command(name="remove")
def remove(repo_name: str = typer.Argument(..., help="Repository name")) -> None:
    """
    Remove a repository.
    """
    try:
        repo_exists = github.repo_exists(repo_name)
        if not repo_exists:
            typer.secho(f"Repository {repo_name} not found.", fg=typer.colors.RED)
            return
        github.remove(repo_name)
        typer.secho(f"Repository {repo_name} removed successfully!")
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED)
        raise typer.Abort() from e


@app.command(name="clean")
def clean() -> None:
    """
    Clean up all repositories.
    """
    github.clean()


@app.command(name="update")
def update(
    repo_url: Optional[str] = typer.Argument(None, help="Repository URL")
) -> None:
    """
    Update a repository.
    """
    try:
        updated_repos = github.update(repo_url)
        if len(updated_repos) == 0:
            typer.secho("No repositories updated.", fg=typer.colors.YELLOW)
        else:
            for repo in updated_repos:
                typer.secho(f"Updated repository: {repo.name}")
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED)
        raise typer.Abort() from e


@app.command(name="digest")
def digest(
    repo_url: str = typer.Argument(..., help="Repository URL"),
    branch: Optional[str] = typer.Option(None, help="Branch to generate digest for"),
    prompt: Optional[str] = typer.Option(None, help="Prompt to generate digest with"),
) -> None:
    """
    Generate a digest for a repository.
    """
    try:
        repo_path = github.get_repo_path(repo_url)
        if not github.repo_exists(repo_url):
            typer.secho(f"Repository {repo_url} not found. Cloning...")
            github.clone(repo_url, branch)
        elif branch:
            github.checkout(repo_path, branch)
        generate_digest(repo_path, prompt)
        typer.secho(
            f"Digest generated successfully at digests/{repo_path.name}.txt",
        )
    except Exception as e:
        typer.secho(f"An unexpected error occurred: {e}", fg=typer.colors.RED)
        raise typer.Abort() from e


if __name__ == "__main__":
    app()
