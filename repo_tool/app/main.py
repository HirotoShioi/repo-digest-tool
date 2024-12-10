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
                st.success(message)
                st.session_state.repos = (
                    get_repositories()
                )  # Refresh the repository list
            else:
                st.error(message)
        else:
            st.warning("Please enter a valid Git URL.")

    # Display existing repositories
    st.write("### Existing Repositories")
    repos = st.session_state.repos
    if not repos:
        st.warning("No repositories found.")

    # Display repositories in a table with delete buttons
    for repo in repos:
        col1, col2, col3, col4, col5 = st.columns([2, 3, 3, 2, 2])
        col1.write(repo.name)
        col2.write(repo.url)
        col3.write(repo.author)
        col4.write(repo.updated_at)

        # Add a delete button for each repository
        if col5.button("Delete", key=f"delete-{repo.name}"):
            success, message = delete_repository(repo.url)
            if success:
                st.session_state.repos = (
                    get_repositories()
                )  # Refresh the list immediately
                st.success(message)
                st.rerun()  # Force Streamlit to rerun the app
            else:
                st.error(message)
