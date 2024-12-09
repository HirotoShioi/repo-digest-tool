import streamlit as st

from repo_tool.core import GitHub, Repository

github = GitHub()


# Function to get repository details
def get_repositories() -> list[Repository]:
    return github.list()


# Add custom CSS to reduce the padding
# Load custom CSS from file
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

# Repository Management Page
if page == "Repository Management":
    st.subheader("Manage Repositories")

    repos = get_repositories()
    if not repos:
        st.warning("No repositories found.")

    # Search input
    search_query = st.text_input("Search repositories by name or author:", "")
    filtered_repos = [
        repo
        for repo in repos
        if search_query.lower() in repo.name.lower()
        or search_query.lower() in repo.author.lower()
    ]

    if filtered_repos:
        # Display repositories in a table
        st.table(
            [
                {
                    "Name": repo.name,
                    "URL": repo.url,
                    "Author": repo.author,
                    "Last Updated": repo.updated_at,
                }
                for repo in filtered_repos
            ]
        )
    else:
        st.warning("No repositories match your search query.")
