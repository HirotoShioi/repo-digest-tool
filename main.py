import os
import shutil
from datetime import datetime
from typing import Optional, List, Tuple, Union
from pathlib import Path
import fnmatch

def download_repo(repo_url: str, repo_id: str, github_token: Optional[str] = None, branch: Optional[str] = None):
    if not repo_url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub repository URL.")
    if github_token:
        repo_url = repo_url.replace(
            "https://github.com/", f"https://{github_token}@github.com/"
        )
    cmd = ["git", "clone", "--depth=1"]
    if branch:
        cmd.extend(["--branch", branch])
    cmd.extend([repo_url, f"tmp/{repo_id}"])
    result = os.system(" ".join(cmd))
    if result != 0:
        raise RuntimeError("Failed to clone the repository. Check the URL, branch name, or token.")


def is_ignored(file_path: Path, repo_path: Path, ignore_files: List[str], ignore_dirs: List[str]) -> bool:
    relative_path = file_path.relative_to(repo_path)
    relative_path_str = str(relative_path).replace(os.sep, '/')

    for ignore_dir in ignore_dirs:
        ignore_dir = ignore_dir.replace(os.sep, '/')
        if fnmatch.fnmatch(relative_path_str, ignore_dir) or fnmatch.fnmatch(os.path.dirname(relative_path_str), ignore_dir):
            return True

    for ignore_file in ignore_files:
        ignore_file = ignore_file.replace(os.sep, '/')
        if fnmatch.fnmatch(relative_path_str, ignore_file):
            return True

    return False


def get_all_files(repo_path: Path, target_dir: Optional[Union[str, List[str]]]) -> List[Path]:
    all_files = []
    if not target_dir:
        all_files = list(repo_path.rglob("*"))
    else:
        if isinstance(target_dir, str):
            target_dir = [target_dir]
        for pattern in target_dir:
            matching_paths = repo_path.glob(pattern)
            matching_files = [p for p in matching_paths if p.is_file()]
            if matching_files:
                all_files.extend(matching_files)
            elif any(p.is_dir() for p in matching_paths):
                print(f"No files found in '{pattern}', but the directory exists.")
            else:
                print(f"No files matching pattern '{pattern}' in '{repo_path}'.")
    return all_files


def should_ignore(file_path: Path, repo_path: Path, ignore_list: List[str]) -> bool:
    """Check if the file should be ignored based on the ignore list."""
    relative_path = file_path.relative_to(repo_path)
    relative_path_str = str(relative_path).replace(os.sep, '/')
    for pattern in ignore_list:
        if fnmatch.fnmatch(relative_path_str, pattern):
            return True
    return False

def filter_files(
    all_files: List[Path], 
    repo_path: Path, 
    extensions_list: Optional[List[str]], 
    ignore_list: List[str]
) -> List[Path]:
    """Filter files based on extensions and ignore list."""
    filtered_files = []
    for file_path in all_files:
        if should_ignore(file_path, repo_path, ignore_list):
            continue
        if extensions_list:
            if file_path.suffix in extensions_list:
                filtered_files.append(file_path)
        else:
            filtered_files.append(file_path)
    return filtered_files

def get_ignore_list(ignore_file_path: Path) -> List[str]:
    """
    Reads the .gptignore file and returns a list of patterns.
    """
    ignore_list = []
    if ignore_file_path.exists():
        with ignore_file_path.open("r", encoding="utf-8") as ignore_file:
            for line in ignore_file:
                line = line.strip()
                if line and not line.startswith("#"):  # Skip comments and empty lines
                    ignore_list.append(line)
    return ignore_list

def process_repo(repo_id: str, target_dir: Optional[Union[str, List[str]]] = None, extensions_list: Optional[List[str]] = None):
    """
    Processes a repository using the .gptignore file to filter files.
    """
    repo_path = Path(f"tmp/{repo_id}")
    if not repo_path.exists():
        raise ValueError(f"Repository path '{repo_path}' does not exist.")

    # Determine .gptignore location
    ignore_file_path = repo_path / ".gptignore"
    if not ignore_file_path.exists():
        ignore_file_path = Path(".") / ".gptignore"

    ignore_list = get_ignore_list(ignore_file_path)

    # Get all files and filter based on extensions and .gptignore
    all_files = get_all_files(repo_path, target_dir)
    filtered_files = filter_files(all_files, repo_path, extensions_list, ignore_list)

    return generate_digest(repo_path, filtered_files)

def generate_digest(repo_path: Path, filtered_files: List[Path]) -> Tuple[List[str], Path]:
    if not filtered_files:
        print("No matching files found.")
        return [], repo_path

    file_list = [
        str(file_path.relative_to(repo_path)).replace(os.sep, '/') for file_path in filtered_files
    ]

    output_content = []
    output_content.append("\n".join(file_list))
    for file_path in filtered_files:
        try:
            with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                relative_path = file_path.relative_to(repo_path)
                output_content.append(f"# {relative_path}\n{f.read()}\n")
        except Exception as e:
            output_content.append(f"# Error reading file {relative_path}: {e}\n")

    return output_content, repo_path

def save_digest(output_content: List[str], repo_path: Path):
    os.makedirs("digests", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"digests/{repo_path.name}_digest_{timestamp}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(output_content))


def main(
    repo_url: str,
    github_token: Optional[str],
    branch: Optional[str] = None,
    target_dir: Optional[Union[str, List[str]]] = None,
    extensions: Optional[List[str]] = None,
):
    repo_id = repo_url.split("/")[-1].replace(".git", "").replace("/", "_")

    try:
        shutil.rmtree(f"tmp/", ignore_errors=True)
        print("Cloning repository...")
        download_repo(repo_url, repo_id, github_token, branch)

        print("Processing repository...")
        output_content, repo_path = process_repo(repo_id, target_dir, extensions)
        if output_content:
            print("Saving digest...")
            save_digest(output_content, repo_path)
        else:
            print("Failed to generate digest.")

        print("Cleaning up...")
        shutil.rmtree(f"tmp/{repo_id}")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main(
        repo_url="https://github.com/TanStack/query",
        github_token=None,
        branch=None,
        target_dir=None,
        extensions=None,
    )
