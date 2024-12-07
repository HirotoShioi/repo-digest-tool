from dotenv import load_dotenv

from repo_tool import GitHub, generate_digest

load_dotenv()


def main() -> None:
    repo_url = "https://github.com/HirotoShioi/repo-digest-tool"
    branch = None
    repo_id = GitHub.calculate_repo_id(repo_url)
    prompt = None
    github = GitHub()
    # prompt = "I'm interested in the code that is related to react. Please include examples as well as any documentation that is relevant to react."
    try:
        # shutil.rmtree(REPO_DIR, ignore_errors=True)
        print("Cloning repository...")
        github.clone(repo_url, branch, force=True)

        print("Processing repository...")
        generate_digest(repo_id, prompt)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
