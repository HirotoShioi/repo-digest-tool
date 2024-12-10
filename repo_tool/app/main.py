import gradio as gr  # type: ignore

from repo_tool.app.pages.repository_management import get_repositories
from repo_tool.core import Repository


def init_repositories() -> list[Repository]:
    """Initialize repositories state"""
    return get_repositories()


def show_repository_management() -> gr.Dataframe:
    """Repository management interface"""
    repos = init_repositories()
    # Display repositories in a table format
    return gr.Dataframe(
        value=[[repo.name, repo.url, repo.branch] for repo in repos],
        headers=["Name", "URL", "Branch"],
    )


# Create Gradio interface
with gr.Blocks(title="Repo Digest Viewer", theme=gr.themes.Soft()) as app:
    gr.Markdown("# Repo Digest Viewer")

    with gr.Tab("Repository Management"):
        show_repository_management()

if __name__ == "__main__":
    app.launch()
