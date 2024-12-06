# Repo Digest Tool Development Plan

## Overview

This is a CLI application for managing repositories and generating digests, implemented using Typer. The tool provides the following features:

---

## Requirements

### Features

1. **Repository Digest Generation**
   - Digests are saved in the `digests` directory.
   - Example: `digests/honojs_hono_digest.txt`
2. **Repository Management**
   - Repositories are saved in the `repo` directory.
   - Provides commands to add, remove, and list repositories.
3. **CLI Command Structure**
   ```
   repo
   ├── add <repo_url> [--branch <branch>] [--force]
   ├── remove <repo_url>
   ├── list
   ├── digest <repo_url> [--branch <branch>] [--prompt <prompt>] [--force]
   ├── clear [--all | --author <author>]
   └── update <repo_url>
   ```

### Input Specifications

- **Definition of `repo_id`**
  - Format: `{author/organization}@{repo_name}`
  - Example: `https://github.com/honojs/hono` → `honojs@hono`
- **Options**
  - `--force`: Force re-download of a repository.
  - `--branch`: Specify a branch for operations.
  - `--prompt`: Provide a custom prompt for digest generation.
  - `--update`: Update a branch
  - `--checkout`: Checkout to specific branch

---

## Directory Structure

```
repo-digest-tool/
├── repo_tool/                  # Main application code
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # CLI entry point
│   ├── core/
│   │   ├── repository.py       # Repository operations (add/remove/list)
│   │   ├── digest.py           # Digest generation logic
│   │   ├── metadata.py         # Metadata management
│   │   ├── utils.py            # Utility functions
│   │   └── __init__.py         # Submodule initialization
│   └── config.py               # Configuration management
├── tests/                      # Test code
│   ├── test_cli.py             # CLI unit tests
│   ├── test_repository.py      # Repository operations tests
│   ├── test_digest.py          # Digest generation tests
│   └── conftest.py             # pytest shared settings
├── repo/                       # Repository storage directory
│   └── (Generated at runtime)
├── digests/                    # Digest storage directory
│   └── (Generated at runtime)
├── .gitignore                  # Git ignore settings
├── pyproject.toml              # Python project configuration file
├── README.md                   # Project overview and usage
├── LICENSE                     # License
└── requirements.txt            # Required packages
```

---

## How to Run the CLI

### 1. Direct Execution Locally

Run `repo_tool/cli.py` directly:

```bash
python repo_tool/cli.py add https://github.com/honojs/hono
```

### 2. Run as a Package

#### Setup Instructions

1. **Configure `pyproject.toml`**

   ```toml
   [project]
   name = "repo-digest-tool"
   version = "0.1.0"
   description = "A CLI tool for managing repositories and generating digests."
   authors = ["Hiroto Shoi"]
   dependencies = ["typer[all]", "gitpython"]

   [build-system]
   requires = ["setuptools", "wheel"]
   build-backend = "setuptools.build_meta"

   [project.scripts]
   repo = "repo_tool.cli:app"
   ```

2. **Install Locally**

   ```bash
   pip install -e .
   ```

3. **Run the CLI**
   ```bash
   repo add https://github.com/honojs/hono
   repo list
   repo digest https://github.com/honojs/hono
   ```

### 3. Quick Execution During Development

Run as a Python module:

```bash
python -m repo_tool.cli add https://github.com/honojs/hono
```

---

## Development Roadmap

### **Phase 1: Basic Functionality**

- **Duration**: 1–2 weeks
- **Tasks**:
  1. Implement `add`, `remove`, and `list` commands.
  2. Add conversion logic for `repo_id` and `repo_url` in `utils.py`.
  3. Initialize directory structures (`repo`, `digests`).

### **Phase 2: Digest Generation**

- **Duration**: 1–2 weeks
- **Tasks**:
  1. Implement the `digest` command.
  2. Develop flexible digest generation logic that supports prompts.
  3. Add error handling and debugging logs.

### **Phase 3: Testing and Documentation**

- **Duration**: 1 week
- **Tasks**:
  1. Set up unit tests using `pytest`.
  2. Create detailed CLI command help documentation.
  3. Add usage examples in `README.md`.

### **Phase 4: Extensions and Optimization**

- **Duration**: 2+ weeks
- **Tasks**:
  1. Add an update feature (`git pull`).
  2. Implement automatic removal of old cache.
  3. Consider supporting other repository services (GitLab, Bitbucket).

---

## Additional Considerations

1. **Repository State Management**
   - Save metadata (e.g., registration date, last update date, size).
   - Recover corrupted repositories.
2. **Lightweight Updates via `git pull`**
   - Allow updates without re-cloning repositories.
3. **Batch Operations**
   - Enable bulk deletion or updates.
4. **Cache Management**
   - Remove old repositories or digests.
5. **Error Handling**
   - Provide detailed error messages.
6. **Logging**
   - Record operation history and errors.

---

## Scalability

- Support for other repository services (e.g., GitLab, Bitbucket).
- Improved filtering for specific directories or file extensions.
- Enhanced digest generation logic.
