use repo_tool_rust::clone::clone_repository;
use repo_tool_rust::compress::compress_files;
use repo_tool_rust::filter::filter_files_in_repo;
use std::path::PathBuf;

#[tokio::main]
async fn main() {
    let repo_url = "https://github.com/TanStack/query";
    let repo_info = match clone_repository(repo_url, PathBuf::from("./repositories/"), false).await
    {
        Ok(repo_info) => repo_info,
        Err(err) => {
            eprintln!("Error cloning repo: {:?}", err);
            return;
        }
    };
    let files = match filter_files_in_repo(&repo_info.repo_path, None) {
        Ok(files) => files,
        Err(err) => {
            eprintln!("Error filtering files: {:?}", err);
            return;
        }
    };
    match compress_files(repo_info, files) {
        Ok(_) => println!("Compress successful!"),
        Err(err) => eprintln!("Error compressing files: {:?}", err),
    }
}
