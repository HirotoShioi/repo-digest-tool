from dotenv import load_dotenv

from repo_tool import GitHub, generate_digest

load_dotenv()


def main() -> None:
    repo_url = "https://github.com/HirotoShioi/repo-digest-tool"
    branch = None
    prompt = None
    github = GitHub()
    # prompt = "I'm interested in the code that is related to react. Please include examples as well as any documentation that is relevant to react."
    try:
        print("Cloning repository...")
        github.clone(repo_url, branch)

        print("Processing repository...")
        repo_path = GitHub.get_repo_path(repo_url)
        generate_digest(repo_path, prompt)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
