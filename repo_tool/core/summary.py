import os
from pathlib import Path
from typing import List, Dict
import asyncio
import aiofiles
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader
import tiktoken

data_size = 20
precision = 2


# カスタムフィルターを定義
def format_number(value):
    """数値をカンマ区切りにフォーマット"""
    if isinstance(value, (int, float)):
        return f"{value:,}"  # カンマ区切り
    return value


def create_visualization(summary: dict, repo_path: Path, files: List[Path]):
    """
    Create HTML report with Chart.js visualizations using Jinja2
    """
    # ファイルサイズデータの取得
    file_size_data = []
    repo_dir = Path(f"tmp/{repo_path.name}")

    for file_path in files:
        # 相対パスの処理を修正
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # tmp/repo-name/を除去して相対パスを取得
        try:
            relative_path = file_path.relative_to(repo_dir)
        except ValueError:
            # すでに相対パスの場合はそのまま使用
            relative_path = file_path

        full_path = repo_dir / relative_path
        if full_path.is_file():
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    tokens = len(encoding.encode(content))

                file_size_data.append(
                    {
                        "name": relative_path.name,
                        "path": str(relative_path),
                        "extension": relative_path.suffix.lower() or "no_extension",
                        "tokens": tokens,
                    }
                )
            except Exception as e:
                print(f"Error processing file {relative_path}: {e}")
                continue

    # トークン数でソート
    file_size_data.sort(key=lambda x: x["tokens"], reverse=True)

    # Jinja2環境の設定
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["format_number"] = format_number
    template = env.get_template("report.html")

    # テンプレートにデータを渡す際にall_filesを確実に含める
    html_content = template.render(
        repo_name=repo_path.name,
        summary=summary,
        file_types_labels=[
            ext
            for ext, _ in sorted(
                summary["file_types"].items(), key=lambda x: x[1], reverse=True
            )[:data_size]
        ],
        file_types_data=[
            count
            for _, count in sorted(
                summary["file_types"].items(), key=lambda x: x[1], reverse=True
            )[:data_size]
        ],
        file_sizes_labels=[item["name"] for item in file_size_data[:data_size]],
        file_sizes_data=[item["tokens"] for item in file_size_data[:data_size]],
        file_sizes_paths=[item["path"] for item in file_size_data[:data_size]],
        all_files=file_size_data,  # 全ファイルデータを確実に渡す
    )

    # Save HTML report
    report_path = f"digests/{repo_path.name}_report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Report saved to {report_path}")


encoding = tiktoken.get_encoding("o200k_base")


@dataclass
class FileInfo:
    """ファイル処理に必要な情報を保持するデータクラス"""

    file_path: Path
    repo_path: Path


async def process_single_file(file_info: FileInfo) -> Dict:
    """
    単一ファイルの非同期処理を行う補助関数
    """
    try:
        relative_path = str(file_info.file_path.relative_to(file_info.repo_path))

        async with aiofiles.open(
            file_info.file_path, "r", encoding="utf-8", errors="ignore"
        ) as f:
            content = await f.read()
            tokens = len(encoding.encode(content))

        file_size = file_info.file_path.stat().st_size / 1024  # bytes to KB
        ext = file_info.file_path.suffix.lower() or "no_extension"

        return {
            "path": relative_path,
            "size": file_size,
            "tokens": tokens,
            "extension": ext,
        }
    except Exception as e:
        print(f"Error processing file {file_info.file_path}: {e}")
        return None


async def process_files(file_infos: List[FileInfo]) -> Dict:
    """
    全ファイルの非同期処理と集計を行う
    """
    extension_tokens = {}
    total_size = 0
    file_sizes = []
    total_tokens = 0
    processed_files = []

    tasks = [process_single_file(file_info) for file_info in file_infos]
    results = await asyncio.gather(*tasks)

    for result in results:
        if result is None:
            continue

        processed_files.append(result["path"])
        total_size += result["size"]
        total_tokens += result["tokens"]
        file_sizes.append(result["size"])

        ext = result["extension"]
        extension_tokens[ext] = extension_tokens.get(ext, 0) + result["tokens"]

    file_count = len(processed_files)
    return {
        "file_count": file_count,
        "total_size": total_size,
        "average_size": total_size / file_count if file_count > 0 else 0,
        "max_size": max(file_sizes, default=0),
        "min_size": min(file_sizes, default=0),
        "extension_tokens": extension_tokens,
        "total_tokens": total_tokens,
    }


def generate_summary(
    repo_path: Path,
    file_list: List[Path],
):
    """
    ファイル統計のサマリーレポートを生成する
    """
    os.makedirs("digests", exist_ok=True)
    file_infos = [FileInfo(Path(f), repo_path) for f in file_list]

    # 非同期処理の実行と結果の取得
    stats = asyncio.run(process_files(file_infos))

    # サマリーの生成
    summary = {
        "repository": repo_path.name,
        "total_files": stats["file_count"],
        "total_size_kb": round(stats["total_size"], precision),
        "average_file_size_kb": round(stats["average_size"], precision),
        "max_file_size_kb": round(stats["max_size"], precision),
        "min_file_size_kb": round(stats["min_size"], precision),
        "file_types": stats["extension_tokens"],
        "total_tokens": stats["total_tokens"],
    }

    # レポートの生成
    create_visualization(summary, repo_path, file_list)


def generated_file(repo_path: Path, filtered_files: List[Path]) -> None:
    """
    Generates a digest from the filtered files in the repository.
    Includes a file list at the beginning of the output.
    """
    if not filtered_files:
        print("No matching files found.")
        return

    # 出力ディレクトリとファイルパスの設定
    output_dir = Path("digests")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"{repo_path.name}.txt"

    with open(output_path, "w", encoding="utf-8") as output:
        # Add preamble
        output.write(
            "The following text represents the contents of the repository.\n"
            "Each section begins with ----, followed by the file path and name.\n"
            "A file list is provided at the beginning. End of repository content is marked by --END--.\n\n"
        )

        # ファイルのみを処理
        file_list = [f for f in filtered_files if f.is_file()]

        # Add file contents
        for file_path in file_list:
            try:
                relative_path = file_path.relative_to(repo_path)
                output.write("----\n")  # Section divider
                output.write(f"{relative_path}\n")  # File path

                # ファイルを1行ずつ読み込んで処理
                with file_path.open("r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        output.write(line)
                output.write("\n")

            except Exception as e:
                # Log the error and continue
                relative_path = file_path.relative_to(repo_path)
                output.write("----\n")
                output.write(f"{relative_path}\n")
                output.write(f"Error reading file: {e}\n\n")

        output.write("--END--")  # End marker