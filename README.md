# Repo Digest Tool

Extract and summarize contents from GitHub repositories with advanced filtering options, tailored for LLM data preparation—all within Google Colab.

## Description

This tool allows you to clone a GitHub repository, filter its files based on specified criteria, aggregate their contents, and download the combined result—all from within a Google Colab environment. It's particularly useful for preparing data for Large Language Models (LLMs) by extracting relevant code and documentation from repositories.

## Features

- **Clone Repositories**: Clone public or private GitHub repositories directly in Colab.
- **Advanced Filtering**:
  - Filter files by target directories and file extensions.
  - Ignore specific files and directories based on patterns.
- **Content Aggregation**: Combine the contents of filtered files into a single text file.
- **Easy Download**: Automatically download the aggregated file within the Colab interface.
- **Customizable**: Adjust parameters to suit different repositories and requirements.

## Usage in Google Colab

### 1. Copy the Script into a Colab Notebook

- Open a new Google Colab notebook.
- Copy the entire script provided into a code cell.

### 2. Set Parameters and Run

Below is an example of how to use the tool within the Colab notebook:

```python
if __name__ == "__main__":
    # GitHub personal access token (required for private repositories)
    github_token = None  # Replace with your token if needed

    parameters = {
        "repo_url": "https://github.com/your-username/your-repo",  # GitHub repository URL
        "github_token": github_token,
        "branch": None,  # Specify branch if needed
        "target_dir": ["src/**"],  # Directories to include (supports glob patterns)
        "extensions": ["*.py"],  # File extensions to include
        "ignore_files": ["test_*.py", "*.md"],  # File patterns to ignore
        "ignore_dirs": ["docs/", "tests/"],  # Directories to ignore
    }

    main(**parameters)
```

### Parameters Explained

- **`repo_url`**: URL of the GitHub repository to clone.
- **`github_token`**: Personal access token for GitHub (optional, but required for private repos).
- **`branch`**: Specific branch to clone (default is the default branch).
- **`target_dir`**: List of directories or patterns to include. Uses glob patterns.
- **`extensions`**: List of file extensions or patterns to include.
- **`ignore_files`**: List of file patterns to exclude.
- **`ignore_dirs`**: List of directories or patterns to exclude.

### 3. Run the Notebook

- Execute all cells in the notebook.
- The script will:
  - Clone the specified repository into the Colab environment.
  - Process the repository based on your parameters.
  - Generate an aggregated text file.
  - Automatically download the aggregated file to your local machine.

## Examples

### Example 1: Process a Public Repository

```python
parameters = {
    "repo_url": "https://github.com/psf/requests",
    "github_token": None,
    "target_dir": ["requests/**"],
    "extensions": ["*.py"],
    "ignore_files": ["test_*.py"],
    "ignore_dirs": ["tests/"],
}

main(**parameters)
```

### Example 2: Process a Private Repository

```python
parameters = {
    "repo_url": "https://github.com/your-username/private-repo",
    "github_token": "your_personal_access_token",
    "branch": "develop",
    "target_dir": ["app/**", "lib/**"],
    "extensions": ["*.py", "*.txt"],
    "ignore_files": ["config.py"],
    "ignore_dirs": ["app/logs/", "lib/temp/"],
}

main(**parameters)
```

## Notes

- **GitHub Personal Access Token**: Required for accessing private repositories. Generate one from your GitHub account settings with appropriate scopes.
- **File Patterns**: The script uses `glob` and `fnmatch` for pattern matching. Ensure your patterns are correctly specified.
- **Google Colab Specifics**: The `download_digest()` function uses `google.colab`'s `files.download()` method to download files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an issue or contact the repository owner.
