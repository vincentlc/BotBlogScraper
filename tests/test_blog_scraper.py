import pytest
from unittest.mock import patch, AsyncMock
import feedparser
from src.scrapers.blog import BlogScraper

@pytest.mark.asyncio
async def test_blog_scraper_fetch_latest():
    """Test blog scraper fetching latest post"""
    # Setup
    scraper = BlogScraper("https://test.com/feed", "Test Blog")
    
    mock_entry = {
        'id': 'test123',
        'title': 'Test Post',
        'link': 'https://test.com/post/1',
        'published_parsed': (2025, 11, 6, 12, 0, 0),
        'author': 'Test Author',
        'summary': 'Test summary',
        'tags': [type('TestTag', (), {'term': 'test'})()]
    }
    
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