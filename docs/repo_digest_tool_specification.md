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

---

## CLI Command Descriptions

The CLI commands and their functionalities are as follows:

### `repo add <repo_url> [--branch <branch>] [--force]`

- **Description**: Adds a repository to the local storage. Optionally, a specific branch can be checked out. The `--force` option re-downloads the repository if it already exists.
- **Example**:
  ```bash
  repo add https://github.com/honojs/hono
  repo add https://github.com/honojs/hono --branch develop --force
  ```

### `repo remove <repo_url>`

- **Description**: Removes a repository from the local storage.
- **Example**:
  ```bash
  repo remove https://github.com/honojs/hono
  ```

### `repo list`

- **Description**: Lists all locally stored repositories, including details such as URL, branch, and last updated date.
- **Example**:
  ```bash
  repo list
  ```

### `repo digest <repo_url> [--branch <branch>] [--prompt <prompt>] [--force]`

- **Description**: Generates a digest for the specified repository. Optionally allows specifying a branch and a custom prompt for LLM-based filtering. The `--force` option regenerates the digest even if it exists.
- **Example**:
  ```bash
  repo digest https://github.com/honojs/hono
  repo digest https://github.com/honojs/hono --prompt "Focus on APIs"
  ```

### `repo clear [--all | --author <author>]`

- **Description**: Clears repositories from local storage. The `--all` option removes all repositories, while `--author` selectively removes repositories by the specified author.
- **Example**:
  ```bash
  repo clear --all
  repo clear --author honojs
  ```

### `repo update <repo_url>`

- **Description**: Updates the specified repository by pulling the latest changes.
- **Example**:
  ```bash
  repo update https://github.com/honojs/hono
  ```

---

## Directory Structure

```
repo-digest-tool/
├── repo_tool/                  # Main application code
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # CLI entry point
│   ├── core/                   # Core functionalities
│   │   ├── __init__.py         # Submodule initialization
│   │   ├── contants.py         # Constants definition
│   │   ├── digest.py           # Digest generation logic
│   │   ├── filter.py           # File filtering logic
│   │   ├── github.py           # GitHub operations
│   │   ├── llm.py              # LLM-related functionalities
│   │   ├── logger.py           # Logging features
│   │   └── summary.py          # Summary report generation
│   ├── config.py               # Configuration management
├── tests/                      # Test code
│   ├── github_test.py          # Tests for GitHub operations
│   ├── test_digest.py          # Tests for digest generation
│   └── conftest.py             # Shared pytest settings
├── repositories/               # Repository storage directory (generated at runtime)
│   └── (Generated at runtime)
├── digests/                    # Digest storage directory (generated at runtime)
│   └── (Generated at runtime)
├── templates/                  # Templates for reports
│   └── report.html             # HTML template
├── .gitignore                  # Git ignore settings
├── pyproject.toml              # Python project configuration file
├── README.md                   # Project overview and usage
├── LICENSE                     # License
└── requirements.txt            # Required packages
```

---

## Templates

### Purpose of `templates/report.html`

The `templates/report.html` file is used to generate HTML reports summarizing repository statistics and digest results. It serves as the presentation layer for digest outputs, formatted for readability.

---

## LLM Functionality

The tool leverages a Language Learning Model (LLM) to filter files based on relevance. This is particularly useful for large repositories where only specific types of files are needed.

### How LLM Filtering Works:

1. **Input Prompt**: Users can provide a custom prompt describing the filtering criteria.
2. **File Evaluation**: The LLM processes a list of file paths and their metadata to determine relevance.
3. **Batch Processing**: Files are evaluated in batches for efficiency.

### Use Cases:

- Filtering out CI/CD files, configuration files, and binaries.
- Selecting only files relevant for API documentation, tutorials, or code reviews.

### Example Prompts:

- "Focus on API implementation and tests."
- "Exclude CI/CD files and binary outputs. Include Python and Markdown files."

### Advantages:

- **Precision**: Filters files based on user-defined criteria.
- **Adaptability**: Handles different repository structures and use cases.

### Example Workflow:

```bash
repo digest https://github.com/honojs/hono --prompt "Focus on API implementation"
```

Output:

```
Filtered 100 files to 20 relevant files based on the given prompt.
Digest generated: digests/hono_digest.txt
```

---
