# Content Update Bot

A flexible, extensible bot for tracking updates across different content sources (manga chapters, blog posts, etc.) and sending notifications through Telegram.

## Features

- Object-oriented design with easy-to-extend base classes
- Support for multiple content sources:
  - Manga chapter updates
  - Blog post feeds
- Persistent storage of latest items
- Telegram notifications
- Async implementation for efficient polling
- Configurable check intervals
- Comprehensive test suite
- Secure systemd service integration

## Setup

1. Clone the repository
2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install package and dependencies:
```bash
# For development (includes testing tools)
pip install -e ".[dev]"

# For production only
pip install -e .
```

4. Create a `.env` file with your configuration:
```env
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
CHECK_INTERVAL=300  # Optional, defaults to 300 seconds
STORAGE_DIR=storage  # Optional, defaults to 'storage'
LOG_FILE=bot.log  # Optional, defaults to 'bot.log'
LOG_LEVEL=INFO  # Optional, defaults to 'INFO'
```

## Usage

### Running Manually

Run the bot directly:
```bash
python main.py
```

### Running as a Service

Install and start the systemd service:
```bash
sudo ./install_service.sh
```

This will:
1. Create a virtual environment if needed
2. Install dependencies
3. Set up the systemd service
4. Start the bot

Check service status:
```bash
systemctl status content-update-bot
```

After making changes to the service file:
```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Restart the service
sudo systemctl restart content-update-bot
```

View logs:
```bash
journalctl -u content-update-bot -f
```

### Development and Testing

Run the test suite:
```bash
# Activate virtual environment first
source venv/bin/activate

# Run tests with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_manga_scraper.py -v

# Format code
black src/ tests/
isort src/ tests/
```

## Adding New Content Sources

1. Create a new scraper class that inherits from `BaseScraper`
2. Implement the required methods:
   - `fetch_latest()`: Fetch the latest item
   - `get_item_id()`: Extract unique identifier
   - `format_notification()`: Format notification message
   - `validate_item()`: Validate scraped item

Example:
```python
class MyNewScraper(BaseScraper):
    async def fetch_latest(self) -> Optional[ScrapedItem]:
        # Implementation here
        pass
```

3. Add your new scraper to the list in `main.py`

## Project Structure

```
src/
  ├── scrapers/
  │   ├── base.py      # Base scraper class
  │   ├── manga.py     # Manga-specific scraper
  │   └── blog.py      # Blog-specific scraper
  ├── storage/
  │   └── handler.py   # Persistent storage handling
  ├── notifications/
  │   └── handler.py   # Notification handling
  └── bot/
      └── manager.py   # Main bot logic
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## License

MIT License - feel free to use and modify as needed.