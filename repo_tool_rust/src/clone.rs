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
pub async fn clone_repository(url: &str, repo_dir: PathBuf, force: bool) -> Result<()> {
    // Validate the URL
    let parsed_url =
        Url::parse(url).with_context(|| format!("Failed to parse repository URL: {}", url))?;

    // Extract author and repo name from URL path segments
    let path_segments: Vec<&str> = parsed_url
        .path_segments()
        .map(|segments| segments.collect())
        .unwrap_or_default();

    let (author, repo_name) = match (path_segments.get(0), path_segments.get(1)) {
        (Some(author), Some(repo_name)) => (author, repo_name),
        _ => return Err(anyhow::anyhow!("Invalid repository URL format")),
    };

    // Construct the full repository path
    let repo_dir = repo_dir.join(author).join(repo_name);

    // If repository already exists and force is false, return early with success
    if !force && repo_dir.exists() {
        println!("Repository already exists at {:?}", repo_dir);
        return Ok(());
    }

    // Handle force flag
    if force && repo_dir.exists() {
        std::fs::remove_dir_all(&repo_dir)?;
    }

    // Create the destination directory if it doesn't exist
    std::fs::create_dir_all(&repo_dir)
        .with_context(|| format!("Failed to create directory at {:?}", repo_dir))?;

    // Clone the repository
    let git_url = gix::url::parse(url.into())?;
    let mut prepare_clone = gix::prepare_clone(git_url, &repo_dir)?;
    let (mut prepare_checkout, _) = prepare_clone
        .fetch_then_checkout(gix::progress::Discard, &gix::interrupt::IS_INTERRUPTED)?;
    let (repo, _) =
        prepare_checkout.main_worktree(gix::progress::Discard, &gix::interrupt::IS_INTERRUPTED)?;

    println!(
        "Repository cloned successfully to {:?}",
        repo.work_dir().expect("should be there")
    );
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    #[tokio::test]
    async fn test_clone_repository() {
        let temp_dir = tempdir().unwrap();
        let repo_url = "https://github.com/HirotoShioi/repo-digest-tool";

        let result = clone_repository(repo_url, temp_dir.path().to_path_buf(), true).await;

        assert!(result.is_ok());
        let repo_dir = temp_dir.path().join("HirotoShioi").join("repo-digest-tool");
        println!("repo_dir: {:?}", repo_dir);
        assert!(repo_dir.exists());
        assert!(repo_dir.join(".git").exists());
    }

    #[tokio::test]
    async fn reclone_should_not_fail() {
        let temp_dir = tempdir().unwrap();
        let repo_url = "https://github.com/HirotoShioi/repo-digest-tool";

        let result = clone_repository(repo_url, temp_dir.path().to_path_buf(), false).await;
        let result2 = clone_repository(repo_url, temp_dir.path().to_path_buf(), false).await;

        assert!(result.is_ok());
        assert!(result2.is_ok());
    }

    #[tokio::test]
    async fn test_clone_invalid_url() {
        let temp_dir = tempdir().unwrap();
        let invalid_url = "not-a-url";

        let result = clone_repository(invalid_url, temp_dir.path().to_path_buf(), true).await;

        assert!(result.is_err());
    }
}
