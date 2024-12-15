use anyhow::{Context, Result};
use globset::{Glob, GlobSet, GlobSetBuilder};
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use walkdir::WalkDir;

#[derive(Debug, Serialize, Deserialize)]
pub struct FilterSettings {
    ignore_list: Vec<String>,
    include_list: Vec<String>,
}

fn build_glob_set(patterns: &[String]) -> Result<GlobSet> {
    let mut builder = GlobSetBuilder::new();
    for pattern in patterns {
        let glob = Glob::new(pattern)
            .with_context(|| format!("Failed to create glob pattern from: {}", pattern))?;
        builder.add(glob);
    }
    builder.build().context("Failed to build glob set")
}

pub fn get_all_files(repo_path: &Path, ignore_patterns: &[String]) -> Result<Vec<PathBuf>> {
    let mut all_files = Vec::new();
    let ignore_set = build_glob_set(ignore_patterns)?;

    for entry in WalkDir::new(repo_path) {
        let entry = entry.context("Failed to read directory entry")?;
        let path = entry.path().to_path_buf();

        if !should_ignore(&path, repo_path, &ignore_set) {
            all_files.push(path);
        }
    }

    Ok(all_files)
}

fn should_ignore(file_path: &Path, repo_path: &Path, ignore_set: &GlobSet) -> bool {
    if let Ok(relative_path) = file_path.strip_prefix(repo_path) {
        let path_str = relative_path.to_string_lossy();

        // ディレクトリの場合は末尾にスラッシュを追加
        if file_path.is_dir() {
            return ignore_set.is_match(format!("{}/", path_str));
        }

        ignore_set.is_match(path_str.as_ref())
    } else {
        false
    }
}

pub fn filter_files(
    all_files: &[PathBuf],
    repo_path: &Path,
    ignore_patterns: &[String],
    include_patterns: &[String],
) -> Result<Vec<PathBuf>> {
    let ignore_set = build_glob_set(ignore_patterns)?;
    let include_set = build_glob_set(include_patterns)?;
    let mut filtered_files = Vec::new();

    for file_path in all_files {
        if should_ignore(file_path, repo_path, &ignore_set) {
            continue;
        }

        if let Ok(relative_path) = file_path.strip_prefix(repo_path) {
            let path_str = relative_path.to_string_lossy();
            // Check if the file matches any include pattern
            let include_match =
                include_patterns.is_empty() || include_set.is_match(path_str.as_ref());

            if include_match {
                filtered_files.push(file_path.to_path_buf());
            }
        }
    }

    Ok(filtered_files)
}

fn read_pattern_file(file_path: &Path) -> Result<Vec<String>> {
    if !file_path.exists() {
        return Ok(Vec::new());
    }

    let content = std::fs::read_to_string(file_path)
        .with_context(|| format!("Failed to read pattern file: {}", file_path.display()))?;

    Ok(content
        .lines()
        .filter(|line| !line.trim().is_empty() && !line.starts_with('#'))
        .map(String::from)
        .collect())
}

pub fn filter_files_in_repo(repo_path: &Path, prompt: Option<String>) -> Result<Vec<PathBuf>> {
    if !repo_path.exists() {
        anyhow::bail!("Repository path '{}' does not exist", repo_path.display());
    }

    let filter_settings = get_filter_settings()?;

    let all_files = get_all_files(repo_path, &filter_settings.ignore_list)?;
    let filtered_files = filter_files(
        &all_files,
        repo_path,
        &filter_settings.ignore_list,
        &filter_settings.include_list,
    )?;

    if let Some(_prompt) = prompt {
        // Note: LLM filtering would need to be implemented separately
        // filtered_files = filter_files_with_llm(&filtered_files, &prompt)?;
    }

    Ok(filtered_files
        .into_iter()
        .filter(|path| path.is_file())
        .collect())
}

pub fn get_filter_settings() -> Result<FilterSettings> {
    let ignore_list = read_pattern_file(&Path::new("../.gptignore"))?;
    let include_list = read_pattern_file(&Path::new("../.gptinclude"))?;

    Ok(FilterSettings {
        ignore_list,
        include_list,
    })
}
