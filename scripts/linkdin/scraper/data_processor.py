"""
Data Processor Module
Handles data cleaning, processing, and validation for scraped job data.
Enhanced with comprehensive logging and error handling.
"""

import re
import string
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import hashlib
import json

# Set up logging
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Data processor for cleaning and validating scraped job data.
    Enhanced with comprehensive logging and error handling.
    """
    
    def __init__(self):
        """Initialize the data processor."""
        logger.info("Initializing DataProcessor")
        
        # Download required NLTK data
        self._setup_nltk()
        
        # Initialize processing statistics
        self.stats = {
            'jobs_processed': 0,
            'jobs_cleaned': 0,
            'jobs_validated': 0,
            'validation_errors': 0,
            'processing_errors': 0
        }
        
        # Common skill patterns for extraction
        self.skill_patterns = self._load_skill_patterns()
        
        logger.info("DataProcessor initialized successfully")
    
    def _setup_nltk(self):
        """Download required NLTK data."""
        try:
            # Download punkt tokenizer
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                logger.info("Downloading NLTK punkt tokenizer")
                nltk.download('punkt')
            
            # Download stopwords
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                logger.info("Downloading NLTK stopwords")
                nltk.download('stopwords')
                
        except Exception as e:
            logger.error(f"Error setting up NLTK: {str(e)}")
    
    def _load_skill_patterns(self) -> Dict[str, List[str]]:
        """Load comprehensive skill patterns for extraction."""
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php',
                'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
                'perl', 'shell', 'bash', 'powershell', 'dart', 'lua', 'clojure'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express',
                'django', 'flask', 'spring', 'asp.net', 'laravel', 'jquery',
                'bootstrap', 'sass', 'less', 'webpack', 'babel', 'next.js',
                'nuxt.js', 'ember', 'backbone', 'jsp', 'servlet'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'cassandra', 'dynamodb', 'sqlite', 'oracle', 'sql server',
                'neo4j', 'couchdb', 'firebase', 'mariadb', 'influxdb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'linode', 'vultr', 'cloudflare', 'vercel', 'netlify', 'ibm cloud',
                'oracle cloud', 'alibaba cloud'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
                'bitbucket', 'ansible', 'terraform', 'vagrant', 'chef', 'puppet',
                'circleci', 'travis ci', 'github actions', 'azure devops',
                'jira', 'confluence', 'slack', 'teams'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'tensorflow', 'pytorch',
                'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
                'jupyter', 'tableau', 'power bi', 'spark', 'hadoop', 'kafka',
                'airflow', 'dbt', 'snowflake', 'databricks', 'mlflow'
            ],
            'mobile_development': [
                'ios', 'android', 'react native', 'flutter', 'xamarin',
                'cordova', 'phonegap', 'ionic', 'swift', 'kotlin', 'objective-c'
            ],
            'methodologies': [
                'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd',
                'microservices', 'rest api', 'graphql', 'soap', 'api design',
                'test driven development', 'behavior driven development'
            ]
        }
    
    def process_jobs(self, jobs_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a list of job data.
        
        Args:
            jobs_data: List of raw job dictionaries
            
        Returns:
            List of processed job dictionaries
        """
        logger.info(f"Processing {len(jobs_data)} jobs")
        processed_jobs = []
        
        for i, job in enumerate(jobs_data):
            try:
                logger.debug(f"Processing job {i + 1}/{len(jobs_data)}: {job.get('title', 'Unknown')}")
                
                processed_job = self.process_single_job(job)
                if processed_job:
                    processed_jobs.append(processed_job)
                    self.stats['jobs_processed'] += 1
                    self.stats['jobs_cleaned'] += 1
                else:
                    logger.warning(f"Failed to process job {i + 1}")
                    self.stats['processing_errors'] += 1
                    
            except Exception as e:
                logger.error(f"Error processing job {i + 1}: {str(e)}")
                self.stats['processing_errors'] += 1
                continue
        
        logger.info(f"Successfully processed {len(processed_jobs)} out of {len(jobs_data)} jobs")
        return processed_jobs
    
    def process_single_job(self, job_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single job data dictionary.
        
        Args:
            job_data: Raw job data dictionary
            
        Returns:
            Processed job dictionary or None if processing fails
        """
        try:
            processed_job = {}
            
            # Basic fields
            processed_job['id'] = self._clean_id(job_data.get('id', ''))
            processed_job['title'] = self.clean_text(job_data.get('title', ''))
            processed_job['company'] = self.clean_text(job_data.get('company', ''))
            processed_job['location'] = self.clean_text(job_data.get('location', ''))
            processed_job['description'] = self.clean_text(job_data.get('description', ''))
            processed_job['url'] = self._clean_url(job_data.get('url', ''))
            
            # Date processing
            processed_job['date_posted'] = self._process_date(job_data.get('date_posted', ''))
            processed_job['scraped_date'] = job_data.get('scraped_date', datetime.now().isoformat())
            
            # Salary processing
            processed_job['salary'] = self.format_salary(job_data.get('salary', ''))
            
            # Job type and experience
            processed_job['job_type'] = self._extract_job_type(processed_job['description'])
            processed_job['experience_level'] = self._extract_experience_level(processed_job['description'])
            
            # Skills extraction
            processed_job['skills'] = self.extract_skills(processed_job['description'])
            
            # Additional processing
            processed_job['location_data'] = self.parse_location(processed_job['location'])
            processed_job['contact_info'] = self.extract_contact_info(processed_job['description'])
            processed_job['years_experience'] = self.extract_years_of_experience(processed_job['description'])
            
            # Generate job hash for duplicate detection
            processed_job['job_hash'] = self.create_job_hash(processed_job)
            
            # Validation
            if self.validate_job_data(processed_job):
                self.stats['jobs_validated'] += 1
                logger.debug(f"Successfully processed job: {processed_job['title']}")
                return processed_job
            else:
                self.stats['validation_errors'] += 1
                logger.warning(f"Job validation failed: {processed_job.get('title', 'Unknown')}")
                return None
                
        except Exception as e:
            logger.error(f"Error processing single job: {str(e)}")
            return None
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text data.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        logger.debug(f"Cleaning text of length: {len(text)}")
        
        # Remove HTML tags
        text = BeautifulSoup(text, "html.parser").get_text()
        
        # Remove extra whitespace and newlines
        text = ' '.join(text.split())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        logger.debug(f"Cleaned text length: {len(text)}")
        return text
    
    def format_salary(self, salary_text: str) -> str:
        """
        Format and standardize salary information.
        
        Args:
            salary_text: Raw salary text
            
        Returns:
            Formatted salary string
        """
        if not salary_text:
            return ""
        
        logger.debug(f"Formatting salary: {salary_text}")
        
        # Common salary formats to handle
        salary_text = salary_text.strip()
        
        # Remove currency symbols and common prefixes
        salary_text = re.sub(r'[£€¥₹]', '$', salary_text)  # Normalize currency symbols
        salary_text = re.sub(r'salary:?|pay:?|wage:?', '', salary_text, flags=re.IGNORECASE)
        
        # Extract salary ranges
        salary_match = re.search(r'\$?([\d,]+)(?:\s*-\s*\$?([\d,]+))?(?:\s*(k|thousand|per\s+year|annually|/yr|yr))?', 
                               salary_text, re.IGNORECASE)
        
        if salary_match:
            min_sal = salary_match.group(1).replace(',', '')
            max_sal = salary_match.group(2)
            unit = salary_match.group(3)
            
            # Handle thousands indicator
            if unit and ('k' in unit.lower() or 'thousand' in unit.lower()):
                min_sal = str(int(min_sal) * 1000)
                if max_sal:
                    max_sal = str(int(max_sal.replace(',', '')) * 1000)
            
            # Format output
            if max_sal:
                formatted = f"${min_sal} - ${max_sal}"
            else:
                formatted = f"${min_sal}"
            
            logger.debug(f"Formatted salary: {formatted}")
            return formatted
        
        return salary_text
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills and technologies from text.
        
        Args:
            text: Text to extract skills from
            
        Returns:
            List of found skills
        """
        if not text:
            return []
        
        logger.debug(f"Extracting skills from text of length: {len(text)}")
        
        text = text.lower()
        found_skills = []
        
        for category, skills in self.skill_patterns.items():
            for skill in skills:
                # Use word boundaries to avoid false positives
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    found_skills.append(skill)
        
        # Remove duplicates and return
        unique_skills = list(set(found_skills))
        logger.debug(f"Extracted {len(unique_skills)} unique skills: {unique_skills}")
        return unique_skills
    
    def _extract_job_type(self, text: str) -> str:
        """Extract job type from job text."""
        if not text:
            return ""
        
        text = text.lower()
        
        job_type_patterns = {
            'Full-time': ['full time', 'full-time', 'permanent', 'staff'],
            'Part-time': ['part time', 'part-time'],
            'Contract': ['contract', 'contractor', 'freelance', 'consulting'],
            'Temporary': ['temporary', 'temp', 'interim'],
            'Internship': ['intern', 'internship', 'co-op']
        }
        
        for job_type, patterns in job_type_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    return job_type
        
        return ""
    
    def _extract_experience_level(self, text: str) -> str:
        """Extract experience level from job text."""
        if not text:
            return ""
        
        text = text.lower()
        
        experience_patterns = {
            'Internship': ['intern', 'internship', 'trainee', 'graduate program'],
            'Entry level': ['entry level', 'junior', 'associate', '0-2 years', 'new grad', 'recent graduate'],
            'Mid level': ['mid level', 'mid-level', '3-5 years', '2-4 years', 'experienced'],
            'Senior level': ['senior', 'sr.', '5+ years', '6+ years', 'lead', 'principal'],
            'Executive': ['director', 'vp', 'vice president', 'cto', 'ceo', 'head of']
        }
        
        for level, patterns in experience_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    return level
        
        return ""
    
    def parse_location(self, location_text: str) -> Dict[str, str]:
        """
        Parse location text into components.
        
        Args:
            location_text: Location string to parse
            
        Returns:
            Dictionary with location components
        """
        if not location_text:
            return {}
        
        logger.debug(f"Parsing location: {location_text}")
        
        location_data = {}
        location_text = location_text.strip()
        
        # Handle "City, State" or "City, Country" format
        if ',' in location_text:
            parts = [part.strip() for part in location_text.split(',')]
            if len(parts) >= 2:
                location_data['city'] = parts[0]
                location_data['state_or_country'] = parts[1]
                if len(parts) > 2:
                    location_data['country'] = parts[2]
        else:
            location_data['city'] = location_text
        
        # Detect remote work
        remote_keywords = ['remote', 'work from home', 'wfh', 'distributed', 'anywhere']
        if any(keyword in location_text.lower() for keyword in remote_keywords):
            location_data['remote'] = True
        
        logger.debug(f"Parsed location data: {location_data}")
        return location_data
    
    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """
        Extract contact information from text.
        
        Args:
            text: Text to extract contact info from
            
        Returns:
            Dictionary containing contact information
        """
        contact_info = {}
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['emails'] = emails
        
        # Phone number extraction (US format)
        phone_pattern = r'\b(?:\+1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phones'] = ['-'.join(phone) for phone in phones]
        
        # URL extraction
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        urls = re.findall(url_pattern, text)
        if urls:
            contact_info['urls'] = urls
        
        return contact_info
    
    def extract_years_of_experience(self, text: str) -> Optional[int]:
        """
        Extract years of experience requirement from job description.
        
        Args:
            text: Job description text
            
        Returns:
            Years of experience or None if not found
        """
        if not text:
            return None
        
        text = text.lower()
        
        # Look for patterns like "3+ years", "5-7 years", "minimum 2 years"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s+)?experience',
            r'minimum\s+(\d+)\s*years?',
            r'at\s+least\s+(\d+)\s*years?',
            r'(\d+)-\d+\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                years = int(match.group(1))
                logger.debug(f"Extracted years of experience: {years}")
                return years
        
        return None
    
    def _process_date(self, date_text: str) -> str:
        """Process and standardize date format."""
        if not date_text:
            return datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Handle relative dates
            date_text = date_text.lower().strip()
            
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
            
            # Handle actual dates
            for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%B %d, %Y']:
                try:
                    posted_date = datetime.strptime(date_text, date_format)
                    return posted_date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {str(e)}")
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def _clean_id(self, job_id: str) -> str:
        """Clean and validate job ID."""
        if not job_id:
            return hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        return str(job_id).strip()
    
    def _clean_url(self, url: str) -> str:
        """Clean and validate URL."""
        if not url:
            return ""
        
        url = url.strip()
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://www.linkedin.com' + url
        
        return url
    
    def validate_job_data(self, job_data: Dict[str, Any]) -> bool:
        """
        Validate job data to ensure it meets quality standards.
        
        Args:
            job_data: Job data dictionary to validate
            
        Returns:
            True if job data is valid, False otherwise
        """
        try:
            # Required fields
            required_fields = ['title', 'company']
            for field in required_fields:
                if not job_data.get(field) or not str(job_data[field]).strip():
                    logger.debug(f"Validation failed: missing {field}")
                    return False
            
            # Validate job title length
            title = job_data.get('title', '')
            if title and len(title) > 200:
                logger.debug("Validation failed: title too long")
                return False
            
            # Validate company name
            company = job_data.get('company', '')
            if company and len(company) > 100:
                logger.debug("Validation failed: company name too long")
                return False
            
            # Validate description length
            description = job_data.get('description', '')
            if description and len(description) < 50:
                logger.debug("Validation failed: description too short")
                return False
            
            # Validate URL format
            url = job_data.get('url', '')
            if url and not url.startswith(('http://', 'https://')):
                logger.debug("Validation failed: invalid URL format")
                return False
            
            logger.debug("Job data validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Error validating job data: {str(e)}")
            return False
    
    def create_job_hash(self, job_data: Dict[str, Any]) -> str:
        """
        Create a unique hash for a job posting to detect duplicates.
        
        Args:
            job_data: Job data dictionary
            
        Returns:
            MD5 hash string
        """
        # Use key fields to create hash
        hash_components = [
            job_data.get('title', '').lower().strip(),
            job_data.get('company', '').lower().strip(),
            job_data.get('location', '').lower().strip()
        ]
        
        # Create hash
        hash_string = '|'.join(hash_components)
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate text similarity using Jaccard similarity.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        if not text1 or not text2:
            return 0.0
        
        try:
            # Tokenize and convert to lowercase
            tokens1 = set(word_tokenize(text1.lower()))
            tokens2 = set(word_tokenize(text2.lower()))
            
            # Remove stopwords
            stop_words = set(stopwords.words('english'))
            tokens1 = {word for word in tokens1 if word not in stop_words and word.isalpha()}
            tokens2 = {word for word in tokens2 if word not in stop_words and word.isalpha()}
            
            # Calculate Jaccard similarity
            intersection = tokens1.intersection(tokens2)
            union = tokens1.union(tokens2)
            
            if not union:
                return 0.0
            
            similarity = len(intersection) / len(union)
            logger.debug(f"Text similarity: {similarity:.3f}")
            return similarity
            
        except Exception as e:
            logger.error(f"Error calculating text similarity: {str(e)}")
            return 0.0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dictionary containing processing statistics
        """
        return self.stats.copy()
    
    def reset_statistics(self):
        """Reset processing statistics."""
        self.stats = {
            'jobs_processed': 0,
            'jobs_cleaned': 0,
            'jobs_validated': 0,
            'validation_errors': 0,
            'processing_errors': 0
        }
        logger.info("Processing statistics reset")

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    processor = DataProcessor()
    
    # Sample job data
    sample_job = {
        'id': 'job_001',
        'title': 'Senior Data Scientist',
        'company': 'TechCorp Inc.',
        'location': 'San Francisco, CA',
        'description': 'Looking for an experienced data scientist with Python and machine learning skills. Must have 5+ years of experience.',
        'salary': '$120,000 - $150,000 per year',
        'date_posted': '2 days ago',
        'url': 'https://linkedin.com/jobs/view/123456'
    }
    
    # Process the job
    processed_job = processor.process_single_job(sample_job)
    
    if processed_job:
        print("Processed job:")
        print(json.dumps(processed_job, indent=2))
        
        # Print statistics
        stats = processor.get_statistics()
        print(f"\nProcessing statistics: {stats}")
    else:
        print("Failed to process job")
