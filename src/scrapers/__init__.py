"""
Scrapers package for content aggregation.

Available scrapers:
- BlogScraper: For standard RSS/Atom feeds
- SocialMediaScraper: For social media via RSSHub
- MangaScraper: For manga sites
"""

from .base import BaseScraper, ScrapedItem
from .blog import BlogScraper
from .social_media import SocialMediaScraper
from .manga import MangaScraper

__all__ = [
    'BaseScraper',
    'ScrapedItem',
    'BlogScraper',
    'SocialMediaScraper',
    'MangaScraper',
]
