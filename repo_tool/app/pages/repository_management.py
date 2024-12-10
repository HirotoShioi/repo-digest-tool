from datetime import datetime

import humanize
import streamlit as st

from repo_tool.core import GitHub, Repository

github = GitHub()


def get_repositories() -> list[Repository]:
    return github.list()


def delete_repository(repo_name: str) -> tuple[bool, str]:
    try:
        github.remove(repo_name)
        return True, f"Repository '{repo_name}' deleted successfully!"
    except Exception as e:
        return False, f"Error deleting repository: {e}"


def clone_repository(repo_url: str) -> tuple[bool, str]:
    try:
        github.clone(repo_url)
        return True, f"Repository '{repo_url}' cloned successfully!"
    except Exception as e:
        return False, f"Error cloning repository: {e}"


def show_repository_management_page() -> None:
    st.subheader("Manage Repositories")

    # Add repository section
    st.write("### Add a Repository")
    repo_url = st.text_input("Enter Git URL of the repository to clone:")
    if st.button("Clone Repository"):
        if repo_url:
            success, message = clone_repository(repo_url)
            if success:
                st.toast(message, icon="✅")
                st.session_state.repos = (
                    get_repositories()
                )  # Refresh the repository list
            else:
                st.error(message)
        else:
            st.warning("Please enter a valid Git URL.")

    # Display existing repositories
    st.write("### Repositories")
    repos = st.session_state.repos
    if not repos:
        st.warning("No repositories found.")
    else:
        # Add search filter
        search_term = st.text_input(
            "Search repositories",
            placeholder="Filter by name, URL, or author...",
            key="search_repos",
        ).lower()

        # Filter repositories based on search term
        filtered_repos = repos
        if search_term:
            filtered_repos = [
                repo
                for repo in repos
                if search_term in repo.name.lower()
                or search_term in repo.url.lower()
                or search_term in repo.author.lower()
            ]

        if not filtered_repos:
            st.info("No repositories match your search.")
        else:
            # Create columns for the table header
            cols = st.columns([2, 3, 2, 2, 1])
            cols[0].write("**Name**")
            cols[1].write("**URL**")
            cols[2].write("**Author**")
            cols[3].write("**Last Updated**")
            cols[4].write("**Actions**")

            # Display repository data
            for repo in filtered_repos:
                cols = st.columns([2, 3, 2, 2, 1])
                cols[0].write(repo.name)
                cols[1].write(repo.url)
                cols[2].write(repo.author)
                cols[3].write(humanize.naturaltime(datetime.now() - repo.updated_at))
                if cols[4].button("Delete", key=f"delete-{repo.name}"):
                    success, message = delete_repository(repo.url)
                    if success:
                        st.session_state.repos = get_repositories()
                        st.toast(message, icon="✅")
                        st.rerun()
                    else:
                        st.error(message)
