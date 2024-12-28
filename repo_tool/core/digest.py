import concurrent.futures
import os
from concurrent.futures import Future
from io import StringIO
from pathlib import Path
from typing import List, Optional, TypeVar

from pydantic import BaseModel, Field

from repo_tool.core.contants import DIGEST_DIR
from repo_tool.core.filter import filter_files_in_repo
from repo_tool.core.github import Repository
from repo_tool.core.summary import generate_summary

T = TypeVar("T")  # Define a type variable for the Future's return type


def generateSummaryAndReport(repo_info: Repository, file_list: List[Path]) -> None:
    summary = generate_summary(repo_info, file_list)
    summary.generate_report()


def generate_digest(repo_info: Repository, prompt: Optional[str] = None) -> None:
    try:
        file_list = filter_files_in_repo(repo_info.path, prompt)
        if file_list:
            print("Generating summary and digest...")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Create properly typed futures list
                futures: List[Future[None]] = [
                    executor.submit(store_result_to_file, repo_info.path, file_list),
                    executor.submit(generateSummaryAndReport, repo_info, file_list),
                ]
                # Wait for all tasks to complete
                concurrent.futures.wait(futures)
        else:
            print("Failed to generate digest.")
    except Exception as e:
        print("Error:", e)


def generate_digest_content(repo_path: Path, filtered_files: List[Path]) -> str:
    """
    Generates digest content as a string from the filtered files in the repository.
    """
    if not filtered_files:
        return "No matching files found."

    output = StringIO()

    # Add preamble
    output.write(
        "The following text represents the contents of the repository.\n"
        "Each section begins with ----, followed by the file path and name.\n"
        "A file list is provided at the beginning. End of repository content is marked by --END--.\n\n"
    )

    # ファイルのみを処理
    file_list = [f for f in filtered_files if f.is_file()]

    # Add file contents
    for file_path in file_list:
        try:
            relative_path = file_path.relative_to(repo_path)
            output.write("----\n")  # Section divider
            output.write(f"{relative_path}\n")  # File path

            # ファイルを1行ずつ読み込んで処理
            with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    output.write(line)
            output.write("\n")

        except Exception as e:
            # Log the error and continue
            relative_path = file_path.relative_to(repo_path)
            output.write("----\n")
            output.write(f"{relative_path}\n")
            output.write(f"Error reading file: {e}\n\n")

    output.write("--END--")
    return output.getvalue()


def store_result_to_file(repo_path: Path, filtered_files: List[Path]) -> None:
    """
    Generates a digest from the filtered files and stores it in a file.
    """
    if not filtered_files:
        print("No matching files found.")
        return

    # 出力ディレクトリとファイルパスの設定
    output_dir = Path(DIGEST_DIR)
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{repo_path.name}.txt"

    digest_content = generate_digest_content(repo_path, filtered_files)

    with open(output_path, "w", encoding="utf-8") as output:
        output.write(digest_content)


class File(BaseModel):
    path: str = Field(..., description="The path of the file")
    content: str = Field(..., description="The content of the file")
    url: str = Field(..., description="The URL of the file")


class RespositoryContent(BaseModel):
    id: str = Field(..., description="The id of the repository")
    name: str = Field(..., description="The name of the repository")
    author: str = Field(..., description="The author of the repository")
    files: List[File]


def read_file_content(file_path: Path, repository: Repository) -> Optional[File]:
    """
    Read a single file's content with proper error handling.

    Args:
        file_path: Path to the file to read
        repo_path: Base repository path for calculating relative path

    Returns:
        File object if successful, None if failed
    """
    try:
        if not file_path.is_file():
            return None

        relative_path = str(file_path.relative_to(repository.path))
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return File(
            path=relative_path,
            content=content,
            url=f"{repository.url}/blob/{repository.branch}/{relative_path}",
        )

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None


def generate_repository_content(
    repository: Repository, filtered_files: List[Path]
) -> RespositoryContent:
    """
    Generate repository content from filtered files with concurrent file reading.

    Args:
        repo_path: Base repository path
        filtered_files: List of filtered file paths to process

    Returns:
        RespositoryContent containing list of files with their paths and contents
    """
    # Calculate optimal number of threads based on CPU count and list size
    max_workers = min(32, len(filtered_files), (os.cpu_count() or 1) * 4)

    files = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all file reading tasks
        future_to_file = {
            executor.submit(read_file_content, file_path, repository): file_path
            for file_path in filtered_files
        }

        # Collect results as they complete
        for future in concurrent.futures.as_completed(future_to_file):
            file_result = future.result()
            if file_result:
                files.append(file_result)

    return RespositoryContent(
        id=repository.id,
        name=repository.name,
        author=repository.author,
        files=files,
    )
