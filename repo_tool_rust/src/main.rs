use repo_tool_rust::clone::clone_repository;
use repo_tool_rust::compress::compress_files;
use repo_tool_rust::filter::filter_files_in_repo;
use std::path::PathBuf;

#[tokio::main]
async fn main() {
    let repo_url = "https://github.com/HirotoShioi/repo-digest-tool";
    match clone_repository(repo_url, PathBuf::from("./repositories/"), true).await {
        Ok(_) => println!("Clone successful!"),
        Err(err) => eprintln!("Error cloning repo: {:?}", err),
    }
    let repo_path = PathBuf::from("./repositories/HirotoShioi/repo-digest-tool");
    let files = match filter_files_in_repo(&repo_path, None) {
        Ok(files) => files,
        Err(err) => {
            eprintln!("Error filtering files: {:?}", err);
            return;
        }
    };
    match compress_files("repo-digest-tool".to_string(), files) {
        Ok(_) => println!("Compress successful!"),
        Err(err) => eprintln!("Error compressing files: {:?}", err),
    }
}
