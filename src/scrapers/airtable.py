from datetime import datetime
from typing import Any, Dict, List, Optional
import logging
import aiohttp
import json

from .base import BaseScraper, ScrapedItem

class AirtableScraper(BaseScraper):
    """Scraper for Airtable tables with country news"""
    
    COUNTRIES = ["Chile", "Argentina", "Peru", "Colombia", "Mexico"]
    
    def __init__(self, base_id: str, table_id: str, view_id: str = ""):
        self.base_url = f"https://api.airtable.com/v0/{base_id}/{table_id}"
        if view_id:
            self.base_url += f"?view={view_id}"
            
        super().__init__(
            url=self.base_url,
            storage_key=f"airtable_{table_id}"
        )
        self.logger = logging.getLogger(__name__)
        
    async def fetch_latest(self) -> Optional[ScrapedItem]:
        """Fetch latest entries from Airtable"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url) as response:
                    if response.status != 200:
                        self.logger.error(f"Error fetching from Airtable: {response.status}")
                        return None
                    
                    data = await response.json()
                    records = data.get('records', [])
                    
                    if not records:
                        return None
                
            # Get the most recent record
            latest = records[0]
            
            # Check if this is a country we're interested in
            country = latest['fields'].get('Country', '')
            if country not in self.COUNTRIES and country != 'Austria':  # Austria incluido para testing
                return None
            
            # Build content dictionary with all subfields
            content = {
                'country': country,
                'subItems': latest['fields'].get('Items', []),
                'description': latest['fields'].get('Description', ''),
                'category': latest['fields'].get('Category', ''),
                'status': latest['fields'].get('Status', '')
            }
            
            # Convert Airtable timestamp to datetime
            timestamp_str = latest['fields'].get('Last modified', '')
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                timestamp = datetime.utcnow()
            
            return ScrapedItem(
                id=latest['id'],
                title=f"New update for {country}",
                url=self.url,
                timestamp=timestamp,
                content=content
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching from Airtable: {e}")
            return None
    
    def get_item_id(self, item: Dict[str, Any]) -> str:
        """Extract unique identifier from Airtable record"""
        return item['id']
    
    def format_notification(self, item: ScrapedItem) -> str:
        """Format notification message for country updates"""
        country = item.content['country']
        items = item.content['subItems']
        description = item.content['description']
        category = item.content['category']
        
        message = [
            f"🌎 New update for {country}",
            f"Category: {category}",
            f"Description: {description}",
        ]
        
        if items:
            message.append("\nItems:")
            for sub_item in items:
                message.append(f"• {sub_item}")
                
        message.append(f"\nStatus: {item.content['status']}")
        message.append(f"Last modified: {item.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        return "\n".join(message)
    
    def validate_item(self, item: ScrapedItem) -> bool:
        """Validate that the scraped item has all required fields"""
        return (
            item.id and
            item.content.get('country') and
            item.content.get('country') in (self.COUNTRIES + ['Austria'])
        )