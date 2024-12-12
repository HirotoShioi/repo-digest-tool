## App Overview

- **Name**: Repo Digest Viewer
- **Objective**:  
  Provide an intuitive UI to manage local repositories using a React frontend and a Python API backend. This architecture separates the presentation layer from the logic, improving scalability and modularity.

---

## Target Audience

- Software engineers and project managers.
- Users who want to efficiently manage and understand the structure and content of Git repositories.

---

## Core Features

1. **Repository Management** (Frontend + Backend API):
   - View a list of locally available repositories.
   - Add new repositories by cloning from a Git URL.
   - Delete existing repositories.
   - Update repositories to pull the latest changes.
2. **Repository Details** (Frontend + Backend API):
   - View repository metadata (file count, total size, last updated, etc.).
   - Visualize file distribution by size and type using charts.
   - Filter files by extension, size range, and other criteria.
   - Generate a digest file summarizing selected files.
   - Download the digest file.

---

## Technical Stack

- **Frontend**: React (TypeScript, Axios, React Router, Tailwind CSS)
- **Backend**: Python (FastAPI, GitPython)
- **Charting**: Altair
- **Dependencies**:
  - Frontend:
    - `axios`, `react-router-dom`, `tailwindcss`
  - Backend:
    - `fastapi`, `uvicorn`, `gitpython`

---

## Conceptual Data Model

### Repository

```yaml
id: int
name: string
path: string
last_updated: datetime
files: List[File]
```

### File

```yaml
name: string
path: string
size: int (in bytes)
extension: string
```

---

## API Design

### Endpoints

1. **Repository Management**:
   - `GET /repositories`: Retrieve a list of local repositories.
   - `POST /repositories`: Clone a new repository.
   - `DELETE /repositories/{id}`: Delete an existing repository.
   - `PUT /repositories/{id}`: Update a repository (pull changes).
2. **Digest Operations**:
   - `POST /digest`: Generate a digest file based on filtering criteria.
   - `GET /digest/{id}`: Retrieve the generated digest file.

---

## Directory Structure

```plaintext
repo-digest-tool/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # Reusable React components
│   │   ├── pages/            # Page-specific components
│   │   ├── services/         # API service calls
│   │   └── App.tsx           # Root React component
│   ├── public/
│   │   └── index.html        # HTML template
│   └── package.json          # Frontend dependencies
├── backend/                  # Python API server
│   ├── app/
│   │   ├── api/
│   │   │   ├── repository.py # Repository management APIs
│   │   │   ├── digest.py     # Digest operations APIs
│   │   ├── main.py           # FastAPI entry point
│   │   └── utils.py          # Shared utilities
│   ├── requirements.txt      # Backend dependencies
│   └── Dockerfile            # Backend Docker configuration
└── README.md                 # Project documentation
```

---

## Development Phases

### Phase 1: API Server Development

- Implement `GET`, `POST`, `DELETE`, `PUT` endpoints for repository management.
- Add `POST` and `GET` endpoints for digest operations.

### Phase 2: Frontend Prototyping

- Create repository management UI:
  - Display list of repositories.
  - Allow repository addition, deletion, and updates.
- Implement React Router for navigation.

### Phase 3: Data Visualization and Digest Generation

- Build repository details page:
  - Show metadata (file count, total size).
  - Visualize file distribution using charts.
- Add filtering and digest generation capabilities.

### Phase 4: UI Refinements

- Enhance design with Tailwind CSS.
- Improve user feedback with notifications and progress indicators.

---

## Challenges and Solutions

1. **API Performance**:
   - Use caching for frequently accessed data.
   - Optimize large file processing with asynchronous operations.
2. **Error Handling**:
   - Add detailed error messages for API failures.
   - Validate user input on both frontend and backend.
3. **Scalability**:
   - Use Docker for deployment.
   - Ensure the backend is stateless for horizontal scaling.

---

## Future Extensions

- Add support for other repository platforms (e.g., GitLab, Bitbucket).
- Implement LLM-based file content summarization.
- Provide advanced repository analytics.

---
