import json
import os
import shutil
from typing import Optional, List
from pathlib import Path
import fnmatch
import subprocess
import logging
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import json

load_dotenv()

# Configure logging
logging.basicConfig(
    filename="repo_tool.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_error(e: Exception):
    logging.error(str(e))


def download_repo(
    repo_url: str,
    repo_id: str,
    github_token: Optional[str] = None,
    branch: Optional[str] = None,
):
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

    try:
        subprocess.run(cmd, check=True, text=True)
    except subprocess.CalledProcessError as e:
        log_error(e)
        raise RuntimeError(f"Error during repository cloning: {e}")


def is_ignored(
    file_path: Path, repo_path: Path, ignore_files: List[str], ignore_dirs: List[str]
) -> bool:
    relative_path = file_path.relative_to(repo_path).as_posix()

    for ignore_dir in ignore_dirs:
        if fnmatch.fnmatch(relative_path, ignore_dir) or fnmatch.fnmatch(
            str(file_path.parent), ignore_dir
        ):
            return True

    for ignore_file in ignore_files:
        if fnmatch.fnmatch(relative_path, ignore_file):
            return True

    return False


def get_all_files(repo_path: Path) -> List[Path]:
    try:
        all_files = list(repo_path.rglob("*"))
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


def read_file(file_path: Path) -> str:
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except UnicodeDecodeError:
        with file_path.open("r", encoding="shift_jis", errors="ignore") as f:
            return f.read()


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


def process_repo(repo_id: str):
    """
    Processes a repository using the .gptignore file to filter files.
    """
    repo_path = Path(f"tmp/{repo_id}")
    if not repo_path.exists():
        raise ValueError(f"Repository path '{repo_path}' does not exist.")

    try:
        # Determine .gptignore location
        ignore_file_path = repo_path / ".gptignore"
        if not ignore_file_path.exists():
            ignore_file_path = Path(".") / ".gptignore"
        include_file_path = repo_path / ".gptinclude"
        if not include_file_path.exists():
            include_file_path = Path(".") / ".gptinclude"

        ignore_list = read_pattern_file(ignore_file_path)
        include_list = read_pattern_file(include_file_path)

        # Get all files and filter based on extensions and .gptignore
        all_files = get_all_files(repo_path)
        filtered_files = filter_files(all_files, repo_path, ignore_list, include_list)

        return (
            generate_digest(repo_path, filtered_files),
            generate_file_list(repo_path, filtered_files),
            repo_path,
        )
    except Exception as e:
        log_error(e)
        raise RuntimeError(f"Error while processing repository '{repo_id}': {e}") from e


def generate_file_list(repo_path: Path, filtered_files: List[Path]) -> List[Path]:
    return [file_path for file_path in filtered_files if file_path.is_file()]


def generate_digest(repo_path: Path, filtered_files: List[Path]) -> List[str]:
    """
    Generates a digest from the filtered files in the repository.
    Includes a file list at the beginning of the output.
    """
    if not filtered_files:
        print("No matching files found.")
        return []

    output_content = []

    # Add preamble to explain the format
    preamble = (
        "The following text represents the contents of the repository.\n"
        "Each section begins with ----, followed by the file path and name.\n"
        "A file list is provided at the beginning. End of repository content is marked by --END--.\n"
    )
    output_content.append(preamble)

    # Add file contents
    for file_path in filtered_files:
        # Skip directories
        if file_path.is_dir():
            continue

    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            relative_path = file_path.relative_to(repo_path)
            output_content.append("----")  # Section divider
            output_content.append(str(relative_path))  # File path
            output_content.append(f.read())  # File content
    except Exception as e:
        # Log the error and continue
        relative_path = file_path.relative_to(repo_path)
        output_content.append("----")
        output_content.append(str(relative_path))
        output_content.append(f"Error reading file: {e}")

    output_content.append("--END--")  # End marker
    return output_content


def save_digest(output_content: List[str], repo_path: Path):
    os.makedirs("digests", exist_ok=True)
    output_path = f"digests/{repo_path.name}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(output_content))


from jinja2 import Environment, FileSystemLoader


# カスタムフィルターを定義
def format_number(value):
    """数値をカンマ区切りにフォーマット"""
    if isinstance(value, (int, float)):
        return f"{value:,}"  # カンマ区切り
    return value


def create_visualization(summary: dict, repo_path: Path):
    """
    Create HTML report with Chart.js visualizations using Jinja2
    """
    # ファイルサイズデータの取得
    file_list_path = f"digests/{repo_path.name}_file_list.txt"
    with open(file_list_path, "r", encoding="utf-8") as f:
        files = f.read().splitlines()

    file_size_data = []
    repo_dir = Path(f"tmp/{repo_path.name}")

    for file_path in files:
        full_path = repo_dir / file_path
        if full_path.is_file():
            size_kb = round(full_path.stat().st_size / 1024, 2)  # Convert to KB
            file_size_data.append(
                {
                    "name": str(Path(file_path).name),
                    "path": str(file_path),
                    "size": size_kb,
                }
            )

    # サイズでソート
    file_size_data.sort(key=lambda x: x["size"], reverse=True)

    # Jinja2環境の設定
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["format_number"] = format_number
    template = env.get_template("report.html")

    # テンプレートにデータを渡してレンダリング
    html_content = template.render(
        repo_name=repo_path.name,
        summary=summary,
        file_types_labels=[
            ext
            for ext, _ in sorted(
                summary["file_types"].items(), key=lambda x: x[1], reverse=True
            )[:20]
        ],
        file_types_data=[
            count
            for _, count in sorted(
                summary["file_types"].items(), key=lambda x: x[1], reverse=True
            )[:20]
        ],
        file_sizes_labels=[item["name"] for item in file_size_data[:20]],
        file_sizes_data=[item["size"] for item in file_size_data[:20]],
        file_sizes_paths=[item["path"] for item in file_size_data[:20]],
    )

    # Save HTML report
    report_path = f"digests/{repo_path.name}_report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Report saved to {report_path}")


