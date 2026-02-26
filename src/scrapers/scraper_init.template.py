"""
Template for scraper initialization.

Make a private copy of this file at `src/scrapers/scraper_init.py` and fill in your
private/secret configuration (API keys, custom RSSHub base URLs, or local overrides).

Add `src/scrapers/scraper_init.py` to your `.gitignore` so private data isn't committed.

Example usage:
    def get_scrapers(config):
        return [
            SocialMediaScraper(route='/instagram/user/myaccount', site_name='My Instagram'),
            BlogScraper(feed_url='https://example.com/feed', site_name='Example Blog')
        ]

Note: This file is only a template and will not be imported by the app. Copy it to
`src/scrapers/scraper_init.py` to enable private initialization.

For social media routes, see RSSHUB_GUIDE.md for available routes and examples.
"""

from typing import List

from src.scrapers.blog import BlogScraper
from src.scrapers.social_media import SocialMediaScraper
from src.scrapers.manga import MangaScraper


def get_scrapers(config) -> List:
    """Return a list of scraper instances.

    Replace or extend this with your real private initialization.
    
    Examples of Social Media routes:
        /instagram/user/{username}      - Instagram user timeline
        /instagram/hashtag/{hashtag}    - Instagram hashtag posts
        /twitter/user/{user}            - Twitter timeline
        /tiktok/user/{user}             - TikTok videos
        /youtube/channel/{id}           - YouTube videos
        /reddit/subreddit/{name}        - Reddit posts
    """
    return [
        # Social media examples (using RSSHub)
        SocialMediaScraper(
            route='/instagram/user/municipiopuertovaras',
            site_name='Puerto Varas Municipality',
            rsshub_base='https://rsshub.app'  # or 'http://localhost:1200' if running locally
        ),
        # Blog examples (standard RSS/Atom feeds)
        BlogScraper(
            feed_url='https://leo.prie.to/tag/essay/feed',
            site_name="Leo's Essays"
        ),
        # Manga example
        MangaScraper(
            manga_name="one-piece",
            base_url="https://www.lelmanga.com"
        )
    ]
