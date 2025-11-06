from typing import Optional
import logging
import aiohttp
from dataclasses import dataclass

@dataclass
class TelegramConfig:
    token: str
    chat_id: str

class NotificationHandler:
    """Handles sending notifications through various channels"""
    
    def __init__(self, telegram_config: Optional[TelegramConfig] = None):
        self.telegram_config = telegram_config
        
    async def send_telegram(self, message: str) -> bool:
        """Send a message through Telegram"""
        if not self.telegram_config:
            logging.error("Telegram configuration not provided")
            return False
            
        try:
            url = f"https://api.telegram.org/bot{self.telegram_config.token}/sendMessage"
            data = {
                "chat_id": self.telegram_config.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as response:
                    if response.status != 200:
                        logging.error(f"Failed to send Telegram message: {response.status}")
                        return False
                    return True
                    
        except Exception as e:
            logging.error(f"Error sending Telegram message: {e}")
            return False