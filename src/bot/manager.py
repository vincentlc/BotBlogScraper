import asyncio
import logging
from typing import List, Optional
from datetime import datetime

from ..scrapers.base import BaseScraper, ScrapedItem
from ..storage.handler import StorageHandler
from ..notifications.handler import NotificationHandler, TelegramConfig

class BotManager:
    """Manages multiple scrapers and handles updates"""
    
    def __init__(
        self,
        scrapers: List[BaseScraper],
        storage: StorageHandler,
        notifier: NotificationHandler,
        check_interval: int = 300  # 5 minutes
    ):
        self.scrapers = scrapers
        self.storage = storage
        self.notifier = notifier
        self.check_interval = check_interval
        
    async def check_scraper(self, scraper: BaseScraper) -> Optional[ScrapedItem]:
        """Check a single scraper for updates"""
        try:
            # Get latest item from scraper
            latest_item = await scraper.fetch_latest()
            if not latest_item or not scraper.validate_item(latest_item):
                return None
                
            # Get previously stored item
            stored_data = self.storage.get_latest(scraper.storage_key)
            stored_id = stored_data.get("id") if stored_data else None
            
            # If we have a new item
            if not stored_id or latest_item.id != stored_id:
                # Store the new item
                self.storage.store_latest(
                    scraper.storage_key,
                    {
                        "id": latest_item.id,
                        "title": latest_item.title,
                        "url": latest_item.url,
                        "timestamp": latest_item.timestamp.isoformat(),
                        "content": latest_item.content
                    }
                )
                return latest_item
                
        except Exception as e:
            logging.error(f"Error checking scraper {scraper.__class__.__name__}: {e}")
            
        return None
        
    async def check_all_scrapers(self):
        """Check all scrapers for updates"""
        for scraper in self.scrapers:
            if new_item := await self.check_scraper(scraper):
                # Send notification
                message = scraper.format_notification(new_item)
                await self.notifier.send_telegram(message)
                
    async def run(self):
        """Run the bot manager in a loop"""
        while True:
            try:
                await self.check_all_scrapers()
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                
            await asyncio.sleep(self.check_interval)