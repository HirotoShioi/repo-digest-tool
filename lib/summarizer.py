import json
import os
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader
import tiktoken


# カスタムフィルターを定義
def format_number(value):
    """数値をカンマ区切りにフォーマット"""
    if isinstance(value, (int, float)):
        return f"{value:,}"  # カンマ区切り
    return value


def create_visualization(summary: dict, repo_path: Path):
    """
    Create HTML report with Chart.js visualizations using Jinja2
    """
    # ファイルサイズデータの取得
    file_list_path = f"digests/{repo_path.name}_file_list.txt"
    with open(file_list_path, "r", encoding="utf-8") as f:
        files = f.read().splitlines()

    file_size_data = []
    repo_dir = Path(f"tmp/{repo_path.name}")

    for file_path in files:
        full_path = repo_dir / file_path
        if full_path.is_file():
            size_kb = round(full_path.stat().st_size / 1024, 2)  # Convert to KB
            file_size_data.append(
                {
                    "name": str(Path(file_path).name),
                    "path": str(file_path),
                    "size": size_kb,
                }
            )

    # サイズでソート
    file_size_data.sort(key=lambda x: x["size"], reverse=True)

    # Jinja2環境の設定
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["format_number"] = format_number
    template = env.get_template("report.html")

    # テンプレートにデータを渡してレンダリング
    html_content = template.render(
        repo_name=repo_path.name,
        summary=summary,
        file_types_labels=[
            ext
            for ext, _ in sorted(
                summary["file_types"].items(), key=lambda x: x[1], reverse=True
            )[:20]
        ],
        file_types_data=[
            count
            for _, count in sorted(
                summary["file_types"].items(), key=lambda x: x[1], reverse=True
            )[:20]
        ],
        file_sizes_labels=[item["name"] for item in file_size_data[:20]],
        file_sizes_data=[item["size"] for item in file_size_data[:20]],
        file_sizes_paths=[item["path"] for item in file_size_data[:20]],
    )

    # Save HTML report
    report_path = f"digests/{repo_path.name}_report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Report saved to {report_path}")


encoding = tiktoken.get_encoding("o200k_base")


def generate_summary(file_list: List[Path], repo_path: Path, output_content: str):
    """
    Save the file list and generate a summary report with file statistics.
    File sizes are stored in kilobytes.
    """
    os.makedirs("digests", exist_ok=True)
    file_list_path = f"digests/{repo_path.name}_file_list.txt"
    summary_path = f"digests/{repo_path.name}_summary.json"

    # Initialize counters and stats
    extension_counts = {}
    total_size = 0  # in KB
    file_sizes = []  # in KB
    total_tokens = len(encoding.encode(output_content))

    # Process files for detailed stats
    processed_files = []
    for file_path in file_list:
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if not file_path.is_file():
            continue

        try:
            relative_path = file_path.relative_to(repo_path)
            processed_files.append(str(relative_path))

            # Convert bytes to KB
            file_size = file_path.stat().st_size / 1024  # bytes to KB
            total_size += file_size
            file_sizes.append(file_size)

            # Count file extensions
            ext = file_path.suffix.lower() or "no_extension"
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

    # Calculate stats (all in KB)
    file_count = len(processed_files)
    average_size = round(total_size / file_count, 2) if file_count > 0 else 0
    max_size = round(max(file_sizes, default=0), 2)
    min_size = round(min(file_sizes, default=0), 2)
    total_size = round(total_size, 2)

    # Save file list
    with open(file_list_path, "w", encoding="utf-8") as f:
        f.write("\n".join(processed_files))
    print(f"File list saved to {file_list_path}")

    # Generate summary
    summary = {
        "repository": repo_path.name,
        "total_files": file_count,
        "total_size_kb": total_size,
        "average_file_size_kb": average_size,
        "max_file_size_kb": max_size,
        "min_file_size_kb": min_size,
        "file_types": extension_counts,
        "total_tokens": total_tokens,
    }

    # Save summary as JSON
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    print(f"Summary saved to {summary_path}")

    # Generate visualization report
    create_visualization(summary, repo_path)
