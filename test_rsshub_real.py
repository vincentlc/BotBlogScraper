import asyncio
import logging
import sys
from typing import Optional
from src.scrapers.social_media import SocialMediaScraper
from src.scrapers.base import ScrapedItem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_social_media(
    instagram_username: str,
    rsshub_base: str = "https://rsshub.app",
    site_name: Optional[str] = None
) -> bool:
    """Test Social Media Scraper with a real account.
    
    Args:
        instagram_username: Instagram username to scrape (e.g., 'testaccount')
        rsshub_base: RSSHub base URL (default: https://rsshub.app)
        site_name: Display name for the site (default: based on username)
    
    Returns:
        True if successful, False otherwise
    """
    if site_name is None:
        site_name = f"Instagram @{instagram_username}"
    
    logger.info(f"Testing Social Media Scraper for @{instagram_username}")
    logger.info(f"Using RSSHub base: {rsshub_base}")
    
    try:
        # Create scraper with Instagram route
        scraper = SocialMediaScraper(
            route=f'/instagram/user/{instagram_username}',
            site_name=site_name,
            rsshub_base=rsshub_base
        )
        
        logger.info(f"Feed URL: {scraper.url}")
        
        # Fetch latest post
        logger.info("Fetching latest Instagram post...")
        result: Optional[ScrapedItem] = await scraper.fetch_latest()
        
        if result is None:
            logger.warning("No posts found in feed")
            return False
        
        # Display results
        logger.info("✓ Successfully fetched Instagram post!")
        logger.info(f"  ID: {result.id}")
        logger.info(f"  Title: {result.title}")
        logger.info(f"  URL: {result.url}")
        logger.info(f"  Timestamp: {result.timestamp}")
        logger.info(f"  Author: {result.content.get('author', 'Unknown')}")
        logger.info(f"  Summary: {result.content.get('summary', '')[:100]}...")
        logger.info(f"  Tags: {result.content.get('tags', [])}")
        
        # Validate item
        if scraper.validate_item(result):
            logger.info("✓ Item validation passed")
            return True
        else:
            logger.warning("✗ Item validation failed")
            return False
            
    except Exception as e:
        logger.error(f"✗ Error testing social media scraper: {e}", exc_info=True)
        return False


async def test_multiple_accounts(rsshub_base: str = "https://rsshub.app") -> None:
    """Test multiple Instagram accounts."""
    test_accounts = [
        ('testaccount1', 'Test Account 1'),
        ('testaccount2', 'Test Account 2'),
    ]
    
    results = {}
    for username, display_name in test_accounts:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing: {display_name} (@{username})")
        logger.info('='*60)
        
        success = await test_social_media(
            instagram_username=username,
            rsshub_base=rsshub_base,
            site_name=display_name
        )
        results[username] = success
        
        # Small delay between requests
        await asyncio.sleep(2)
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("SUMMARY")
    logger.info('='*60)
    for username, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        logger.info(f"{status}: @{username}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test Social Media Scraper with real feeds'
    )
    parser.add_argument(
        '--rsshub-base',
        default='https://rsshub.app',
        help='RSSHub base URL (default: https://rsshub.app)'
    )
    parser.add_argument(
        '--username',
        help='Test a specific Instagram username'
    )
    
    args = parser.parse_args()
    
    if args.username:
        # Test single account
        success = asyncio.run(
            test_social_media(
                instagram_username=args.username,
                rsshub_base=args.rsshub_base
            )
        )
        sys.exit(0 if success else 1)
    else:
        # Test multiple accounts
        asyncio.run(test_multiple_accounts(rsshub_base=args.rsshub_base))


if __name__ == '__main__':
    main()
