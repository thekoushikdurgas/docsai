"""
LinkedIn Job Scraper Package
Contains modules for scraping job postings from LinkedIn.
"""

__version__ = "1.0.0"
__author__ = "LinkedIn Job Scraper Team"

from .linkedin_scraper import LinkedInJobScraper
from .data_processor import DataProcessor
from .url_builder import URLBuilder
from .rate_limiter import RateLimiter

__all__ = [
    'LinkedInJobScraper',
    'DataProcessor', 
    'URLBuilder',
    'RateLimiter'
]
