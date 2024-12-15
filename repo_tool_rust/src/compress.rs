use crate::clone::RepoInfo;
use anyhow::{Context, Result};
use std::fs::{self, File};
use std::io::{BufRead, BufReader};
use std::path::{Path, PathBuf};

pub fn compress_files(repo_info: RepoInfo, files: Vec<PathBuf>) -> Result<()> {
    if files.is_empty() {
        return Ok(());
    }
    let content = generate_digest_content(&repo_info.repo_path, &files)?;

    // Create digests directory if it doesn't exist
    fs::create_dir_all("digests")?;

    // Write to output file
    let output_path = format!("digests/{}.txt", repo_info.repo_name);
    fs::write(&output_path, content)?;

    Ok(())
}

pub fn generate_digest_content(repo_path: &Path, files: &[PathBuf]) -> Result<String> {
    if files.is_empty() {
        return Ok("No matching files found.".to_string());
    }

    let mut output = String::new();

    // Add preamble
    output.push_str(
        "The following text represents the contents of the repository.\n\
        Each section begins with ----, followed by the file path and name.\n\
        A file list is provided at the beginning. End of repository content is marked by --END--.\n\n",
    );

    // Process only files (skip directories)
    let file_list: Vec<_> = files.iter().filter(|p| p.is_file()).collect();

    // Add file contents
    for file_path in file_list {
        let relative_path = file_path
            .strip_prefix(repo_path)
            .context("Failed to get relative path")?;

        output.push_str("----\n");
        output.push_str(&format!("{}\n", relative_path.display()));

        match read_file_contents(file_path) {
            Ok(contents) => {
                output.push_str(&contents);
                output.push('\n');
            }
            Err(e) => {
                output.push_str(&format!("Error reading file: {}\n\n", e));
            }
        }
    }

    output.push_str("--END--");
    Ok(output)
}

fn read_file_contents(path: &Path) -> Result<String> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut content = String::new();

    for line in reader.lines() {
        content.push_str(&line?);
        content.push('\n');
    }

    Ok(content)
}
