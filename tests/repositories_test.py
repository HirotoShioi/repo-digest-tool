# type: ignore
from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel, create_engine

from repo_tool.api.repositories import (
    FilterSettingsRepository,
    SummaryCacheRepository,
    get_repository_id,
)
from repo_tool.core.filter import FilterSettings
from repo_tool.core.summary import FileData, FileType, Summary


@pytest.fixture(name="session")
def session_fixture():
    # Create in-memory database for testing
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def filter_settings_repository(session):
    return FilterSettingsRepository(session)


@pytest.fixture
def summary_cache_repository(session):
    return SummaryCacheRepository(session)


@pytest.fixture
def sample_summary():
    file_types = [FileType(extension=".py", count=10, tokens=1000)]
    file_data = [
        FileData(name="test.py", path="/test.py", extension=".py", tokens=100),
        FileData(
            name="日本語.py", path="/path/to/日本語.py", extension=".py", tokens=100
        ),
        FileData(
            name="with space.py",
            path="/path/with space.py",
            extension=".py",
            tokens=100,
        ),
        FileData(
            name="special#$@!.py", path="/special#$@!.py", extension=".py", tokens=100
        ),
        FileData(
            name='with"quote".py', path='/with"quote".py', extension=".py", tokens=100
        ),
    ]

    return Summary(
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


class TestFilterSettingsRepository:
    def test_get_repository_id(self):
        assert get_repository_id("author", "repo") == "author/repo"

    def test_get_nonexistent_settings(self, filter_settings_repository):
        settings = filter_settings_repository.get_by_repository_id("nonexistent/repo")
        assert settings is None

    def test_create_and_get_settings(self, filter_settings_repository):
        # Create settings
        settings = filter_settings_repository.upsert(
            repository_id="test/repo",
            include_patterns=["*.py"],
            exclude_patterns=["*.pyc"],
            max_file_size=1000,
        )

        assert isinstance(settings, FilterSettings)
        assert settings.include_patterns == ["*.py"]
        assert settings.exclude_patterns == ["*.pyc"]
        assert settings.max_file_size == 1000

        # Get settings
        retrieved = filter_settings_repository.get_by_repository_id("test/repo")
        assert retrieved is not None
        assert retrieved.include_patterns == ["*.py"]
        assert retrieved.exclude_patterns == ["*.pyc"]
        assert retrieved.max_file_size == 1000

    def test_update_settings(self, filter_settings_repository):
        # Create initial settings
        filter_settings_repository.upsert(
            repository_id="test/repo",
            include_patterns=["*.py"],
            exclude_patterns=["*.pyc"],
            max_file_size=1000,
        )

        # Update settings
        updated = filter_settings_repository.upsert(
            repository_id="test/repo",
            include_patterns=["*.js"],
            exclude_patterns=["*.min.js"],
            max_file_size=2000,
        )

        assert updated.include_patterns == ["*.js"]
        assert updated.exclude_patterns == ["*.min.js"]
        assert updated.max_file_size == 2000

        # Verify update
        retrieved = filter_settings_repository.get_by_repository_id("test/repo")
        assert retrieved is not None
        assert retrieved.include_patterns == ["*.js"]
        assert retrieved.exclude_patterns == ["*.min.js"]
        assert retrieved.max_file_size == 2000

    def test_delete_settings(self, filter_settings_repository):
        # Create settings
        filter_settings_repository.upsert(
            repository_id="test/repo",
            include_patterns=["*.py"],
            exclude_patterns=["*.pyc"],
            max_file_size=1000,
        )

        # Delete settings
        result = filter_settings_repository.delete_by_repository_id("test/repo")
        assert result is True

        # Verify deletion
        settings = filter_settings_repository.get_by_repository_id("test/repo")
        assert settings is None

    def test_delete_nonexistent_settings(self, filter_settings_repository):
        result = filter_settings_repository.delete_by_repository_id("nonexistent/repo")
        assert result is False

    def test_delete_all_settings(self, filter_settings_repository):
        # Create multiple settings
        for i in range(3):
            filter_settings_repository.upsert(
                repository_id=f"test/repo{i}",
                include_patterns=["*.py"],
                exclude_patterns=["*.pyc"],
                max_file_size=1000,
            )

        # Delete all settings
        filter_settings_repository.delete_all()

        # Verify all settings are deleted
        for i in range(3):
            settings = filter_settings_repository.get_by_repository_id(f"test/repo{i}")
            assert settings is None


class TestSummaryCacheRepository:
    def test_get_nonexistent_summary(self, summary_cache_repository):
        summary = summary_cache_repository.get_by_repository_id("nonexistent/repo")
        assert summary is None

    def test_create_and_get_summary(self, summary_cache_repository, sample_summary):
        # Create summary cache
        current_time = datetime.now().isoformat()
        saved_summary = summary_cache_repository.upsert(
            summary=sample_summary, last_updated=current_time
        )

        assert isinstance(saved_summary, Summary)
        assert saved_summary.author == "test"
        assert saved_summary.repository == "repo"

        # Get summary
        retrieved = summary_cache_repository.get_by_repository_id("test/repo")
        assert retrieved is not None
        assert retrieved.author == "test"
        assert retrieved.repository == "repo"
        assert len(retrieved.file_types) == 1
        assert len(retrieved.file_data) == 1

    def test_update_summary(self, summary_cache_repository, sample_summary):
        # Create initial summary
        current_time = datetime.now().isoformat()
        summary_cache_repository.upsert(
            summary=sample_summary, last_updated=current_time
        )

        # Update summary with new data
        updated_summary = Summary(
            author=sample_summary.author,
            repository=sample_summary.repository,
            total_files=20,
            total_size_kb=sample_summary.total_size_kb,
            average_file_size_kb=sample_summary.average_file_size_kb,
            max_file_size_kb=sample_summary.max_file_size_kb,
            min_file_size_kb=sample_summary.min_file_size_kb,
            file_types=sample_summary.file_types,
            context_length=sample_summary.context_length,
            file_data=sample_summary.file_data,
        )

        new_time = datetime.now().isoformat()

        updated = summary_cache_repository.upsert(
            summary=updated_summary, last_updated=new_time
        )

        assert updated.total_files == 20

        # Verify update
        retrieved = summary_cache_repository.get_by_repository_id("test/repo")
        assert retrieved is not None
        assert retrieved.total_files == 20

    def test_delete_summary(self, summary_cache_repository, sample_summary):
        # Create summary
        current_time = datetime.now().isoformat()
        summary_cache_repository.upsert(
            summary=sample_summary, last_updated=current_time
        )

        # Delete summary
        result = summary_cache_repository.delete_by_repository_id("test/repo")
        assert result is True

        # Verify deletion
        summary = summary_cache_repository.get_by_repository_id("test/repo")
        assert summary is None

    def test_delete_nonexistent_summary(self, summary_cache_repository):
        result = summary_cache_repository.delete_by_repository_id("nonexistent/repo")
        assert result is False

    def test_delete_all_summaries(self, summary_cache_repository, sample_summary):
        current_time = datetime.now().isoformat()

        # Create multiple summaries
        for i in range(3):
            modified_summary = Summary(
                author=sample_summary.author,
                repository=f"repo{i}",
                total_files=sample_summary.total_files,
                total_size_kb=sample_summary.total_size_kb,
                average_file_size_kb=sample_summary.average_file_size_kb,
                max_file_size_kb=sample_summary.max_file_size_kb,
                min_file_size_kb=sample_summary.min_file_size_kb,
                file_types=sample_summary.file_types,
                context_length=sample_summary.context_length,
                file_data=sample_summary.file_data,
            )
            summary_cache_repository.upsert(
                summary=modified_summary, last_updated=current_time
            )

        # Delete all summaries
        summary_cache_repository.delete_all()

        # Verify all summaries are deleted
        for i in range(3):
            summary = summary_cache_repository.get_by_repository_id(f"test/repo{i}")
            assert summary is None
