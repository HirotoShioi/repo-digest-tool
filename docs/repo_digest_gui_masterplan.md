### 更新された **masterplan.md**

以下は、新しい画面構成を反映した **masterplan.md** の更新版です。

---

## **masterplan.md**

### **App Overview**

- **Name**: Repo Digest Viewer
- **Objective**:  
  Provide an intuitive UI to manage local repositories, visualize repository content, and generate digest files. This app focuses on simplifying repository management and offering actionable insights through visualization and filtering.

---

### **Target Audience**

- Software engineers and project managers.
- Users who want to efficiently manage and understand the structure and content of Git repositories.

---

### **Core Features**

1. **Repository Management** (Management Page):
   - View a list of locally available repositories.
   - Add new repositories by cloning from a Git URL.
   - Delete existing repositories.
   - Update repositories to pull the latest changes.
2. **Repository Details** (Details Page):
   - View repository metadata (file count, total size, last updated, etc.).
   - Visualize file distribution by size and type using charts.
   - Filter files by extension, size range, and other criteria.
   - Generate a digest file summarizing selected files.
   - Download the digest file.

---

### **Technical Stack**

- **Frontend**: Streamlit
- **Backend**: Python
  - Data handling: Pandas
  - File operations: pathlib
  - Git operations: GitPython
  - Charting: Altair
- **Dependencies**:
  - `streamlit`
  - `pandas`
  - `altair`
  - `gitpython`

---

### **Conceptual Data Model**

```yaml
Repository:
  - name: string
  - path: string
  - last_updated: datetime
  - files: List[File]

File:
  - name: string
  - path: string
  - size: int (in bytes)
  - extension: string
```

---

### **UI Design**

#### **Repository Management Page**

- **Purpose**: Manage repositories.
- **Components**:
  - List of repositories with details (name, path, last updated).
  - Buttons for:
    - Adding a repository (clone from Git URL).
    - Deleting a repository.
    - Updating a repository.

#### **Repository Details Page**

- **Purpose**: Explore repository contents and generate digests.
- **Components**:
  - Repository metadata (total files, total size, etc.).
  - File distribution charts (size and type).
  - Filters:
    - By extension.
    - By file size range.
  - Digest generation and download.

---

### **Directory Structure**

```plaintext
repo-digest-tool/
├── app/
│   ├── main.py               # Streamlit entry point
│   ├── components/           # Reusable UI components
│   │   ├── filters.py        # UI for filtering options
│   │   ├── charts.py         # Chart rendering logic
│   │   └── tables.py         # Table rendering logic
│   ├── repository/           # Repository-specific utilities
│   │   ├── operations.py     # Add, remove, update repository
│   │   ├── details.py        # Retrieve repository metadata
│   │   └── digest.py         # Generate digest files
│   └── utils/                # Shared utilities
│       └── file_loader.py    # Load and read files
├── repo_tool/                # Existing CLI logic
│   ├── core/
│   └── cli.py
├── templates/                # Templates for reports
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .streamlit/               # Streamlit configurations
```

---

### **Development Phases**

#### **Phase 1: Repository Management Page**

- List repositories.
- Add, delete, and update repositories.

#### **Phase 2: Repository Details Page**

- Show repository metadata.
- Display file distribution charts.

#### **Phase 3: Filtering and Digest Generation**

- Add file filters.
- Implement digest file generation and download.

#### **Phase 4: UI Refinements**

- Improve user feedback (progress bars, notifications).
- Enhance design and layout for better usability.

---

### **Challenges and Solutions**

1. **Handling Large Repositories**:
   - Batch processing and caching for better performance.
   - Asynchronous file loading with progress feedback.
2. **Error Handling**:
   - Log errors for repository operations and file processing.
   - Provide clear feedback to users.
3. **Extensibility**:
   - Modularize the codebase for adding new features (e.g., additional visualization).

---

### **Future Extensions**

- Add compatibility with other platforms (GitLab, Bitbucket).
- Integrate file content summarization using LLMs.
- Extend repository insights with detailed metrics and history tracking.
