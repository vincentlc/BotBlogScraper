from setuptools import setup, find_packages

setup(
    name="content-update-bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.3",
        "feedparser>=6.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "lark-parser>=0.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
        ],
    },
    python_requires=">=3.7",
)