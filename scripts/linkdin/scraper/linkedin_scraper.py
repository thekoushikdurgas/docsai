"""
LinkedIn Job Scraper Module
Handles the scraping of job postings from LinkedIn using BeautifulSoup and requests.
Enhanced with comprehensive logging, error handling, and anti-detection measures.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import re
from urllib.parse import urlencode, quote_plus
from datetime import datetime, timedelta
import json
import logging
from typing import List, Dict, Optional, Any
import hashlib
from dataclasses import dataclass
from enum import Enum

# Set up logging
logger = logging.getLogger(__name__)

class JobType(Enum):
    """Enum for job types"""
    FULL_TIME = "F"
    PART_TIME = "P"
    CONTRACT = "C"
    TEMPORARY = "T"
    INTERNSHIP = "I"

class ExperienceLevel(Enum):
    """Enum for experience levels"""
    INTERNSHIP = "1"
    ENTRY_LEVEL = "2"
    ASSOCIATE = "3"
    MID_SENIOR = "4"
    DIRECTOR = "5"
    EXECUTIVE = "6"

@dataclass
class ScrapingConfig:
    """Configuration class for scraping parameters"""
    delay_range: tuple = (2, 5)
    max_retries: int = 3
    max_pages: int = 5
    respect_robots_txt: bool = True
    user_agent_rotation: bool = True
    timeout: int = 30
    follow_redirects: bool = True

class ScrapingError(Exception):
    """Custom exception for scraping errors"""
    pass

class LinkedInJobScraper:
    """
    LinkedIn job scraper with rate limiting and anti-detection measures.
    Enhanced with comprehensive logging and error handling.
    """
    
    def __init__(self, config: Optional[ScrapingConfig] = None):
        """
        Initialize the scraper with configuration.
        
        Args:
            config: ScrapingConfig object with scraping parameters
        """
        self.config = config or ScrapingConfig()
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.ua = UserAgent()
        self.session = requests.Session()
        
        # Configure session
        self.session.timeout = self.config.timeout
        self.session.max_redirects = 10 if self.config.follow_redirects else 0
        
        # Initialize logging
        logger.info("Initializing LinkedIn Job Scraper")
        logger.debug(f"Configuration: {self.config}")
        
        # Statistics tracking
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'jobs_scraped': 0,
            'pages_scraped': 0
        }
        
    def get_headers(self) -> Dict[str, str]:
        """
        Generate random headers to avoid detection.
        
        Returns:
            Dict containing HTTP headers
        """
        headers = {
            'User-Agent': self.ua.random if self.config.user_agent_rotation else self.ua.chrome,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        
        logger.debug(f"Generated headers: {headers['User-Agent']}")
        return headers
    
    def build_search_url(self, job_title: str, location: str, start: int = 0, 
                        filters: Optional[Dict] = None) -> str:
        """
        Build LinkedIn job search URL with parameters.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            start: Starting position for pagination
            filters: Additional filters to apply
            
        Returns:
            Complete LinkedIn search URL
        """
        params = {
            'keywords': job_title,
            'location': location,
            'start': start,
            'sortBy': 'DD',  # Sort by date posted
            'f_TPR': 'r86400'  # Past 24 hours by default
        }
        
        # Add additional filters if provided
        if filters:
            if filters.get('job_type') and filters['job_type'] != 'All':
                job_type_value = self._get_job_type_value(filters['job_type'])
                if job_type_value:
                    params['f_JT'] = job_type_value
            
            if filters.get('experience_level') and filters['experience_level'] != 'All':
                exp_value = self._get_experience_value(filters['experience_level'])
                if exp_value:
                    params['f_E'] = exp_value
            
            if filters.get('date_posted') and filters['date_posted'] != 'All':
                date_value = self._get_date_value(filters['date_posted'])
                if date_value:
                    params['f_TPR'] = date_value
        
        url = f"{self.base_url}?{urlencode(params)}"
        logger.debug(f"Built search URL: {url}")
        return url
    
    def _get_job_type_value(self, job_type: str) -> Optional[str]:
        """Convert job type string to LinkedIn parameter value"""
        job_type_map = {
            'Full-time': JobType.FULL_TIME.value,
            'Part-time': JobType.PART_TIME.value,
            'Contract': JobType.CONTRACT.value,
            'Temporary': JobType.TEMPORARY.value,
            'Internship': JobType.INTERNSHIP.value
        }
        return job_type_map.get(job_type)
    
    def _get_experience_value(self, experience: str) -> Optional[str]:
        """Convert experience level string to LinkedIn parameter value"""
        exp_map = {
            'Internship': ExperienceLevel.INTERNSHIP.value,
            'Entry level': ExperienceLevel.ENTRY_LEVEL.value,
            'Associate': ExperienceLevel.ASSOCIATE.value,
            'Mid-Senior level': ExperienceLevel.MID_SENIOR.value,
            'Director': ExperienceLevel.DIRECTOR.value,
            'Executive': ExperienceLevel.EXECUTIVE.value
        }
        return exp_map.get(experience)
    
    def _get_date_value(self, date_posted: str) -> Optional[str]:
        """Convert date posted string to LinkedIn parameter value"""
        date_map = {
            'Past 24 hours': 'r86400',
            'Past week': 'r604800',
            'Past month': 'r2592000',
            'Any time': 'r86400'
        }
        return date_map.get(date_posted)
    
    def scrape_jobs(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Main method to scrape jobs based on configuration.
        
        Args:
            config: Dictionary containing scraping configuration
            
        Returns:
            List of scraped job dictionaries
        """
        logger.info(f"Starting job scraping with config: {config}")
        
        job_title = config.get('job_title', '')
        location = config.get('location', '')
        max_pages = config.get('max_pages', 3)
        filters = {
            'job_type': config.get('job_type', 'All'),
            'experience_level': config.get('experience_level', 'All'),
            'date_posted': config.get('date_posted', 'Past week')
        }
        
        all_jobs = []
        
        try:
            for page in range(max_pages):
                start = page * 25  # LinkedIn shows 25 jobs per page
                
                logger.info(f"Scraping page {page + 1} of {max_pages}")
                
                # Build search URL
                search_url = self.build_search_url(job_title, location, start, filters)
                
                # Get job listings from this page
                page_jobs = self._scrape_page(search_url)
                
                if page_jobs:
                    logger.info(f"Found {len(page_jobs)} jobs on page {page + 1}")
                    
                    # Get detailed information for each job
                    detailed_jobs = []
                    for i, job in enumerate(page_jobs):
                        logger.debug(f"Processing job {i + 1}/{len(page_jobs)}: {job.get('title', 'Unknown')}")
                        
                        detailed_job = self._get_job_details(job)
                        if detailed_job:
                            detailed_jobs.append(detailed_job)
                            self.stats['jobs_scraped'] += 1
                        
                        # Random delay to avoid rate limiting
                        delay = random.uniform(*self.config.delay_range)
                        logger.debug(f"Waiting {delay:.2f} seconds before next job")
                        time.sleep(delay)
                    
                    all_jobs.extend(detailed_jobs)
                    self.stats['pages_scraped'] += 1
                else:
                    logger.warning(f"No jobs found on page {page + 1}")
                
                # Delay between pages
                page_delay = random.uniform(3, 7)
                logger.debug(f"Waiting {page_delay:.2f} seconds before next page")
                time.sleep(page_delay)
                
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            raise ScrapingError(f"Scraping failed: {str(e)}")
        
        logger.info(f"Scraping completed. Total jobs scraped: {len(all_jobs)}")
        logger.info(f"Scraping statistics: {self.stats}")
        return all_jobs
    
    def _scrape_page(self, url: str) -> List[Dict[str, Any]]:
        """
        Scrape a single page of job listings.
        
        Args:
            url: URL of the page to scrape
            
        Returns:
            List of job dictionaries
        """
        jobs = []
        
        try:
            logger.debug(f"Requesting page: {url}")
            response = self._make_request(url)
            
            if not response:
                logger.warning("Failed to get response from page")
                return jobs
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards - LinkedIn uses various class names
            job_cards = self._find_job_cards(soup)
            logger.debug(f"Found {len(job_cards)} job cards on page")
            
            for i, card in enumerate(job_cards):
                try:
                    job = self._extract_job_from_card(card)
                    if job and self._validate_job_data(job):
                        jobs.append(job)
                        logger.debug(f"Successfully extracted job {i + 1}: {job.get('title', 'Unknown')}")
                    else:
                        logger.debug(f"Failed to extract or validate job {i + 1}")
                except Exception as e:
                    logger.error(f"Error extracting job {i + 1}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping page: {str(e)}")
            
        return jobs
    
    def _make_request(self, url: str) -> Optional[requests.Response]:
        """
        Make HTTP request with retry logic and error handling.
        
        Args:
            url: URL to request
            
        Returns:
            Response object or None if failed
        """
        for attempt in range(self.config.max_retries):
            try:
                logger.debug(f"Making request (attempt {attempt + 1}/{self.config.max_retries})")
                
                response = self.session.get(url, headers=self.get_headers())
                self.stats['total_requests'] += 1
                
                response.raise_for_status()
                self.stats['successful_requests'] += 1
                
                logger.debug(f"Request successful. Status: {response.status_code}")
                return response
                
            except requests.exceptions.RequestException as e:
                self.stats['failed_requests'] += 1
                logger.warning(f"Request failed (attempt {attempt + 1}): {str(e)}")
                
                if attempt < self.config.max_retries - 1:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    logger.debug(f"Retrying in {delay:.2f} seconds")
                    time.sleep(delay)
                else:
                    logger.error(f"All retry attempts failed for URL: {url}")
                    
        return None
    
    def _find_job_cards(self, soup: BeautifulSoup) -> List:
        """
        Find job card elements in the HTML.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            List of job card elements
        """
        # Common patterns for LinkedIn job cards
        job_card_selectors = [
            'div[data-job-id]',
            'div.job-search-card',
            'li.job-result-card',
            'div[class*="job-card"]',
            'div[class*="result-card"]',
            'li[class*="job"]'
        ]
        
        job_cards = []
        for selector in job_card_selectors:
            cards = soup.select(selector)
            if cards:
                logger.debug(f"Found {len(cards)} job cards using selector: {selector}")
                job_cards.extend(cards)
                break
        
        # Fallback: look for any div with job-related classes
        if not job_cards:
            job_cards = soup.find_all(['div', 'li'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['job', 'result', 'card', 'listing']
            ))
            logger.debug(f"Fallback: Found {len(job_cards)} job cards")
        
        return job_cards
    
    def _extract_job_from_card(self, card) -> Optional[Dict[str, Any]]:
        """
        Extract job information from a job card element.
        
        Args:
            card: BeautifulSoup element representing a job card
            
        Returns:
            Dictionary containing job information or None if extraction fails
        """
        try:
            job = {}
            
            # Job title
            title_elem = self._find_element_by_patterns(card, ['h3', 'h2', 'a'], 
                                                      ['title', 'job-title', 'position'])
            if not title_elem:
                title_elem = card.find('a')
            job['title'] = self._clean_text(title_elem.get_text()) if title_elem else ''
            
            # Company name
            company_elem = self._find_element_by_patterns(card, ['span', 'div', 'a'], 
                                                        ['company', 'employer', 'organization'])
            job['company'] = self._clean_text(company_elem.get_text()) if company_elem else ''
            
            # Location
            location_elem = self._find_element_by_patterns(card, ['span', 'div'], 
                                                         ['location', 'place', 'city'])
            job['location'] = self._clean_text(location_elem.get_text()) if location_elem else ''
            
            # Job URL
            link_elem = card.find('a', href=True)
            job['url'] = link_elem['href'] if link_elem else ''
            if job['url'] and not job['url'].startswith('http'):
                job['url'] = 'https://www.linkedin.com' + job['url']
            
            # Date posted
            date_elem = self._find_element_by_patterns(card, ['time', 'span'], 
                                                     ['time', 'date', 'ago', 'posted'])
            job['date_posted'] = self._parse_date(date_elem.get_text()) if date_elem else ''
            
            # Job ID (extract from URL or generate)
            job['id'] = self._extract_job_id(job.get('url', ''))
            
            # Additional fields
            job['scraped_date'] = datetime.now().isoformat()
            job['source'] = 'linkedin'
            
            logger.debug(f"Extracted job: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}")
            return job
                
        except Exception as e:
            logger.error(f"Error extracting job from card: {str(e)}")
            return None
    
    def _find_element_by_patterns(self, parent, tag_names: List[str], 
                                 class_patterns: List[str]):
        """
        Find element by tag names and class patterns.
        
        Args:
            parent: Parent element to search in
            tag_names: List of tag names to search for
            class_patterns: List of class patterns to match
            
        Returns:
            Found element or None
        """
        for tag in tag_names:
            for pattern in class_patterns:
                elem = parent.find(tag, class_=lambda x: x and pattern in x.lower())
                if elem:
                    return elem
        return None
    
    def _get_job_details(self, job: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific job.
        
        Args:
            job: Basic job information dictionary
            
        Returns:
            Enhanced job dictionary with detailed information
        """
        if not job.get('url'):
            logger.warning("No URL provided for job details")
            return job
        
        try:
            logger.debug(f"Getting details for job: {job.get('title', 'Unknown')}")
            response = self._make_request(job['url'])
            
            if not response:
                logger.warning(f"Failed to get details for job: {job.get('title', 'Unknown')}")
                return job
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job description
            description_elem = self._find_element_by_patterns(soup, ['div', 'section'], 
                                                            ['description', 'details', 'content', 'job-details'])
            
            if description_elem:
                job['description'] = self._clean_text(description_elem.get_text())
            else:
                job['description'] = ''
            
            # Extract additional details
            additional_details = self._extract_additional_details(soup)
            job.update(additional_details)
            
            logger.debug(f"Successfully extracted details for job: {job.get('title', 'Unknown')}")
            return job
            
        except Exception as e:
            logger.error(f"Error getting job details for {job.get('url')}: {str(e)}")
            return job
    
    def _extract_additional_details(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract additional job details from the job page.
        
        Args:
            soup: BeautifulSoup object of the job page
            
        Returns:
            Dictionary containing additional job details
        """
        details = {}
        
        try:
            # Job type (Full-time, Part-time, etc.)
            job_type_patterns = [
                r'(Full-time|Part-time|Contract|Temporary|Internship)',
                r'(Full time|Part time)',
                r'(Permanent|Temporary)'
            ]
            
            for pattern in job_type_patterns:
                job_type_elem = soup.find(text=re.compile(pattern, re.IGNORECASE))
                if job_type_elem:
                    details['job_type'] = job_type_elem.strip()
                    break
            
            # Experience level
            exp_patterns = [
                r'(Entry level|Associate|Mid-Senior|Director|Executive)',
                r'(Junior|Senior|Lead|Principal)',
                r'(0-2 years|3-5 years|5\+ years)'
            ]
            
            for pattern in exp_patterns:
                exp_elem = soup.find(text=re.compile(pattern, re.IGNORECASE))
                if exp_elem:
                    details['experience_level'] = exp_elem.strip()
                    break
            
            # Salary information
            salary_patterns = [
                r'\$[\d,]+(?: - \$[\d,]+)?',
                r'[\d,]+(?: - [\d,]+)?\s*(?:k|K|thousand|per year|annually)',
                r'(?:salary|pay|compensation):\s*\$?[\d,]+(?: - \$?[\d,]+)?'
            ]
            
            for pattern in salary_patterns:
                salary_elem = soup.find(text=re.compile(pattern, re.IGNORECASE))
                if salary_elem:
                    details['salary'] = salary_elem.strip()
                    break
            
            # Skills/Technologies mentioned
            skills = self._extract_skills_from_text(soup.get_text())
            if skills:
                details['skills'] = skills
                
        except Exception as e:
            logger.error(f"Error extracting additional details: {str(e)}")
            
        return details
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """
        Extract skills and technologies from job description text.
        
        Args:
            text: Text to extract skills from
            
        Returns:
            List of found skills
        """
        # Comprehensive list of technical skills
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php',
            'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
            'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express',
            'django', 'flask', 'spring', 'asp.net', 'laravel', 'jquery',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
            'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        
        logger.debug(f"Extracted {len(found_skills)} skills: {found_skills}")
        return found_skills
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ''
        
        # Remove extra whitespace and newlines
        text = ' '.join(text.split())
        
        # Remove HTML entities
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&quot;', '"').replace('&#39;', "'")
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _parse_date(self, date_text: str) -> str:
        """
        Parse date from various formats.
        
        Args:
            date_text: Date text to parse
            
        Returns:
            Formatted date string
        """
        if not date_text:
            return datetime.now().strftime('%Y-%m-%d')
        
        date_text = date_text.lower().strip()
        
        try:
            if 'hour' in date_text or 'minute' in date_text or 'today' in date_text:
                return datetime.now().strftime('%Y-%m-%d')
            elif 'yesterday' in date_text:
                return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            elif 'day' in date_text:
                days_match = re.search(r'(\d+)', date_text)
                if days_match:
                    days = int(days_match.group(1))
                    date = datetime.now() - timedelta(days=days)
                    return date.strftime('%Y-%m-%d')
            elif 'week' in date_text:
                weeks_match = re.search(r'(\d+)', date_text)
                if weeks_match:
                    weeks = int(weeks_match.group(1))
                    date = datetime.now() - timedelta(weeks=weeks)
                    return date.strftime('%Y-%m-%d')
            elif 'month' in date_text:
                return (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {str(e)}")
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_job_id(self, url: str) -> str:
        """
        Extract job ID from LinkedIn URL.
        
        Args:
            url: LinkedIn job URL
            
        Returns:
            Job ID string
        """
        try:
            # LinkedIn job URLs contain job IDs
            match = re.search(r'jobs/view/(\d+)', url)
            if match:
                return match.group(1)
            
            # Fallback: generate ID from URL hash
            return hashlib.md5(url.encode()).hexdigest()[:8]
        except:
            # Final fallback: random ID
            return str(random.randint(100000, 999999))
    
    def _validate_job_data(self, job: Dict[str, Any]) -> bool:
        """
        Validate job data to ensure it meets minimum requirements.
        
        Args:
            job: Job data dictionary
            
        Returns:
            True if job data is valid, False otherwise
        """
        required_fields = ['title', 'company']
        
        for field in required_fields:
            if not job.get(field) or not job[field].strip():
                logger.debug(f"Job validation failed: missing {field}")
                return False
        
        # Additional validation
        if len(job.get('title', '')) > 200:
            logger.debug("Job validation failed: title too long")
            return False
        
        if len(job.get('company', '')) > 100:
            logger.debug("Job validation failed: company name too long")
            return False
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get scraping statistics.
        
        Returns:
            Dictionary containing scraping statistics
        """
        return self.stats.copy()
    
    def reset_statistics(self):
        """Reset scraping statistics."""
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'jobs_scraped': 0,
            'pages_scraped': 0
        }
        logger.info("Statistics reset")

# Usage example and testing
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    scraper = LinkedInJobScraper()
    
    config = {
        'job_title': 'Data Scientist',
        'location': 'San Francisco, CA',
        'max_pages': 2,
        'experience_level': 'Mid-Senior level',
        'job_type': 'Full-time'
    }
    
    try:
        jobs = scraper.scrape_jobs(config)
        print(f"Scraped {len(jobs)} jobs")
        
        # Print statistics
        stats = scraper.get_statistics()
        print(f"Scraping statistics: {stats}")
        
        # Save results
        with open('scraped_jobs.json', 'w') as f:
            json.dump(jobs, f, indent=2)
        print("Results saved to scraped_jobs.json")
        
    except ScrapingError as e:
        print(f"Scraping failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
