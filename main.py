import asyncio
import logging
from src.config.config import Config
from src.scrapers.manga import MangaScraper
from src.scrapers.blog import BlogScraper
from src.scrapers.social_media import SocialMediaScraper
from src.storage.handler import StorageHandler
from src.notifications.handler import NotificationHandler
from src.bot.manager import BotManager

def setup_logging(config):
    """Configure logging based on config"""
    logging.basicConfig(
        level=getattr(logging, config.scraper.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=config.scraper.log_file
    )

def main():
    # Load configuration
    config = Config.load()
    
    # Setup logging
    setup_logging(config)
    
    # Initialize components
    notifier = NotificationHandler(telegram_config=config.telegram)
    storage = StorageHandler(storage_dir=config.scraper.storage_dir)
    
    # Initialize scrapers, prefer a private initializer if available
    try:
        from src.scrapers.scraper_init import get_scrapers  # pragma: no cover - optional private file
        scrapers = get_scrapers(config)
    except (ImportError, ModuleNotFoundError, AttributeError):
        logging.warning("Private scraper initializer not found or invalid, using default scrapers.")
        scrapers = [
            # Example blog scraper
            BlogScraper(
                feed_url="https://leo.prie.to/tag/essay/feed",
                site_name="Leo's Essays"
            ),
            # Example manga scraper
            MangaScraper(
                manga_name="one-piece",
                base_url="https://www.lelmanga.com"
            )
        ]
    
    # Initialize bot manager
    bot = BotManager(
        scrapers=scrapers,
        storage=storage,
        notifier=notifier,
        check_interval=300  # Check every 5 minutes
    )
    
    # Run the bot
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot stopped due to error: {e}")

if __name__ == "__main__":
    main()