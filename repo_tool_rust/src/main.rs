use repo_tool_rust::clone::clone_repository;
use repo_tool_rust::filter::{filter_files_in_repo, get_filter_settings};
use std::path::PathBuf;

#[tokio::main]
async fn main() {
    let repo_url = "https://github.com/HirotoShioi/repo-digest-tool";
    match clone_repository(repo_url, PathBuf::from("./repositories/"), true).await {
        Ok(_) => println!("Clone successful!"),
        Err(err) => eprintln!("Error cloning repo: {:?}", err),
    }
    let repo_path = PathBuf::from("./repositories/HirotoShioi/repo-digest-tool");
    match filter_files_in_repo(&repo_path, None) {
        Ok(files) => println!("Filtered files: {:?}", files),
        Err(err) => eprintln!("Error filtering files: {:?}", err),
    }
}
