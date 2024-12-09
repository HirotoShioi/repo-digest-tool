import streamlit as st

# App title
st.title("Repo Digest Viewer")

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Choose a page", ["Repository Selection", "Visualization", "Digest Generation"]
)

# Pages
if page == "Repository Selection":
    st.subheader("Step 1: Select a Repository")
    st.text("List available repositories here.")
elif page == "Visualization":
    st.subheader("Step 2: Visualize Repository Data")
    st.text("Display charts and stats here.")
elif page == "Digest Generation":
    st.subheader("Step 3: Generate Digest File")
    st.text("Generate and download digest file here.")
