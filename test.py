from dotenv import load_dotenv

from repo_tool import GitHub, generate_digest

load_dotenv(override=True)


def main() -> None:
    repo_url = "https://github.com/HirotoShioi/repo-digest-tool"
    branch = None
    prompt = None
    github = GitHub()
    prompt = "I want to know how to use the repository."
    try:
        print("Cloning repository...")
        github.clone(repo_url, branch)
        github.update(repo_url)

        print("Processing repository...")
        repo_path = github.get_repo_path(repo_url)
        generate_digest(repo_path, prompt)
        repos = github.list()
        print(repos)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
