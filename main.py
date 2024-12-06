import shutil
from dotenv import load_dotenv
from lib import generate_summary, generate_digest, filter_files_in_repo
from lib.github import download_repo
import concurrent.futures

load_dotenv()


def main():
    repo_url = "https://github.com/HirotoShioi/repo-digest-tool"
    branch = None
    repo_id = repo_url.split("/")[-1].replace(".git", "").replace("/", "_")
    prompt = None
    # prompt = "I'm interested in the code that is related to react. Please include examples as well as any documentation that is relevant to react."
    try:
        shutil.rmtree(f"tmp/", ignore_errors=True)
        print("Cloning repository...")
        download_repo(repo_url, repo_id, branch)

        print("Processing repository...")
        file_list, repo_path = filter_files_in_repo(repo_id, prompt)
        if file_list:
            print("Generating summary and digest in parallel...")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # 両方のタスクを同時に実行
                futures = [
                    executor.submit(generate_digest, repo_path, file_list),
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


if __name__ == "__main__":
    main()
