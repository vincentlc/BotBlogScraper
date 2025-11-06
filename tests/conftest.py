import pytest
import os
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from src.config.config import Config
from src.scrapers.base import ScrapedItem

@pytest.fixture
def mock_config():
    """Provides a test configuration"""
    with patch('src.config.config.load_dotenv'):
        with patch.dict(os.environ, {
            'TELEGRAM_TOKEN': 'test_token',
            'TELEGRAM_CHAT_ID': 'test_chat_id',
            'CHECK_INTERVAL': '60',
            'STORAGE_DIR': 'test_storage'
        }):
            return Config.load()

@pytest.fixture
def sample_scraped_item():
    """Provides a sample scraped item for testing"""
    return ScrapedItem(
        id="123",
        title="Test Item",
        url="https://test.com/123",
        timestamp=datetime.now(),
        content={"test_key": "test_value"}
    )

@pytest.fixture
def mock_response():
    """Provides a mock response for HTTP requests"""
    mock = MagicMock()
    mock.status = 200
    mock.text = AsyncMock(return_value="<html>Test content</html>")
    return mock

@pytest.fixture
def mock_session():
    """Provides a mock aiohttp ClientSession"""
    mock = AsyncMock()
    mock.__aenter__ = AsyncMock()
    mock.__aexit__ = AsyncMock()
    return mock