def save_file_list(file_list: List[Path], repo_path: Path):
    """
    Save the file list and generate a summary report with file statistics.
    File sizes are stored in kilobytes.
    """
    os.makedirs("digests", exist_ok=True)
    file_list_path = f"digests/{repo_path.name}_file_list.txt"
    summary_path = f"digests/{repo_path.name}_summary.json"

    # Initialize counters and stats
    extension_counts = {}
    total_size = 0  # in KB
    file_sizes = []  # in KB

    # Process files for detailed stats
    processed_files = []
    for file_path in file_list:
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if not file_path.is_file():
            continue

        try:
            relative_path = file_path.relative_to(repo_path)
            processed_files.append(str(relative_path))

            # Convert bytes to KB
            file_size = file_path.stat().st_size / 1024  # bytes to KB
            total_size += file_size
            file_sizes.append(file_size)

            # Count file extensions
            ext = file_path.suffix.lower() or "no_extension"
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

    # Calculate stats (all in KB)
    file_count = len(processed_files)
    average_size = round(total_size / file_count, 2) if file_count > 0 else 0
    max_size = round(max(file_sizes, default=0), 2)
    min_size = round(min(file_sizes, default=0), 2)
    total_size = round(total_size, 2)

    # Save file list
    with open(file_list_path, "w", encoding="utf-8") as f:
        f.write("\n".join(processed_files))
    print(f"File list saved to {file_list_path}")

    # Generate summary
    summary = {
        "repository": repo_path.name,
        "total_files": file_count,
        "total_size_kb": total_size,
        "average_file_size_kb": average_size,
        "max_file_size_kb": max_size,
        "min_file_size_kb": min_size,
        "file_types": extension_counts,
    }

    # Save summary as JSON
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    print(f"Summary saved to {summary_path}")

    # Generate visualization report
    create_visualization(summary, repo_path)


def main(
    repo_url: str,
    github_token: Optional[str],
    branch: Optional[str] = None,
):
    repo_id = repo_url.split("/")[-1].replace(".git", "").replace("/", "_")

    try:
        shutil.rmtree(f"tmp/", ignore_errors=True)
        print("Cloning repository...")
        download_repo(repo_url, repo_id, github_token, branch)

        print("Processing repository...")
        output_content, file_list, repo_path = process_repo(repo_id)
        if file_list:
            print("Saving file list...")
            save_file_list(file_list, repo_path)
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
        github_token=os.getenv("GITHUB_TOKEN"),
        branch=None,
    )
