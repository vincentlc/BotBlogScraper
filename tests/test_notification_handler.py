import pytest
from unittest.mock import patch, AsyncMock
from src.notifications.handler import NotificationHandler, TelegramConfig

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
    
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.post.return_value.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await notification_handler.send_telegram("Test message")
        
    assert result is True
    mock_session.post.assert_called_once()

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