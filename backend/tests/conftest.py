"""
Pytest configuration and fixtures for ScholarMind tests.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_database():
    """Mock database connection for unit tests."""
    mock_db = Mock()
    mock_db.execute = AsyncMock()
    mock_db.fetch = AsyncMock()
    mock_db.commit = AsyncMock()
    mock_db.rollback = AsyncMock()
    return mock_db


@pytest.fixture
def mock_vector_db():
    """Mock vector database client for unit tests."""
    mock_vector_db = Mock()
    mock_vector_db.add_documents = Mock()
    mock_vector_db.query = Mock()
    mock_vector_db.delete = Mock()
    return mock_vector_db


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for unit tests."""
    mock_client = Mock()
    mock_client.embeddings = Mock()
    mock_client.chat = Mock()
    return mock_client


@pytest.fixture(scope="session")
def test_config(temp_dir):
    """Test configuration settings."""
    upload_dir = temp_dir / "test_uploads"
    upload_dir.mkdir(exist_ok=True)

    return {
        "database_url": "postgresql://test:test@localhost:5432/test_db",
        "vector_db_url": "http://localhost:8001",
        "openai_api_key": "test-api-key",
        "upload_dir": str(upload_dir),
        "max_file_size": 10 * 1024 * 1024,  # 10MB for tests
    }


@pytest.fixture(autouse=True)
def setup_test_environment(temp_dir):
    """Setup test environment variables."""
    upload_dir = temp_dir / "test_uploads"
    upload_dir.mkdir(exist_ok=True)

    test_env = {
        "TESTING": "true",
        "DATABASE_URL": "postgresql://test:test@localhost:5432/test_db",
        "VECTOR_DB_URL": "http://localhost:8001",
        "OPENAI_API_KEY": "test-api-key",
        "UPLOAD_DIR": str(upload_dir),
    }

    # Store original values
    original_env = {}
    for key, value in test_env.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value

    yield

    # Restore original values
    for key, original_value in original_env.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value
