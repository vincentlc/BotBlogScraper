import math
from datetime import datetime
from typing import Optional
import logging
import aiohttp
from bs4 import BeautifulSoup

from .base import BaseScraper, ScrapedItem

class MangaScraper(BaseScraper):
    """Scraper for manga chapters"""
    
    def __init__(self, manga_name: str, base_url: str):
        super().__init__(
            url=f"{base_url}/manga/{manga_name}",
            storage_key=f"manga_{manga_name}"
        )
        self.manga_name = manga_name
        self.base_url = base_url
        
    async def fetch_latest(self) -> Optional[ScrapedItem]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status != 200:
                        logging.error(f"Failed to fetch {self.url}: {response.status}")
                        return None
                        
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find the chapter list
                    chapter_items = soup.find_all('li', attrs={"data-num": True})
                    if not chapter_items:
                        logging.error("Chapter list not found")
                        return None

                    # Extract data-num attributes and find the latest
                    list_chapter = [li.get('data-num') for li in chapter_items]
                    # logging.info(f"{list_chapter}")
                    data_nums = [math.trunc(float(li.get('data-num').split(" ")[0])) for li in chapter_items]
                    
                    # Sort chapters in descending order and find first valid (non-RAW, non-Oneshot)
                    sorted_chapters = sorted(zip(data_nums, list_chapter), key=lambda x: x[0], reverse=True)
                    
                    for chapter_num, chapter_str in sorted_chapters:
                        if chapter_num == 0:
                            continue
                        if "RAW" in chapter_str or "Oneshot" in chapter_str:
                            logging.info(f"Skipping chapter {chapter_num} due to RAW/Oneshot tag")
                            continue
                        # Found a valid chapter
                        return ScrapedItem(
                            id=str(chapter_num),
                            title=f"{self.manga_name.title()} Chapter {chapter_num}",
                            url=f"{self.base_url}/{self.manga_name}-{chapter_num}",
                            timestamp=datetime.now(),
                            content={"chapter_number": chapter_num}
                        )
                    
                    # No valid chapter found
                    return None
                    
        except Exception as e:
            logging.error(f"Error fetching manga chapter: {e}")
            return None
            
    def get_item_id(self, item: ScrapedItem) -> str:
        return str(item.content["chapter_number"])
        
    def format_notification(self, item: ScrapedItem) -> str:
        return (
            f"¡Nuevo capítulo de {item.title} disponible!\n"
            f"Puedes leerlo aquí: {item.url}"
        )
        
    def validate_item(self, item: ScrapedItem) -> bool:
        return (
            item.id.isdigit() and
            "chapter_number" in item.content and
            isinstance(item.content["chapter_number"], int)
        )