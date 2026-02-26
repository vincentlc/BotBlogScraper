import pytest
from unittest.mock import patch, MagicMock
from src.scrapers.social_media import SocialMediaScraper


@pytest.mark.asyncio
async def test_social_media_scraper_fetch_latest():
    """Test SocialMediaScraper building feed URL and fetching latest entry"""
    scraper = SocialMediaScraper(
        route='/twitter/user/testuser',
        site_name="Test User"
    )

    # Create mock entry using MagicMock to support get method properly
    mock_entry = MagicMock()
    mock_entry.id = 'tweet_123'
    mock_entry.title = 'Test Tweet'
    mock_entry.link = 'https://twitter.com/testuser/status/123'
    mock_entry.published_parsed = (2025, 11, 6, 12, 0, 0)

    def mock_get(key, default=''):
        data = {
            'author': 'Test User',
            'summary': 'Test tweet summary',
            'tags': [MagicMock(term='test')]
        }
        return data.get(key, default)

    mock_entry.get = mock_get

    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value.entries = [mock_entry]
        result = await scraper.fetch_latest()

    assert result is not None
    assert result.id == 'tweet_123'
    assert result.title == 'Test Tweet'
    assert result.url == 'https://twitter.com/testuser/status/123'
    assert result.content['author'] == 'Test User'


@pytest.mark.asyncio
async def test_social_media_scraper_no_entries():
    """Test SocialMediaScraper when no entries are found"""
    scraper = SocialMediaScraper(
        route='/tiktok/user/testuser',
        site_name="Test TikTok"
    )

    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value.entries = []
        result = await scraper.fetch_latest()

    assert result is None


def test_social_media_scraper_format_notification(sample_scraped_item):
    """Test notification formatting for social media"""
    scraper = SocialMediaScraper(
        route='/instagram/user/testuser',
        site_name='Test Instagram'
    )
    message = scraper.format_notification(sample_scraped_item)

    assert "Test Instagram" in message
    assert sample_scraped_item.title in message
    assert sample_scraped_item.url in message


@pytest.mark.asyncio
async def test_social_media_instagram_scraper():
    """Test SocialMediaScraper specifically for Instagram routes"""
    # RSSHub Instagram route format: /instagram/user/{username}
    scraper = SocialMediaScraper(
        route='/instagram/user/testaccount',
        site_name='Test Instagram Account'
    )

    # Verify the feed URL is built correctly
    assert 'instagram/user/testaccount' in scraper.url
    assert scraper.url.startswith('https://rsshub.app/')

    # Create mock Instagram post entry
    mock_entry = MagicMock()
    mock_entry.id = 'insta_12345'
    mock_entry.title = 'Instagram Post'
    mock_entry.link = 'https://instagram.com/p/ABC123/'
    mock_entry.published_parsed = (2025, 12, 17, 10, 30, 0)

    def mock_get(key, default=''):
        data = {
            'author': 'testaccount',
            'summary': 'Instagram post content',
            'tags': [MagicMock(term='instagram'), MagicMock(term='test')]
        }
        return data.get(key, default)

    mock_entry.get = mock_get

    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value.entries = [mock_entry]
        result = await scraper.fetch_latest()

    # Assert
    assert result is not None
    assert result.id == 'insta_12345'
    assert result.title == 'Instagram Post'
    assert result.url == 'https://instagram.com/p/ABC123/'
    assert result.content['author'] == 'testaccount'
    assert len(result.content['tags']) == 2


@pytest.mark.asyncio
async def test_social_media_url_construction():
    """Test that SocialMediaScraper correctly constructs feed URLs"""
    test_cases = [
        # (route, expected_url_part, platform)
        ('/instagram/user/testuser', 'instagram/user/testuser', 'Instagram'),
        ('/twitter/user/testuser', 'twitter/user/testuser', 'Twitter'),
        ('/tiktok/user/testuser', 'tiktok/user/testuser', 'TikTok'),
        ('/youtube/channel/123', 'youtube/channel/123', 'YouTube'),
        ('/reddit/subreddit/test', 'reddit/subreddit/test', 'Reddit'),
    ]

    for route, expected_part, platform in test_cases:
        scraper = SocialMediaScraper(route=route, site_name=platform)
        assert expected_part in scraper.url, f"Expected {expected_part} in {scraper.url}"
        assert scraper.url.startswith('https://rsshub.app/'), (
            f"URL {scraper.url} doesn't start with correct base"
        )


def test_social_media_scraper_with_custom_base():
    """Test SocialMediaScraper with custom RSSHub base URL"""
    scraper = SocialMediaScraper(
        route='/instagram/user/testuser',
        site_name='Test',
        rsshub_base='http://localhost:1200'
    )

    assert 'localhost:1200' in scraper.url
    assert scraper.url.startswith('http://localhost:1200/')


def test_social_media_validate_item(sample_scraped_item):
    """Test item validation"""
    scraper = SocialMediaScraper(
        route='/instagram/user/testuser',
        site_name='Test'
    )

    # Valid item
    assert scraper.validate_item(sample_scraped_item) is True

    # Invalid item (missing URL)
    invalid_item = sample_scraped_item
    invalid_item.url = ''
    assert scraper.validate_item(invalid_item) is False
