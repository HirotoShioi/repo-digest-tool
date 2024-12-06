import shutil
from typing import Optional
from repo_tool.core.filter import filter_files_in_repo
import concurrent.futures
from repo_tool.core.summary import generate_summary, store_result_to_file


def generate_digest(repo_id: str, prompt: Optional[str] = None) -> None:
    try:
        print("Processing repository...")
        file_list, repo_path = filter_files_in_repo(repo_id, prompt)
        if file_list:
            print("Generating summary and digest in parallel...")
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

        print("Cleaning up...")
        shutil.rmtree(f"tmp/{repo_id}")
    except Exception as e:
        print("Error:", e)
