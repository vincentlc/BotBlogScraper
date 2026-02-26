"""
Social Media Scraper using RSSHub.

This module provides scrapers for social media platforms through RSSHub,
making it easy to convert social media feeds into standard RSS/Atom feeds.

Supports: Instagram, Twitter, TikTok, YouTube, Reddit, and many more.

See: https://docs.rsshub.app/ for available routes.
"""

from datetime import datetime
from typing import Optional
import logging
import feedparser
from urllib.parse import urljoin

from .base import BaseScraper, ScrapedItem


class SocialMediaScraper(BaseScraper):
    """Generic scraper for RSSHub-generated social media feeds.

    Uses RSSHub to convert social media timelines into RSS/Atom feeds.
    Supports any platform with a RSSHub route.

    Examples:
        Instagram: /instagram/user/{username}
        Twitter: /twitter/user/{user}
        TikTok: /tiktok/user/{user}
        YouTube: /youtube/channel/{id}
        Reddit: /reddit/subreddit/{name}
    """

    def __init__(
        self,
        route: str,
        site_name: str,
        rsshub_base: str = "https://rsshub.app"
    ):
        """Initialize Social Media Scraper.

        Args:
            route: RSSHub route (e.g., '/instagram/user/username')
            site_name: Display name for the social media source
            rsshub_base: Base URL of RSSHub instance
        """
        # Build full feed URL from base + route
        full_route = route.lstrip('/')
        feed_url = urljoin(
            rsshub_base if rsshub_base.endswith('/') else rsshub_base + '/',
            full_route
        )
        
        super().__init__(
            url=feed_url,
            storage_key=f"social_{site_name}"
        )
        self.site_name = site_name
        self.route = route
        self.rsshub_base = rsshub_base

    async def fetch_latest(self) -> Optional[ScrapedItem]:
        """Fetch the latest post from the social media feed."""
        try:
            feed = feedparser.parse(self.url)

            if not feed.entries:
                logging.error(f"No entries found in feed: {self.url}")
                return None

            latest_entry = feed.entries[0]

            # Get the published date, fallback to current time if not available
            try:
                timestamp = datetime(*latest_entry.published_parsed[:6])
            except (AttributeError, TypeError):
                timestamp = datetime.now()

            return ScrapedItem(
                id=latest_entry.id if hasattr(latest_entry, 'id') else latest_entry.link,
                title=latest_entry.title,
                url=latest_entry.link,
                timestamp=timestamp,
                content={
                    "author": latest_entry.get("author", "Unknown"),
                    "summary": latest_entry.get("summary", ""),
                    "tags": [tag.term for tag in latest_entry.get("tags", [])]
                }
            )

        except Exception as e:
            logging.error(f"Error fetching social media feed: {e}")
            return None

    def get_item_id(self, item: ScrapedItem) -> str:
        """Extract unique identifier from scraped item."""
        return item.id

    def format_notification(self, item: ScrapedItem) -> str:
        """Format the notification message for social media content."""
        return (
            f"New post on {self.site_name}!\n"
            f"Title: {item.title}\n"
            f"Read here: {item.url}"
        )

    def validate_item(self, item: ScrapedItem) -> bool:
        """Validate that the scraped item has all required fields."""
        return bool(
            item.id and
            item.title and
            item.url and
            item.url.startswith(("http://", "https://"))
        )
