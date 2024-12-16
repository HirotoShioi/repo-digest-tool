import json
from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy import create_engine
from sqlmodel import Field, Session, SQLModel, select

from repo_tool.core.summary import FileData, FileType, Summary


@dataclass
class FilterSettings:
    include_patterns: List[str]
    exclude_patterns: List[str]
    max_file_size: int

    @staticmethod
    def from_json(json_str: str) -> "FilterSettings":
        return FilterSettings(**json.loads(json_str))

    def to_json(self) -> str:
        return json.dumps(self, ensure_ascii=False, default=lambda o: o.__dict__)


class FilterSettingsTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    repository_id: str
    settings: str


class SummaryCacheTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    repository_id: str
    summary_json: str  # Store JSON string of Summary
    last_updated: str


def get_repository_id(author: str, repository_name: str) -> str:
    return f"{author}/{repository_name}"


class FilterSettingsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_repository_id(self, repository_id: str) -> Optional[FilterSettings]:
        """
        リポジトリIDでFilterSettingsを取得
        """
        statement = select(FilterSettingsTable).where(
            FilterSettingsTable.repository_id == repository_id
        )
        result = self.session.exec(statement).first()
        if result:
            return FilterSettings.from_json(result.settings)
        return None

    def upsert(
        self,
        repository_id: str,
        include_patterns: List[str],
        exclude_patterns: List[str],
        max_file_size: int,
    ) -> FilterSettings:
        """
        FilterSettingsを作成または更新
        Returns the created or updated FilterSettings
        """
        existing = self.get_by_repository_id(repository_id)
        if existing:
            self.session.add(existing)
            self.session.commit()
            return existing

        settings = FilterSettings(
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            max_file_size=max_file_size,
        )
        self.session.add(settings)
        self.session.commit()
        return settings

    def delete_by_repository_id(self, repository_id: str) -> bool:
        """
        リポジトリIDでFilterSettingsを削除
        """
        existing = self.get_by_repository_id(repository_id)
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return True
        return False


class SummaryCacheRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_repository_id(self, repository_id: str) -> Optional[Summary]:
        """
        Get Summary by repository ID
        """
        statement = select(SummaryCacheTable).where(
            SummaryCacheTable.repository_id == repository_id
        )
        result = self.session.exec(statement).first()
        if result:
            return Summary.from_json(result.summary_json)
        return None

    def upsert(self, summary: Summary, last_updated: str) -> Summary:
        """
        Create or update SummaryCache
        Returns the created or updated Summary
        """
        repository_id = get_repository_id(summary.author, summary.repository)
        cache = SummaryCacheTable(
            repository_id=repository_id,
            summary_json=summary.to_json(),
            last_updated=last_updated,
        )

        existing = self.session.exec(
            select(SummaryCacheTable).where(
                SummaryCacheTable.repository_id == repository_id
            )
        ).first()

        if existing:
            existing.summary_json = cache.summary_json
            existing.last_updated = cache.last_updated
            self.session.add(existing)
            self.session.commit()
            return summary

        self.session.add(cache)
        self.session.commit()
        return summary

    def delete_by_repository_id(self, repository_id: str) -> bool:
        """
        リポジトリIDでSummaryCacheを削除
        """
        existing = self.get_by_repository_id(repository_id)
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return True
        return False


def main() -> None:
    engine = create_engine("sqlite:///repo_tool.db")
    SQLModel.metadata.create_all(engine)

    session = Session(engine)
    summary_cache_repository = SummaryCacheRepository(session)

    try:
        # Create test summary
        file_types = [FileType(extension=".py", count=10, tokens=1000)]
        file_data = [
            FileData(name="test.py", path="/test.py", extension=".py", tokens=100)
        ]

        summary = Summary(
            author="test",
            repository="repo",
            total_files=10,
            total_size_kb=100.0,
            average_file_size_kb=10.0,
            max_file_size_kb=20.0,
            min_file_size_kb=5.0,
            file_types=file_types,
            context_length=1000,
            file_data=file_data,
        )

        # Save summary
        saved_summary = summary_cache_repository.upsert(
            summary=summary, last_updated="2024-01-01"
        )
        print("Saved Summary:", saved_summary.repository)

        # Retrieve summary
        retrieved_summary = summary_cache_repository.get_by_repository_id("test/repo")
        if retrieved_summary:
            print("Retrieved Summary:", retrieved_summary.repository)
            print("File Types:", retrieved_summary.file_types)

    finally:
        session.close()


if __name__ == "__main__":
    main()
