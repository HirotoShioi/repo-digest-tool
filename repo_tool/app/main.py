import streamlit as st

from repo_tool.app.pages.repository_management import (
    get_repositories,
    show_repository_management_page,
)


# Add custom CSS to reduce the padding
def load_css(file_path: str) -> None:
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS file
css_file_path = "./repo_tool/app/static/styles.css"
load_css(css_file_path)

# App title
st.title("Repo Digest Viewer")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Repository Management"])

# Initialize session state for repositories
if "repos" not in st.session_state:
    st.session_state.repos = get_repositories()  # type: ignore

# Show selected page
if page == "Repository Management":
    show_repository_management_page()  # type: ignore
