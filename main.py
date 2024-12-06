from dotenv import load_dotenv
from repo_tool import generate_digest, download_repo
from repo_tool.core.repository import calculate_repo_id

load_dotenv()


def main():
    repo_url = "https://github.com/HirotoShioi/repo-digest-tool"
    branch = None
    repo_id = calculate_repo_id(repo_url)
    prompt = None
    # prompt = "I'm interested in the code that is related to react. Please include examples as well as any documentation that is relevant to react."
    try:
        # shutil.rmtree(REPO_DIR, ignore_errors=True)
        print("Cloning repository...")
        download_repo(repo_url, repo_id, branch)

        print("Processing repository...")
        generate_digest(repo_id, prompt)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
