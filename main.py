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


def filter_files(all_files: List[Path], repo_path: Path, extensions_list: List[str], ignore_files: List[str], ignore_dirs: List[str]) -> List[Path]:
    filtered_files = []
    for file_path in all_files:
        if is_ignored(file_path, repo_path, ignore_files, ignore_dirs):
            continue
        if extensions_list:
            if any(file_path.suffix == ext for ext in extensions_list):
                filtered_files.append(file_path)
        else:
            filtered_files.append(file_path)
    return filtered_files


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

def process_repo(
    repo_id: str,
    target_dir: Optional[Union[str, List[str]]] = None,
    extensions_list: Optional[List[str]] = None,
    ignore_files: Optional[List[str]] = None,
    ignore_dirs: Optional[List[str]] = None,
):
    repo_path = Path(f"tmp/{repo_id}")
    if not repo_path.exists():
        raise ValueError(f"Repository path '{repo_path}' does not exist.")

    extensions_list = extensions_list or []
    ignore_files = ignore_files or []
    ignore_dirs = ignore_dirs or []

    all_files = get_all_files(repo_path, target_dir)
    filtered_files = filter_files(all_files, repo_path, extensions_list, ignore_files, ignore_dirs)
    return generate_digest(repo_path, filtered_files)


def main(
    repo_url: str,
    github_token: Optional[str],
    branch: Optional[str] = None,
    target_dir: Optional[Union[str, List[str]]] = None,
    extensions: Optional[List[str]] = None,
    ignore_files: Optional[List[str]] = None,
    ignore_dirs: Optional[List[str]] = None,
):
    repo_id = repo_url.split("/")[-1].replace(".git", "").replace("/", "_")

    try:
        shutil.rmtree(f"tmp/", ignore_errors=True)
        print("Cloning repository...")
        download_repo(repo_url, repo_id, github_token, branch)

        print("Processing repository...")
        output_content, repo_path = process_repo(repo_id, target_dir, extensions, ignore_files, ignore_dirs)
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
        ignore_files=["pnpm-lock.yaml", "*.png", "*.svg", "*.sketch"],
        ignore_dirs=[".git/**"],
    )