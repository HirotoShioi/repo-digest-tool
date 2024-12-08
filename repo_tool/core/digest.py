import concurrent.futures
from pathlib import Path
from typing import List, Optional

from repo_tool.core.contants import DIGEST_DIR
from repo_tool.core.filter import filter_files_in_repo
from repo_tool.core.summary import generate_summary


def generate_digest(repo_path: Path, prompt: Optional[str] = None) -> None:
    try:
        file_list = filter_files_in_repo(repo_path, prompt)
        if file_list:
            print("Generating summary and digest...")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # 両方のタスクを同時に実行
                futures = [
                    executor.submit(store_result_to_file, repo_path, file_list),
                    executor.submit(generate_summary, repo_path, file_list),
                ]
                # 全てのタスクが完了するまで待機
                concurrent.futures.wait(futures)
        else:
            print("Failed to generate digest.")
    except Exception as e:
        print("Error:", e)


def store_result_to_file(repo_path: Path, filtered_files: List[Path]) -> None:
    """
    Generates a digest from the filtered files in the repository.
    Includes a file list at the beginning of the output.
    """
    if not filtered_files:
        print("No matching files found.")
        return

    # 出力ディレクトリとファイルパスの設定
    output_dir = Path(DIGEST_DIR)
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{repo_path.name}.txt"

    with open(output_path, "w", encoding="utf-8") as output:
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

        output.write("--END--")  # End marker
