import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.scrapers.manga import MangaScraper

@pytest.mark.asyncio
async def test_manga_scraper_fetch_latest():
    """Test manga scraper fetching latest chapter"""
    # Setup
    scraper = MangaScraper("test-manga", "https://test.com")
    
    # Create mock response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value="""
        <html>
            <li data-num="123"></li>
            <li data-num="124"></li>
            <li data-num="125"></li>
        </html>
    """)
    
    # Create mock session
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.get.return_value.__aenter__.return_value = mock_response
    
    # Test
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await scraper.fetch_latest()
    
    # Assert
    assert result is not None
    assert result.id == "125"
    assert "125" in result.url
    assert result.content["chapter_number"] == 125

@pytest.mark.asyncio
async def test_manga_scraper_no_chapters(mock_session, mock_response):
    """Test manga scraper when no chapters are found"""
    scraper = MangaScraper("test-manga", "https://test.com")
    mock_response.text = AsyncMock(return_value="<html></html>")
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await scraper.fetch_latest()
    
    assert result is None

def test_manga_scraper_format_notification(sample_scraped_item):
    """Test notification formatting"""
    scraper = MangaScraper("test-manga", "https://test.com")
    message = scraper.format_notification(sample_scraped_item)
    
    assert sample_scraped_item.title in message
    assert sample_scraped_item.url in message

import pytest
from bs4 import BeautifulSoup
from unittest.mock import Mock, AsyncMock

from src.scrapers.manga import MangaScraper
from datetime import datetime

@pytest.fixture
def manga_scraper():
    return MangaScraper("test-manga", "http://test.com")

@pytest.mark.asyncio
async def test_skip_raw_chapter():
    """Test that RAW chapters are skipped"""
    scraper = MangaScraper("test-manga", "https://test.com")
    
    # Create mock response with RAW chapter
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value="""
        <html>
            <li data-num="123 RAW">Chapter 123 RAW</li>
            <li data-num="122">Chapter 122</li>
        </html>
    """)
    
    # Create mock session
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.get.return_value.__aenter__.return_value = mock_response
    
    # Test
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await scraper.fetch_latest()
    
    # Verify that we get chapter 122 instead of RAW 123
    assert result is not None
    assert result.id == "122"
    assert result.content["chapter_number"] == 122

@pytest.mark.asyncio
async def test_skip_oneshot_chapter():
    """Test that Oneshot chapters are skipped"""
    scraper = MangaScraper("test-manga", "https://test.com")
    
    # Create mock response with Oneshot chapter
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.text = AsyncMock(return_value="""
        <html>
            <li data-num="1 Oneshot">Chapter 1 Oneshot</li>
            <li data-num="2">Chapter 2</li>
        </html>
    """)
    
    # Create mock session
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.get.return_value.__aenter__.return_value = mock_response
    
    # Test
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await scraper.fetch_latest()
    
    # Verify that we get chapter 2 instead of Oneshot
    assert result is not None
    assert result.id == "2"
    assert result.content["chapter_number"] == 2