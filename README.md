# Repo Digest Tool

A CLI tool for managing GitHub repositories and generating digest summaries, implemented with Typer.

---

## Features

- **Repository Digest Generation**: Creates digests of repositories and stores them in the `digests/` directory.
- **Repository Management**: Add, remove, update, or list repositories stored locally in the `repositories/` directory.
- **Custom Filtering**: Uses an LLM (Language Learning Model) for advanced filtering of repository contents based on user prompts.
- **HTML Reports**: Generates user-friendly HTML reports summarizing repository statistics and digest contents.

---

## Installation

### Requirements

- Python 3.12 or above
- `git` installed and accessible in your system path

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/repo-digest-tool.git
   cd repo-digest-tool
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Optional: Install as a package for easier access:
   ```bash
   pip install -e .
   ```

---

## Usage

### CLI Commands

Here’s a quick overview of the commands:

#### Add a Repository

```bash
repo add <repo_url> [--branch <branch>] [--force]
```

- Adds a repository to local storage.
- Example:
  ```bash
  repo add https://github.com/honojs/hono
  repo add https://github.com/honojs/hono --branch develop --force
  ```

#### Remove a Repository

```bash
repo remove <repo_url>
```

- Removes a repository from local storage.
- Example:
  ```bash
  repo remove https://github.com/honojs/hono
  ```

#### List Repositories

```bash
repo list
```

- Lists all repositories stored locally.
- Example:
  ```bash
  repo list
  ```

#### Generate a Digest

```bash
repo digest <repo_url> [--branch <branch>] [--prompt <prompt>] [--force]
```

- Generates a digest for a repository. Optional: specify a branch or a custom LLM filtering prompt.
- Example:
  ```bash
  repo digest https://github.com/honojs/hono
  repo digest https://github.com/honojs/hono --prompt "Focus on APIs"
  ```

#### Clear Repositories

```bash
repo clear [--all | --author <author>]
```

- Clears repositories from local storage. Either all or selectively by author.
- Example:
  ```bash
  repo clear --all
  repo clear --author honojs
  ```

#### Update a Repository

```bash
repo update <repo_url>
```

- Updates a repository by pulling the latest changes.
- Example:
  ```bash
  repo update https://github.com/honojs/hono
  ```

---

## Development Roadmap

1. **Basic Functionality**:

   - Repository management (`add`, `remove`, `list`).
   - Digest generation.

2. **Digest Extensions**:

   - LLM filtering with custom prompts.
   - HTML report generation.

3. **Testing and Documentation**:

   - Unit tests for all commands.
   - Comprehensive documentation.

4. **Future Enhancements**:
   - Multi-language report support.
   - Integration with other platforms (e.g., GitLab).

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request.
