from datetime import datetime
from typing import Optional
import logging
import feedparser

from .base import BaseScraper, ScrapedItem

class BlogScraper(BaseScraper):
    """Scraper for blog RSS/Atom feeds"""
    
    def __init__(self, feed_url: str, site_name: str):
        super().__init__(
            url=feed_url,
            storage_key=f"blog_{site_name}"
        )
        self.site_name = site_name
        
    async def fetch_latest(self) -> Optional[ScrapedItem]:
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
            logging.error(f"Error fetching blog feed: {e}")
            return None
            
    def get_item_id(self, item: ScrapedItem) -> str:
        return item.id
        
    def format_notification(self, item: ScrapedItem) -> str:
        return (
            f"New post on {self.site_name}!\n"
            f"Title: {item.title}\n"
            f"Read here: {item.url}"
        )
        
    def validate_item(self, item: ScrapedItem) -> bool:
        return bool(
            item.id and
            item.title and
            item.url and
            item.url.startswith(("http://", "https://"))
        )