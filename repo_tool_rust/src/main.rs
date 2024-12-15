use repo_tool_rust::clone::clone_repository;
use std::path::PathBuf;

#[tokio::main]
async fn main() {
    let repo_url = "https://github.com/HirotoShioi/repo-digest-tool";
    match clone_repository(repo_url, PathBuf::from("./repositories/"), true).await {
        Ok(_) => println!("Clone successful!"),
        Err(err) => eprintln!("Error cloning repo: {:?}", err),
    }
}
