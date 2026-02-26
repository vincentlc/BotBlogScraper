import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.notifications.handler import NotificationHandler, TelegramConfig


class AsyncContextManagerMock:
    """A mock that properly acts as an async context manager"""
    def __init__(self, return_value):
        self.return_value = return_value
    
    async def __aenter__(self):
        return self.return_value
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None


@pytest.fixture
def telegram_config():
    return TelegramConfig(
        token="test_token",
        chat_id="test_chat_id"
    )

@pytest.fixture
def notification_handler(telegram_config):
    return NotificationHandler(telegram_config)

@pytest.mark.asyncio
async def test_send_telegram_success(notification_handler):
    """Test successful Telegram message sending"""
    mock_response = AsyncMock()
    mock_response.status = 200
    
    # Create mock session instance
    mock_session_instance = MagicMock()
    mock_session_instance.post.return_value = AsyncContextManagerMock(mock_response)
    
    # Create mock session class that returns the instance
    mock_session_class = MagicMock(return_value=mock_session_instance)
    mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session_instance)
    mock_session_class.return_value.__aexit__ = AsyncMock(return_value=None)
    
    with patch('src.notifications.handler.aiohttp.ClientSession', mock_session_class):
        result = await notification_handler.send_telegram("Test message")
        
    assert result is True
    mock_session_instance.post.assert_called_once()

@pytest.mark.asyncio
async def test_send_telegram_failure(notification_handler):
    """Test Telegram message sending failure"""
    mock_response = AsyncMock()
    mock_response.status = 400
    
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.post.return_value.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await notification_handler.send_telegram("Test message")
        
    assert result is False

@pytest.mark.asyncio
async def test_send_telegram_no_config():
    """Test sending without Telegram configuration"""
    handler = NotificationHandler(telegram_config=None)
    result = await handler.send_telegram("Test message")
    assert result is False

@pytest.mark.asyncio
async def test_send_telegram_network_error(notification_handler):
    """Test handling of network errors"""
    with patch('aiohttp.ClientSession', side_effect=Exception("Network error")):
        result = await notification_handler.send_telegram("Test message")
        
    assert result is False