
# masterplan.md

## App Overview
- **Name**: Repo Digest Viewer  
- **Objective**:  
  Provide an intuitive UI to explore, filter, and generate a digest file summarizing the contents of local Git repositories. The app focuses on simplifying repository analysis and improving user experience.

---

## Target Audience
- Software engineers and project managers.  
- Users who want to quickly understand the structure and content of Git repositories.

---

## Core Features
1. **Repository Selection**:
   - List local repositories and allow the user to select one for processing.
2. **Data Visualization**:
   - Display file statistics such as file size distribution and extension breakdown via charts.
   - Highlight top N files based on size or token count.
3. **Filtering**:
   - Filter files by extension, size range, or token count.
4. **Digest Generation**:
   - Generate a single digest file summarizing selected files' content.
   - Provide a download link for the generated file.
5. **Error Handling**:
   - Log and display errors for files that fail to process.

---

## Technical Stack
- **Frontend**: Streamlit
- **Backend**: Python
  - Data handling: Pandas
  - File operations: pathlib
  - Charting: Altair
- **Dependencies**:
  - `streamlit`
  - `pandas`
  - `altair`

---

## Conceptual Data Model
```yaml
Repository:
  - name: string
  - path: string
  - files: List[File]

File:
  - name: string
  - path: string
  - size: int (in bytes)
  - extension: string
  - tokens: int (optional)
```

---

## UI Design Principles
1. **Intuitive Navigation**:
   - Use a sidebar for setting filters and a main panel for data visualization.
2. **Visual Feedback**:
   - Include progress bars and success/error notifications for user actions.
3. **Flexibility**:
   - Allow users to dynamically adjust filters and instantly see updated results.

---

## Integration with Existing Repository

### 1. Streamlit Directory Structure
Add a new `app/` directory to your repository for Streamlit-related code:
```plaintext
repo-digest-tool/
├── app/
│   ├── main.py               # Streamlit entry point
│   ├── components/           # Reusable UI components
│   │   ├── filters.py        # UI for filtering options
│   │   ├── charts.py         # Chart rendering logic
│   │   └── tables.py         # Table rendering logic
│   └── utils/                # Utility functions
│       ├── file_operations.py  # File loading and processing
│       ├── data_loader.py     # Repository data handling
│       └── session_manager.py  # Session state management
├── repo_tool/                # Existing CLI code
├── templates/                # Digest templates (HTML/Text)
├── requirements.txt          # Streamlit dependencies added
├── README.md                 # Updated usage instructions
└── .streamlit/               # Streamlit configurations
```

### 2. Refactoring CLI Code
Convert CLI logic into reusable functions to be called from Streamlit.

Example:
```python
# repo_tool/core/digest.py
def generate_digest_from_repo(repo_path: str, prompt: Optional[str] = None) -> str:
    # Existing digest generation logic
    digest_path = f"{repo_path}_digest.txt"
    generate_digest(repo_path, prompt)
    return digest_path
```

Streamlit usage:
```python
# app/utils/file_operations.py
from repo_tool.core.digest import generate_digest_from_repo

def generate_digest_ui(repo_path: str, prompt: Optional[str]) -> str:
    return generate_digest_from_repo(repo_path, prompt)
```

---

## High-Level Development Phases

### Phase 1: Initial Features
- Add repository selection in the sidebar.
- Display basic repository stats (e.g., file count, total size).

### Phase 2: Data Visualization
- Show file size and extension breakdown using charts.
- Highlight top N files based on size or token count.

### Phase 3: Filtering and Digest Generation
- Add filtering options for file extensions, size, and token count.
- Implement digest file generation and provide a download link.

### Phase 4: UI Refinements
- Add progress bars and notifications for better user feedback.
- Enhance theme and responsiveness.

---

## Potential Challenges and Solutions
1. **Handling Large Repositories**:
   - Use asynchronous or batched processing for file loading and filtering.
   - Display progress with Streamlit's `st.progress()`.
2. **Error Handling**:
   - Log errors and notify users for files that fail to process.
   - Allow users to download error logs.
3. **User Experience**:
   - Keep the UI responsive and provide immediate feedback on user actions.

---

## Future Extensions
- Use LLMs to summarize file contents.
- Extend compatibility to other platforms like GitLab or Bitbucket.
- Add project-level statistics for better insights.

---

## Updated README Example
```markdown
## Streamlit App Usage

### Starting the App
Run the following command to start the Streamlit app:
```bash
streamlit run app/main.py
```

Open your browser and navigate to `http://localhost:8501`.

### Features
1. Select a local repository for analysis.
2. Visualize file statistics with charts.
3. Filter files by extension, size, or token count.
4. Generate a digest file summarizing selected files.
5. Download the digest file directly from the app.

### Requirements
Install dependencies using:
```bash
pip install -r requirements.txt
```
```
