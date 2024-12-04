from pathlib import Path
from typing import List, Dict, Any
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import asyncio

load_dotenv()

default_model = "gpt-4o-mini"
default_temperature = 0
default_batch_size = 20


class FileInfo(BaseModel):
    path: str = Field(description="File path")


class FilteredFiles(BaseModel):
    files: List[FileInfo] = Field(
        description="Filtered file list that is suitable for ChatGPT"
    )


async def filter_files_batch(
    file_batch: List[Path], prompt: str, llm_chain
) -> List[Path]:
    """単一のバッチに対するファイルフィルタリングを実行"""
    file_info = [
        {"path": str(file), "size": os.path.getsize(file)}
        for file in file_batch
        if file.is_file()
    ]

    # invoke を使用して同期的に実行
    result = await llm_chain.ainvoke(
        {
            "file_info": "\n".join(
                [f"{file['path']}: {file['size']} bytes" for file in file_info]
            ),
            "user_prompt": prompt,
        }
    )
    return [Path(file_info.path) for file_info in result.files]


async def filter_files_with_llm_in_batch(
    file_list: List[Path], prompt: str, batch_size: int = 50
) -> List[Path]:
    print("Using LLM to filter files in parallel...")

    # プロンプトテンプレートの作成
    template = """
Filter files from a GitHub repository based on relevance to create a digest suitable for input into ChatGPT by excluding irrelevant files such as CI/CD, configuration files, binary files, and compiled files.

Consider files relevant if they contain source code, documentation, or other text-based content that provides insights into project functionality. Make use of given file paths and sizes to assist in filtering decisions.

# Steps

1. **Identify and List Files**: Begin with a list of file paths located in the /tmp directory, ensuring paths are in the format `tmp/query/examples/react/load-more-infinite-scroll/tsconfig.json`.

2. **Identify Irrelevant Files**: Recognize file types that are generally considered irrelevant (CI/CD configurations, binary files, compiled files, etc.) These might include:
   - `.gitignore`
   - `.github/` directories
   - Files with extensions like `.exe`, `.dll`, `.tar`, `.zip`, `.class`, etc.
   - Any continuous integration files such as those in `.circleci`, `.travis.yml`

3. **Filter with Assistance from File Size**: Use the file size as an additional metric to assist in determining relevance, potentially prioritizing smaller text files over larger, likely binary, files.

4. **Filter Relevant Files**: Choose files that contain essential information:
   - Source code files (e.g., `.py`, `.java`, `.cpp`)
   - README and other documentation files (`README.md`, `.txt`, etc.)
   - License files (`LICENSE`)
   - Important script files (`install.sh`, etc.)

# Output Format

The output should be a single, consolidated text file that includes the content of only relevant files from the repository, in a readable and organized manner suitable for text ingestion.

# Examples

**Example 1:**
- **Input**: Repository containing files with paths and sizes such as `tmp/query/examples/react/load-more-infinite-scroll/main.py` (2KB), `tmp/query/readme/README.md` (1KB), `tmp/bin/app.exe` (5MB), `tmp/config/.travis.yml` (3KB)
- **Output**: Consolidated text file content from `main.py` and `README.md`.

(Note: Real examples should include a larger and more diverse file set to demonstrate complexity in file filtering and size-based relevance.)

# Notes

- Edge Cases: Consider cases where files may have unusual extensions but are text-based. Ensure these are not wrongly excluded.
- Pay special attention to nested directories that might contain relevant files.
- The relevance of certain file types might vary depending on the repository's specific nature, and adjustments may be necessary based on context.
- File size should be used to filter out unusually large files that are less likely to be relevant as text inputs.
- File path should not be modified in any way.

# Input
{file_info}

# User Prompt
{user_prompt}
    """

    prompt_template = ChatPromptTemplate.from_template(template)

    # LLMチェーンの作成
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
    ).with_structured_output(FilteredFiles)
    llm_chain = prompt_template | llm

    # ファイルリストをバッチに分割
    batches = [
        file_list[i : i + batch_size] for i in range(0, len(file_list), batch_size)
    ]

    # 各バッチを並行処理
    tasks = []
    for batch in batches:
        task = asyncio.create_task(filter_files_batch(batch, prompt, llm_chain))
        tasks.append(task)

    # すべてのタスクを実行して結果を待機
    results = await asyncio.gather(*tasks)

    # 結果を結合
    filtered_files = [file for batch_result in results for file in batch_result]

    print(
        f"Finished filtering {len(file_list)} files with LLM in {len(batches)} batches."
    )
    return filtered_files


# 同期的なインターフェースを提供するラッパー関数
def filter_files_with_llm(
    file_list: List[Path], prompt: str, batch_size: int = 50
) -> List[Path]:
    return asyncio.run(filter_files_with_llm_in_batch(file_list, prompt, batch_size))
