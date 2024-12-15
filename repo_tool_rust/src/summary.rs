use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use tiktoken_rs::get_bpe_from_model;
use tiktoken_rs::CoreBPE;
use tokio::fs;

// Constants
const DATA_SIZE: usize = 20;
const PRECISION: usize = 2;
const BATCH_SIZE: usize = 100;
const MAX_FILE_SIZE: u64 = 5000; // KB

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileType {
    pub extension: String,
    pub count: usize,
    pub tokens: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileData {
    pub name: String,
    pub path: String,
    pub extension: String,
    pub tokens: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileStats {
    pub file_count: usize,
    pub total_size: f64,
    pub average_size: f64,
    pub max_size: f64,
    pub min_size: f64,
    pub context_length: usize,
    pub extension_tokens: Vec<FileType>,
    pub file_data: Vec<FileData>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Summary {
    pub repository: String,
    pub total_files: usize,
    pub total_size_kb: f64,
    pub average_file_size_kb: f64,
    pub max_file_size_kb: f64,
    pub min_file_size_kb: f64,
    pub file_types: Vec<FileType>,
    pub context_length: usize,
    pub file_data: Vec<FileData>,
}

pub struct FileInfo {
    file_path: PathBuf,
    repo_path: PathBuf,
}

pub async fn generate_summary(repo_path: &Path, file_list: &[PathBuf]) -> Result<Summary> {
    let file_infos: Vec<FileInfo> = file_list
        .iter()
        .map(|f| FileInfo {
            file_path: f.to_path_buf(),
            repo_path: repo_path.to_path_buf(),
        })
        .collect();

    let tokenizer = get_bpe_from_model("gpt-4o-2024-05-13")?;
    let file_stats = process_files(&file_infos, &tokenizer).await?;

    Ok(Summary {
        repository: repo_path
            .file_name()
            .unwrap_or_default()
            .to_string_lossy()
            .to_string(),
        total_files: file_stats.file_count,
        total_size_kb: (file_stats.total_size * 100.0).round() / 100.0,
        average_file_size_kb: (file_stats.average_size * 100.0).round() / 100.0,
        max_file_size_kb: (file_stats.max_size * 100.0).round() / 100.0,
        min_file_size_kb: (file_stats.min_size * 100.0).round() / 100.0,
        file_types: file_stats.extension_tokens,
        context_length: file_stats.context_length,
        file_data: file_stats.file_data,
    })
}

async fn process_files(file_infos: &[FileInfo], tokenizer: &CoreBPE) -> Result<FileStats> {
    let mut extension_data: HashMap<String, (usize, usize)> = HashMap::new(); // (count, tokens)
    let mut total_size = 0.0;
    let mut file_sizes = Vec::new();
    let mut context_length = 0;
    let mut file_data_list = Vec::new();

    for chunk in file_infos.chunks(BATCH_SIZE) {
        let mut futures = Vec::new();
        for file_info in chunk {
            futures.push(process_single_file(file_info, tokenizer));
        }

        let results = futures::future::join_all(futures).await;

        for result in results {
            if let Ok(Some(file_result)) = result {
                total_size += file_result.size;
                context_length += file_result.tokens;
                file_sizes.push(file_result.size);

                file_data_list.push(FileData {
                    name: Path::new(&file_result.path)
                        .file_name()
                        .unwrap_or_default()
                        .to_string_lossy()
                        .to_string(),
                    path: file_result.path,
                    extension: file_result.extension.clone(),
                    tokens: file_result.tokens,
                });
                let entry = extension_data
                    .entry(file_result.extension.clone())
                    .or_insert((0, 0));
                entry.0 += 1;
                entry.1 += file_result.tokens;
            }
        }
    }

    // Sort file_data_list by tokens
    file_data_list.sort_by(|a, b| b.tokens.cmp(&a.tokens));

    let extension_tokens: Vec<FileType> = extension_data
        .into_iter()
        .map(|(ext, (count, tokens))| FileType {
            extension: ext,
            count,
            tokens,
        })
        .collect();

    let file_count = file_data_list.len();
    let average_size = if file_count > 0 {
        total_size / file_count as f64
    } else {
        0.0
    };

    Ok(FileStats {
        file_count,
        total_size,
        average_size,
        max_size: file_sizes.iter().fold(0.0, |a, &b| a.max(b)),
        min_size: file_sizes.iter().fold(f64::INFINITY, |a, &b| a.min(b)),
        context_length,
        extension_tokens,
        file_data: file_data_list,
    })
}

#[derive(Debug, Clone)]
struct FileResult {
    path: String,
    size: f64,
    tokens: usize,
    extension: String,
}

async fn process_single_file(file_info: &FileInfo, bpe: &CoreBPE) -> Result<Option<FileResult>> {
    let relative_path = file_info
        .file_path
        .strip_prefix(&file_info.repo_path)?
        .to_string_lossy()
        .to_string();

    let metadata = fs::metadata(&file_info.file_path).await?;
    let file_size = metadata.len() as f64 / 1024.0; // Convert to KB

    if file_size > MAX_FILE_SIZE as f64 {
        return Ok(Some(FileResult {
            path: relative_path,
            size: file_size,
            tokens: 0,
            extension: file_info
                .file_path
                .extension()
                .and_then(|ext| ext.to_str())
                .unwrap_or("no_extension")
                .to_lowercase(),
        }));
    }

    let content = fs::read_to_string(&file_info.file_path).await?;
    let tokens = bpe.encode_with_special_tokens(&content).len();

    Ok(Some(FileResult {
        path: relative_path,
        size: file_size,
        tokens,
        extension: file_info
            .file_path
            .extension()
            .and_then(|ext| ext.to_str())
            .unwrap_or("no_extension")
            .to_lowercase(),
    }))
}
