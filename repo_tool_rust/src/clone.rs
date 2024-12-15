use anyhow::{Context, Result};
use std::path::PathBuf;
use url::Url;

/// Clones a git repository from the given URL to the specified destination path
///
/// # Arguments
/// * `url` - The URL of the git repository to clone
/// * `destination` - The path where the repository should be cloned to
///
/// # Returns
/// * `Result<()>` - Ok(()) if successful, Error if something went wrong
pub async fn clone_repository(url: &str, destination: PathBuf) -> Result<()> {
    // Validate the URL
    Url::parse(url).with_context(|| format!("Failed to parse repository URL: {}", url))?;

    // Create the destination directory if it doesn't exist
    std::fs::create_dir_all(&destination)
        .with_context(|| format!("Failed to create directory at {:?}", destination))?;
    // Parse the URL for git
    let git_url = gix::url::parse(url.into())?;
    let mut prepare_clone = gix::prepare_clone(git_url, &destination)?;
    let (mut prepare_checkout, _) = prepare_clone
        .fetch_then_checkout(gix::progress::Discard, &gix::interrupt::IS_INTERRUPTED)?;
    let (repo, _) =
        prepare_checkout.main_worktree(gix::progress::Discard, &gix::interrupt::IS_INTERRUPTED)?;

    println!(
        "Checking out into {:?} ...",
        repo.work_dir().expect("should be there")
    );
    Ok(())
}

// #[cfg(test)]
// mod tests {
//     use super::*;
//     use gix::tempfile::tempdir;
//     use std::fs;

//     #[tokio::test]
//     async fn test_clone_repository() {
//         let temp_dir = tempdir().unwrap();
//         let repo_url = "https://github.com/rust-lang/rust.git";

//         let result = clone_repository(repo_url, temp_dir.path().to_path_buf()).await;

//         assert!(result.is_ok());
//         assert!(temp_dir.path().join(".git").exists());
//     }

//     #[tokio::test]
//     async fn test_clone_invalid_url() {
//         let temp_dir = tempdir().unwrap();
//         let invalid_url = "not-a-url";

//         let result = clone_repository(invalid_url, temp_dir.path().to_path_buf()).await;

//         assert!(result.is_err());
//     }
// }
