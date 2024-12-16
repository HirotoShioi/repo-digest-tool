from typing import Optional

from sqlalchemy import create_engine
from sqlmodel import Field, Session, SQLModel, select

from repo_tool.core.summary import FileData, FileType, Summary


class FilterSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    repository_id: str
    include_patterns: Optional[str]
    exclude_patterns: Optional[str]
    max_file_size: Optional[int]


class SummaryCache(SQLModel, table=True):
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
        statement = select(FilterSettings).where(
            FilterSettings.repository_id == repository_id
        )
        return self.session.exec(statement).first()

    def create_or_update(self, settings: FilterSettings) -> FilterSettings:
        """
        FilterSettingsを作成または更新
        Returns the created or updated FilterSettings
        """
        existing = self.get_by_repository_id(settings.repository_id)
        if existing:
            existing.include_patterns = settings.include_patterns
            existing.exclude_patterns = settings.exclude_patterns
            existing.max_file_size = settings.max_file_size
            self.session.add(existing)
            self.session.commit()
            return existing

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
        statement = select(SummaryCache).where(
            SummaryCache.repository_id == repository_id
        )
        result = self.session.exec(statement).first()
        if result:
            return Summary.from_json(result.summary_json)
        return None

    def create_or_update(self, summary: Summary, last_updated: str) -> Summary:
        """
        Create or update SummaryCache
        Returns the created or updated Summary
        """
        repository_id = get_repository_id(summary.author, summary.repository)
        cache = SummaryCache(
            repository_id=repository_id,
            summary_json=summary.to_json(),
            last_updated=last_updated,
        )

        existing = self.session.exec(
            select(SummaryCache).where(SummaryCache.repository_id == repository_id)
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
        saved_summary = summary_cache_repository.create_or_update(
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
