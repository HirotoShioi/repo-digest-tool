import fnmatch
from pathlib import Path
from typing import List, Optional, Tuple
from lib.file_filtering_chain import filter_files_with_llm
from lib.logger import log_error


def get_all_files(repo_path: Path, ignore_patterns: List[str]) -> List[Path]:
    try:
        all_files = []
        for path in repo_path.rglob("*"):
            if not should_ignore(path, repo_path, ignore_patterns):
                all_files.append(path)
        return all_files
    except Exception as e:
        log_error(e)
        raise RuntimeError(f"Error while retrieving files from {repo_path}: {e}") from e


def should_ignore(file_path: Path, repo_path: Path, ignore_patterns: List[str]) -> bool:
    """
    Checks if a file or directory matches any of the ignore patterns.
    """
    relative_path = str(file_path.relative_to(repo_path))
    for pattern in ignore_patterns:
        # Match directories and files explicitly
        if pattern.endswith("/") and file_path.is_dir():
            if fnmatch.fnmatch(relative_path + "/", pattern):
                return True
        elif fnmatch.fnmatch(relative_path, pattern):
            return True
    return False


def filter_files(
    all_files: List[Path],
    repo_path: Path,
    ignore_patterns: List[str],
    include_patterns: List[str],
) -> List[Path]:
    """
    Filters the files based on .gptignore and .gptinclude patterns.
    """
    filtered_files = []
    for file_path in all_files:
        if should_ignore(file_path, repo_path, ignore_patterns):
            continue

        relative_path = str(file_path.relative_to(repo_path))

        # Check if the file matches any include pattern
        include_match = any(
            fnmatch.fnmatch(relative_path, pattern) for pattern in include_patterns
        )

        # If include patterns are provided, skip files that do not match
        if include_patterns and not include_match:
            continue

        filtered_files.append(file_path)
    return filtered_files


def read_pattern_file(file_path: Path) -> List[str]:
    """
    Reads a pattern file and returns a list of patterns.
    Skips comments and empty lines.
    """
    pattern_list = []
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as pattern_file:
            for line in pattern_file:
                line = line.strip()
                if line and not line.startswith("#"):  # Skip comments and empty lines
                    pattern_list.append(line)
    return pattern_list


def process_repo(repo_id: str, prompt: Optional[str] = None) -> Tuple[List[Path], Path]:
    """
    Processes a repository using the .gptignore file to filter files.
    """
    repo_path = Path(f"tmp/{repo_id}")
    if not repo_path.exists():
        raise ValueError(f"Repository path '{repo_path}' does not exist.")

    try:
        ignore_list = read_pattern_file(Path(".") / ".gptignore")
        include_list = read_pattern_file(Path(".") / ".gptinclude")
        # Get all files and filter based on extensions and .gptignore
        all_files = get_all_files(repo_path, ignore_list)
        filtered_files = filter_files(all_files, repo_path, ignore_list, include_list)
        if prompt:
            filtered_files = filter_files_with_llm(filtered_files, prompt)
        file_list = [file_path for file_path in filtered_files if file_path.is_file()]
        return (
            file_list,
            repo_path,
        )
    except Exception as e:
        log_error(e)
        raise RuntimeError(f"Error while processing repository '{repo_id}': {e}") from e
