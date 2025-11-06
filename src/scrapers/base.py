from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass
class ScrapedItem:
    """Base class for scraped items"""
    id: str
    title: str
    url: str
    timestamp: datetime
    content: Dict[str, Any]

class BaseScraper(ABC):
    """Abstract base class for all scrapers"""
    
    def __init__(self, url: str, storage_key: str):
        self.url = url
        self.storage_key = storage_key
        
    @abstractmethod
    async def fetch_latest(self) -> Optional[ScrapedItem]:
        """Fetch the latest item from the source"""
        pass
    
    @abstractmethod
    def get_item_id(self, item: Any) -> str:
        """Extract unique identifier from scraped item"""
        pass
    
    @abstractmethod
    def format_notification(self, item: ScrapedItem) -> str:
        """Format the notification message for this type of content"""
        pass

    @abstractmethod
    def validate_item(self, item: ScrapedItem) -> bool:
        """Validate that the scraped item has all required fields"""
        pass