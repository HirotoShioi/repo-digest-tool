import asyncio
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiofiles
import tiktoken
from jinja2 import Environment, FileSystemLoader

from repo_tool.core.contants import DIGEST_DIR

data_size = 20
precision = 2
encoding = tiktoken.get_encoding("o200k_base")


@dataclass
class FileInfo:
    """ファイル処理に必要な情報を保持するデータクラス"""

    file_path: Path
    repo_path: Path


@dataclass
class FileType:
    extension: str
    count: int
    tokens: int


@dataclass
class FileStats:
    file_count: int
    total_size: float
    average_size: float
    max_size: float
    min_size: float
    context_length: int
    extension_tokens: List[FileType] = field(default_factory=list)


@dataclass
class FileData:
    name: str
    path: str
    extension: str
    tokens: int


@dataclass
class Summary:
    repository: str
    total_files: int
    total_size_kb: float
    average_file_size_kb: float
    max_file_size_kb: float
    min_file_size_kb: float
    file_types: List[FileType]
    context_length: int
    file_data: List[FileData]

    def generate_report(self, data_size: int = 20) -> None:
        """
        HTMLレポートを生成して保存する
        """
        # Jinja2 環境を設定
        env = Environment(loader=FileSystemLoader("templates"))
        env.filters["format_number"] = format_number
        template = env.get_template("report.html")

        # ファイルタイプをトークン数でソート
        sorted_file_types = sorted(
            self.file_types, key=lambda x: x.tokens, reverse=True
        )[:data_size]

        html_content = template.render(
            repo_name=self.repository,
            summary=self,
            file_types_labels=[ft.extension for ft in sorted_file_types],
            file_types_data=[ft.tokens for ft in sorted_file_types],
            file_sizes_labels=[item.name for item in self.file_data[:data_size]],
            file_sizes_data=[item.tokens for item in self.file_data[:data_size]],
            file_sizes_paths=[item.path for item in self.file_data[:data_size]],
            all_files=self.file_data,
        )

        # HTMLレポートを保存
        report_path = f"digests/{self.repository}_report.html"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Report saved to {report_path}")


# カスタムフィルターを定義
def format_number(value: int | float | str) -> str:
    """数値をカンマ区切りにフォーマット"""
    if isinstance(value, (int, float)):
        return f"{value:,}"  # カンマ区切り
    return value


def generate_summary(
    repo_path: Path,
    file_list: List[Path],
) -> Summary:
    """
    ファイル統計のサマリーレポートを生成する
    """
    if not os.path.exists(DIGEST_DIR):
        os.makedirs(DIGEST_DIR, exist_ok=True)
    # レポートの生成
    # ファイルサイズデータの取得
    file_size_data = []

    for file_path in file_list:
        # 相対パスの処理を修正
        if isinstance(file_path, str):
            file_path = Path(file_path)

        try:
            relative_path = file_path.relative_to(repo_path)
        except ValueError:
            # すでに相対パスの場合はそのまま使用
            relative_path = file_path

        full_path = repo_path / relative_path
        if full_path.is_file():
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    tokens = len(encoding.encode(content))

                file_size_data.append(
                    FileData(
                        name=relative_path.name,
                        path=str(relative_path),
                        extension=relative_path.suffix.lower() or "no_extension",
                        tokens=tokens,
                    )
                )
            except Exception as e:
                print(f"Error processing file {relative_path}: {e}")
                continue
    # Sort by token count
    file_size_data.sort(key=lambda x: x.tokens, reverse=True)

    file_infos = [FileInfo(Path(f), repo_path) for f in file_list]
    # 非同期処理の実行と結果の取得
    stats = asyncio.run(process_files(file_infos))

    # サマリーの生成
    summary = Summary(
        repository=repo_path.name,
        total_files=stats.file_count,
        total_size_kb=round(stats.total_size, precision),
        average_file_size_kb=round(stats.average_size, precision),
        max_file_size_kb=round(stats.max_size, precision),
        min_file_size_kb=round(stats.min_size, precision),
        file_types=stats.extension_tokens,
        context_length=stats.context_length,
        file_data=file_size_data,
    )
    return summary


async def process_files(file_infos: List[FileInfo]) -> FileStats:
    """
    全ファイルの非同期処理と集計を行う
    """
    extension_data: Dict[str, Dict[str, int]] = {}  # 一時的な集計用辞書
    total_size = 0
    file_sizes = []
    context_length = 0
    processed_files = []

    tasks = [process_single_file(file_info) for file_info in file_infos]
    results = await asyncio.gather(*tasks)

    for result in results:
        if result is None:
            continue

        processed_files.append(result["path"])
        total_size += result["size"]
        context_length += result["tokens"]
        file_sizes.append(result["size"])

        ext = result["extension"]
        if ext not in extension_data:
            extension_data[ext] = {"count": 0, "tokens": 0}
        extension_data[ext]["count"] += 1
        extension_data[ext]["tokens"] += result["tokens"]

    # 辞書からFileTypeのリストに変換
    extension_tokens = [
        FileType(extension=ext, count=data["count"], tokens=data["tokens"])
        for ext, data in extension_data.items()
    ]

    file_count = len(processed_files)
    return FileStats(
        file_count=file_count,
        total_size=total_size,
        average_size=total_size / file_count if file_count > 0 else 0,
        max_size=max(file_sizes, default=0),
        min_size=min(file_sizes, default=0),
        extension_tokens=extension_tokens,
        context_length=context_length,
    )


async def process_single_file(file_info: FileInfo) -> Optional[Dict[str, Any]]:
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
