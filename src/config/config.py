from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

@dataclass
class TelegramConfig:
    token: str
    chat_id: str

@dataclass
class ScraperConfig:
    check_interval: int = 300  # 5 minutes default
    storage_dir: str = "storage"
    log_file: str = "bot.log"
    log_level: str = "INFO"

class Config:
    """Central configuration management"""
    
    def __init__(self, env_file: Optional[str] = None):
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
            
        # Validate and load Telegram config
        token = os.getenv('TELEGRAM_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not token or not chat_id:
            raise ValueError("TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set in environment")
            
        self.telegram = TelegramConfig(
            token=token,
            chat_id=chat_id
        )
        
        # Load scraper config with defaults
        self.scraper = ScraperConfig(
            check_interval=int(os.getenv('CHECK_INTERVAL', '300')),
            storage_dir=os.getenv('STORAGE_DIR', 'storage'),
            log_file=os.getenv('LOG_FILE', 'bot.log'),
            log_level=os.getenv('LOG_LEVEL', 'INFO')
        )
        
    @classmethod
    def load(cls, env_file: Optional[str] = None) -> 'Config':
        """Factory method to create config instance"""
        return cls(env_file)