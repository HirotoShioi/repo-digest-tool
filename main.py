import os
import shutil
from dotenv import load_dotenv
from lib import generate_summary
from lib.digest import process_repo
from lib.github import download_repo


load_dotenv()


def main():
    repo_url = "https://github.com/TanStack/query"
    branch = None
    repo_id = repo_url.split("/")[-1].replace(".git", "").replace("/", "_")
    prompt = None
    # prompt = "I'm interested in the code that is related to react. Please include examples as well as any documentation that is relevant to react."
    try:
        shutil.rmtree(f"tmp/", ignore_errors=True)
        print("Cloning repository...")
        download_repo(repo_url, repo_id, branch)

        print("Processing repository...")
        output_content, file_list, repo_path, file_info = process_repo(repo_id, prompt)
        if file_list:
            print("Generating summary...")
            generate_summary(file_list, repo_path, output_content, file_info)
        if output_content:
            print("Saving digest...")
            os.makedirs("digests", exist_ok=True)
            output_path = f"digests/{repo_path.name}.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_content)
        else:
            print("Failed to generate digest.")

        print("Cleaning up...")
        shutil.rmtree(f"tmp/{repo_id}")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
