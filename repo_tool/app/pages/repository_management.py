from datetime import datetime
from typing import List, Tuple

import gradio as gr  # type: ignore
import humanize

from repo_tool.core import GitHub, Repository

github = GitHub()


def get_repositories() -> List[Repository]:
    return github.list()


def delete_repository(repo_name: str) -> Tuple[bool, str]:
    try:
        github.remove(repo_name)
        return True, f"Repository '{repo_name}' deleted successfully!"
    except Exception as e:
        return False, f"Error deleting repository: {e}"


def clone_repository(repo_url: str) -> Tuple[bool, str]:
    try:
        github.clone(repo_url)
        return True, f"Repository '{repo_url}' cloned successfully!"
    except Exception as e:
        return False, f"Error cloning repository: {e}"


def filter_repositories(search_term: str, repos: List[Repository]) -> List[Repository]:
    if not search_term:
        return repos

    search_term = search_term.lower()
    return [
        repo
        for repo in repos
        if search_term in repo.name.lower()
        or search_term in repo.url.lower()
        or search_term in repo.author.lower()
    ]


def format_repository_table(repos: List[Repository]) -> List[List[str]]:
    """Format repository data for the table component"""
    return [
        [
            repo.name,
            repo.url,
            repo.author,
            humanize.naturaltime(datetime.now() - repo.updated_at),
        ]
        for repo in repos
    ]


def create_repository_management_tab() -> gr.Blocks:
    with gr.Blocks() as repository_tab:
        gr.Markdown("## Repository Management")

        # Add repository section
        with gr.Group():
            gr.Markdown("### Add a Repository")
            repo_url_input = gr.Textbox(
                label="Git Repository URL",
                placeholder="Enter the repository URL to clone",
            )
            clone_btn = gr.Button("Clone Repository")
            clone_status = gr.Markdown()

        # Repository list section
        with gr.Group():
            gr.Markdown("### Repositories")
            search_input = gr.Textbox(
                label="Search repositories",
                placeholder="Filter by name, URL, or author...",
            )

            # Repository table
            repo_table = gr.Dataframe(
                headers=["Name", "URL", "Author", "Last Updated"],
                interactive=False,
                wrap=True,
            )

            refresh_btn = gr.Button("Refresh List")

        def handle_clone(url: str) -> str:
            if not url:
                return "Please enter a valid Git URL."

            success, message = clone_repository(url)
            if success:
                # Refresh the table data
                repos = get_repositories()
                repo_table.update(value=format_repository_table(repos))
                return f"✅ {message}"
            return f"❌ {message}"

        def update_table(search_term: str = "") -> List[List[str]]:
            repos = get_repositories()
            filtered_repos = filter_repositories(search_term, repos)
            return format_repository_table(filtered_repos)

        # Event handlers
        clone_btn.click(
            fn=handle_clone, inputs=[repo_url_input], outputs=[clone_status]
        )

        search_input.change(
            fn=update_table, inputs=[search_input], outputs=[repo_table]
        )

        refresh_btn.click(fn=update_table, inputs=[search_input], outputs=[repo_table])

        # Initial table load
        repo_table.update(value=format_repository_table(get_repositories()))

    return repository_tab
