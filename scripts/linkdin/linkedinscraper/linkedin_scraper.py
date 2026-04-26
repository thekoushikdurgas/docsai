"""
LinkedIn Job Scraper Module
Handles the scraping of job postings from LinkedIn using BeautifulSoup and requests.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import re
from urllib.parse import urlencode, quote_plus
from datetime import datetime
import json
import logging

class LinkedInJobScraper:
    """LinkedIn job scraper with rate limiting and anti-detection measures"""
    
    def __init__(self):
        """Initialize the scraper with configuration"""
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.ua = UserAgent()
        self.session = requests.Session()
        self.delay_range = (2, 5)  # Random delay between requests
        self.max_retries = 3
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def get_headers(self):
        """Generate random headers to avoid detection"""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
    
    def build_search_url(self, job_title, location, start=0, filters=None):
        """Build LinkedIn job search URL with parameters"""
        params = {
            'keywords': job_title,
            'location': location,
            'start': start
        }
        
        # Add additional filters if provided
        if filters:
            if filters.get('job_type'):
                params['f_JT'] = filters['job_type']
            if filters.get('experience_level'):
                params['f_E'] = filters['experience_level']
            if filters.get('date_posted'):
                params['f_TPR'] = filters['date_posted']
        
        return f"{self.base_url}?{urlencode(params)}"
    
    def scrape_jobs(self, config):
        """Main method to scrape jobs based on configuration"""
        job_title = config.get('job_title', '')
        location = config.get('location', '')
        max_pages = config.get('max_pages', 3)
        
        all_jobs = []
        
        try:
            for page in range(max_pages):
                start = page * 25  # LinkedIn shows 25 jobs per page
                
                self.logger.info(f"Scraping page {page + 1} of {max_pages}")
                
                # Build search URL
                search_url = self.build_search_url(job_title, location, start)
                
                # Get job listings from this page
                page_jobs = self.scrape_page(search_url)
                
                if page_jobs:
                    all_jobs.extend(page_jobs)
                    
                    # Get detailed information for each job
                    detailed_jobs = []
                    for job in page_jobs:
                        detailed_job = self.get_job_details(job)
                        if detailed_job:
                            detailed_jobs.append(detailed_job)
                        
                        # Random delay to avoid rate limiting
                        time.sleep(random.uniform(*self.delay_range))
                    
                    all_jobs = detailed_jobs
                else:
                    self.logger.warning(f"No jobs found on page {page + 1}")
                
                # Delay between pages
                time.sleep(random.uniform(3, 7))
                
        except Exception as e:
            self.logger.error(f"Error during scraping: {str(e)}")
            
        return all_jobs
    
    def scrape_page(self, url):
        """Scrape a single page of job listings"""
        jobs = []
        
        try:
            response = self.session.get(url, headers=self.get_headers())
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards - LinkedIn uses various class names, these are common patterns
            job_cards = soup.find_all(['div', 'li'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['job', 'result', 'card', 'listing']
            ))
            
            for card in job_cards:
                job = self.extract_job_from_card(card)
                if job:
                    jobs.append(job)
                    
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error scraping page: {str(e)}")
            
        return jobs
    
    def extract_job_from_card(self, card):
        """Extract job information from a job card element"""
        try:
            job = {}
            
            # Job title
            title_elem = card.find(['h3', 'h2', 'a'], class_=lambda x: x and 'title' in x.lower())
            if not title_elem:
                title_elem = card.find('a')
            job['title'] = self.clean_text(title_elem.get_text()) if title_elem else ''
            
            # Company name
            company_elem = card.find(['span', 'div', 'a'], class_=lambda x: x and 'company' in x.lower())
            job['company'] = self.clean_text(company_elem.get_text()) if company_elem else ''
            
            # Location
            location_elem = card.find(['span', 'div'], class_=lambda x: x and 'location' in x.lower())
            job['location'] = self.clean_text(location_elem.get_text()) if location_elem else ''
            
            # Job URL
            link_elem = card.find('a', href=True)
            job['url'] = link_elem['href'] if link_elem else ''
            if job['url'] and not job['url'].startswith('http'):
                job['url'] = 'https://www.linkedin.com' + job['url']
            
            # Date posted
            date_elem = card.find(['time', 'span'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['time', 'date', 'ago']
            ))
            job['date_posted'] = self.parse_date(date_elem.get_text()) if date_elem else ''
            
            # Job ID (extract from URL or generate)
            job['id'] = self.extract_job_id(job.get('url', ''))
            
            # Only return job if we have minimum required information
            if job.get('title') and job.get('company'):
                return job
                
        except Exception as e:
            self.logger.error(f"Error extracting job from card: {str(e)}")
            
        return None
    
    def get_job_details(self, job):
        """Get detailed information for a specific job"""
        if not job.get('url'):
            return job
        
        try:
            response = self.session.get(job['url'], headers=self.get_headers())
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job description
            description_elem = soup.find(['div', 'section'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['description', 'details', 'content']
            ))
            
            if description_elem:
                job['description'] = self.clean_text(description_elem.get_text())
            else:
                job['description'] = ''
            
            # Extract additional details
            job.update(self.extract_additional_details(soup))
            
        except Exception as e:
            self.logger.error(f"Error getting job details for {job.get('url')}: {str(e)}")
            
        return job
    
    def extract_additional_details(self, soup):
        """Extract additional job details from the job page"""
        details = {}
        
        try:
            # Job type (Full-time, Part-time, etc.)
            job_type_elem = soup.find(text=re.compile(r'(Full-time|Part-time|Contract|Temporary)'))
            if job_type_elem:
                details['job_type'] = job_type_elem.strip()
            
            # Experience level
            exp_elem = soup.find(text=re.compile(r'(Entry level|Associate|Mid-Senior|Director|Executive)'))
            if exp_elem:
                details['experience_level'] = exp_elem.strip()
            
            # Salary information
            salary_elem = soup.find(text=re.compile(r'\\$[\\d,]+ - \\$[\\d,]+'))
            if salary_elem:
                details['salary'] = salary_elem.strip()
            
            # Skills/Technologies mentioned
            skills = self.extract_skills_from_text(soup.get_text())
            if skills:
                details['skills'] = skills
                
        except Exception as e:
            self.logger.error(f"Error extracting additional details: {str(e)}")
            
        return details
    
    def extract_skills_from_text(self, text):
        """Extract skills and technologies from job description text"""
        # Common skills to look for
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'git', 'jenkins', 'ci/cd', 'agile', 'scrum'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ''
        
        # Remove extra whitespace and newlines
        text = ' '.join(text.split())
        
        # Remove HTML entities
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        
        return text.strip()
    
    def parse_date(self, date_text):
        """Parse date from various formats"""
        if not date_text:
            return datetime.now().strftime('%Y-%m-%d')
        
        date_text = date_text.lower().strip()
        
        try:
            if 'hour' in date_text or 'minute' in date_text:
                return datetime.now().strftime('%Y-%m-%d')
            elif 'day' in date_text:
                days_match = re.search(r'(\\d+)', date_text)
                if days_match:
                    days = int(days_match.group(1))
                    date = datetime.now() - timedelta(days=days)
                    return date.strftime('%Y-%m-%d')
            elif 'week' in date_text:
                weeks_match = re.search(r'(\\d+)', date_text)
                if weeks_match:
                    weeks = int(weeks_match.group(1))
                    date = datetime.now() - timedelta(weeks=weeks)
                    return date.strftime('%Y-%m-%d')
            elif 'month' in date_text:
                return (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        except Exception as e:
            self.logger.error(f"Error parsing date '{date_text}': {str(e)}")
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def extract_job_id(self, url):
        """Extract job ID from LinkedIn URL"""
        try:
            # LinkedIn job URLs contain job IDs
            match = re.search(r'jobs/view/(\\d+)', url)
            if match:
                return match.group(1)
            
            # Fallback: generate ID from URL hash
            import hashlib
            return hashlib.md5(url.encode()).hexdigest()[:8]
        except:
            # Final fallback: random ID
            return str(random.randint(100000, 999999))

# Example usage and configuration
class ScraperConfig:
    """Configuration class for the LinkedIn scraper"""
    
    def __init__(self):
        self.delay_range = (2, 5)
        self.max_retries = 3
        self.max_pages = 5
        self.respect_robots_txt = True
        self.save_raw_html = False
        self.output_format = 'json'  # json, csv, database
    
    def get_search_filters(self, experience_level=None, job_type=None, date_posted=None):
        """Get search filters for LinkedIn"""
        filters = {}
        
        # Experience level mapping
        experience_map = {
            'Internship': '1',
            'Entry level': '2', 
            'Associate': '3',
            'Mid-Senior level': '4',
            'Director': '5',
            'Executive': '6'
        }
        
        # Job type mapping  
        job_type_map = {
            'Full-time': 'F',
            'Part-time': 'P',
            'Contract': 'C',
            'Temporary': 'T',
            'Internship': 'I'
        }
        
        # Date posted mapping
        date_map = {
            'Past 24 hours': 'r86400',
            'Past week': 'r604800',
            'Past month': 'r2592000'
        }
        
        if experience_level and experience_level in experience_map:
            filters['experience_level'] = experience_map[experience_level]
            
        if job_type and job_type in job_type_map:
            filters['job_type'] = job_type_map[job_type]
            
        if date_posted and date_posted in date_map:
            filters['date_posted'] = date_map[date_posted]
        
        return filters

# Error handling and retry logic
class ScrapingError(Exception):
    """Custom exception for scraping errors"""
    pass

def retry_on_failure(max_retries=3, delay=1):
    """Decorator for retrying failed operations"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                        continue
                    
            raise last_exception
        return wrapper
    return decorator

# Usage example
if __name__ == "__main__":
    # Example usage
    scraper = LinkedInJobScraper()
    
    config = {
        'job_title': 'Data Scientist',
        'location': 'San Francisco, CA',
        'max_pages': 3,
        'experience_level': 'Mid-Senior level',
        'job_type': 'Full-time'
    }
    
    jobs = scraper.scrape_jobs(config)
    print(f"Scraped {len(jobs)} jobs")
    
    # Save results
    with open('scraped_jobs.json', 'w') as f:
        json.dump(jobs, f, indent=2)