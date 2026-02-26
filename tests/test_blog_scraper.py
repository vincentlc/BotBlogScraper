import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import feedparser
from src.scrapers.blog import BlogScraper

@pytest.mark.asyncio
async def test_blog_scraper_fetch_latest():
    """Test blog scraper fetching latest post"""
    # Setup
    scraper = BlogScraper("https://test.com/feed", "Test Blog")
    
    # Create mock entry using MagicMock to support get method properly
    mock_entry = MagicMock()
    mock_entry.id = 'test123'
    mock_entry.title = 'Test Post'
    mock_entry.link = 'https://test.com/post/1'
    mock_entry.published_parsed = (2025, 11, 6, 12, 0, 0)
    
    # Setup get method to return values for author, summary, tags
    def mock_get(key, default=''):
        data = {
            'author': 'Test Author',
            'summary': 'Test summary',
            'tags': [MagicMock(term='test')]
        }
        return data.get(key, default)
    
    mock_entry.get = mock_get
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value.entries = [mock_entry]
        result = await scraper.fetch_latest()
    
    # Assert
    assert result is not None
    assert result.id == 'test123'
    assert result.title == 'Test Post'
    assert result.url == 'https://test.com/post/1'
    assert result.content['author'] == 'Test Author'
    assert result.content['tags'] == ['test']

@pytest.mark.asyncio
async def test_blog_scraper_no_entries():
    """Test blog scraper when no entries are found"""
    scraper = BlogScraper("https://test.com/feed", "Test Blog")
    
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value.entries = []
        result = await scraper.fetch_latest()
    
    assert result is None

def test_blog_scraper_format_notification(sample_scraped_item):
    """Test notification formatting"""
    scraper = BlogScraper("https://test.com/feed", "Test Blog")
    message = scraper.format_notification(sample_scraped_item)
    
    assert "Test Blog" in message
    assert sample_scraped_item.title in message
    assert sample_scraped_item.url in message