from datetime import datetime

import humanize
import streamlit as st

from repo_tool.core import GitHub, Repository

github = GitHub()


# Function to get repository details
def get_repositories() -> list[Repository]:
    return github.list()


# Function to delete a repository
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


# Add custom CSS to reduce the padding
def load_css(file_path: str) -> None:
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS file
css_file_path = "./repo_tool/app/static/styles.css"  # Adjust this path as needed
load_css(css_file_path)

# App title
st.title("Repo Digest Viewer")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Repository Management"])

# Initialize session state for repositories
if "repos" not in st.session_state:
    st.session_state.repos = get_repositories()

# Repository Management Page
if page == "Repository Management":
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
            cols = st.columns([2, 3, 2, 2, 1])  # Added column for delete button
            cols[0].write("**Name**")
            cols[1].write("**URL**")
            cols[2].write("**Author**")
            cols[3].write("**Last Updated**")
            cols[4].write("**Actions**")

            # Display repository data
            for repo in filtered_repos:
                cols = st.columns([2, 3, 2, 2, 1])  # Same column layout as header
                cols[0].write(repo.name)
                cols[1].write(repo.url)
                cols[2].write(repo.author)
                cols[3].write(humanize.naturaltime(datetime.now() - repo.updated_at))
                # Add delete button in the last column
                if cols[4].button("Delete", key=f"delete-{repo.name}"):
                    success, message = delete_repository(repo.url)
                    if success:
                        st.session_state.repos = (
                            get_repositories()
                        )  # Refresh the list immediately
                        st.toast(message, icon="✅")
                        st.rerun()
                    else:
                        st.error(message)
