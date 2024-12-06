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
Filter files from a GitHub repository based on relevance by excluding irrelevant files such as CI/CD, configuration files, binary files, and compiled files.

You will receive a list of file paths and their associated sizes. Your task is to assess each file path and determine if it is relevant for creating a digest suitable for input into ChatGPT. Exclude files that are commonly not useful for summaries or understanding, such as CI/CD, configuration files, binary files, and compiled files.

# Steps

1. **Identify File Types**: Examine the file paths and identify the types of files they represent.
2. **Determine Relevance**: Use the following guidelines to determine if a file should be excluded:
   - Exclude files typically irrelevant for summaries:
     - Continuous Integration/Continuous Deployment (CI/CD) files (e.g., `.github/workflows/`, `.gitlab-ci.yml`)
     - Configuration files (e.g., `*.config`, `config.yaml`)
     - Binary files (e.g., `*.exe`, `*.bin`, `*.dll`)
     - Compiled files (e.g., `*.class`, `*.o`, `*.pyc`)
     - Other non-source code files that do not contribute to code understanding (e.g., `*.log`, `*.tmp`)
3. **Filter Files**: Create a list that only includes the files deemed relevant based on the above criteria.

# Notes

- Only focus on the file path suffix in determining file type.
- Consider common conventions for CI/CD and configuration files.
- This process is to ensure only the potentially most relevant files for understanding the repository's code are included.
- Do not modify the file paths in the output in any way.

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
