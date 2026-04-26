"""
Utility Helper Functions
Contains various helper functions for data processing, formatting, and analysis.
Enhanced with comprehensive logging and improved functionality.
"""

import re
import string
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union, Tuple
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import hashlib
import json
import unicodedata
from dataclasses import dataclass
from enum import Enum

# Set up logging
logger = logging.getLogger(__name__)

class TextProcessingLevel(Enum):
    """Enum for text processing levels"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"

@dataclass
class ProcessingStats:
    """Statistics for text processing operations"""
    texts_processed: int = 0
    characters_processed: int = 0
    html_tags_removed: int = 0
    special_chars_removed: int = 0
    duplicates_found: int = 0
    processing_errors: int = 0

class TextProcessor:
    """
    Advanced text processing utility with comprehensive logging and statistics.
    """
    
    def __init__(self, processing_level: TextProcessingLevel = TextProcessingLevel.STANDARD):
        """
        Initialize the text processor.
        
        Args:
            processing_level: Level of text processing to apply
        """
        self.processing_level = processing_level
        self.stats = ProcessingStats()
        
        # Download required NLTK data
        self._setup_nltk()
        
        # Initialize stopwords
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            logger.warning("NLTK stopwords not available")
            self.stop_words = set()
        
        logger.info(f"TextProcessor initialized with level: {processing_level.value}")
    
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
    
    def clean_text(self, text: str, remove_html: bool = True, 
                   normalize_unicode: bool = True) -> str:
        """
        Clean and normalize text data with comprehensive processing.
        
        Args:
            text: Text to clean
            remove_html: Whether to remove HTML tags
            normalize_unicode: Whether to normalize Unicode characters
            
        Returns:
            Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        original_length = len(text)
        self.stats.texts_processed += 1
        self.stats.characters_processed += original_length
        
        try:
            logger.debug(f"Cleaning text of length: {original_length}")
            
            # Remove HTML tags
            if remove_html:
                text = self._remove_html_tags(text)
            
            # Normalize Unicode
            if normalize_unicode:
                text = self._normalize_unicode(text)
            
            # Remove extra whitespace and newlines
            text = ' '.join(text.split())
            
            # Remove special characters based on processing level
            if self.processing_level == TextProcessingLevel.BASIC:
                text = self._basic_cleaning(text)
            elif self.processing_level == TextProcessingLevel.STANDARD:
                text = self._standard_cleaning(text)
            elif self.processing_level == TextProcessingLevel.ADVANCED:
                text = self._advanced_cleaning(text)
            
            # Remove multiple spaces
            text = re.sub(r'\s+', ' ', text)
            
            # Remove leading/trailing whitespace
            text = text.strip()
            
            logger.debug(f"Cleaned text length: {len(text)} (removed {original_length - len(text)} chars)")
            return text
            
        except Exception as e:
            logger.error(f"Error cleaning text: {str(e)}")
            self.stats.processing_errors += 1
            return text
    
    def _remove_html_tags(self, text: str) -> str:
        """Remove HTML tags from text."""
        try:
            soup = BeautifulSoup(text, "html.parser")
            cleaned_text = soup.get_text()
            self.stats.html_tags_removed += 1
            return cleaned_text
        except Exception as e:
            logger.error(f"Error removing HTML tags: {str(e)}")
            return text
    
    def _normalize_unicode(self, text: str) -> str:
        """Normalize Unicode characters."""
        try:
            # Normalize Unicode characters
            text = unicodedata.normalize('NFKD', text)
            return text
        except Exception as e:
            logger.error(f"Error normalizing Unicode: {str(e)}")
            return text
    
    def _basic_cleaning(self, text: str) -> str:
        """Basic text cleaning."""
        # Remove basic special characters
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        return text
    
    def _standard_cleaning(self, text: str) -> str:
        """Standard text cleaning."""
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        
        # Remove extra punctuation
        text = re.sub(r'[.]{2,}', '.', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        return text
    
    def _advanced_cleaning(self, text: str) -> str:
        """Advanced text cleaning."""
        # Standard cleaning first
        text = self._standard_cleaning(text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        
        # Remove phone numbers
        text = re.sub(r'\b(?:\+1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def extract_skills(self, text: str, custom_skills: Optional[List[str]] = None) -> List[str]:
        """
        Extract technical skills and technologies from text.
        
        Args:
            text: Text to extract skills from
            custom_skills: Additional custom skills to look for
            
        Returns:
            List of found skills
        """
        if not text:
            return []
        
        logger.debug(f"Extracting skills from text of length: {len(text)}")
        
        text = text.lower()
        found_skills = []
        
        # Get skill patterns
        skill_patterns = self._get_skill_patterns()
        
        # Add custom skills if provided
        if custom_skills:
            skill_patterns['custom'] = [skill.lower() for skill in custom_skills]
        
        for category, skills in skill_patterns.items():
            for skill in skills:
                # Use word boundaries to avoid false positives
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    found_skills.append(skill)
        
        # Remove duplicates and return
        unique_skills = list(set(found_skills))
        logger.debug(f"Extracted {len(unique_skills)} unique skills: {unique_skills}")
        return unique_skills
    
    def _get_skill_patterns(self) -> Dict[str, List[str]]:
        """Get comprehensive skill patterns for extraction."""
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php',
                'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
                'perl', 'shell', 'bash', 'powershell', 'dart', 'lua', 'clojure',
                'haskell', 'erlang', 'elixir', 'f#', 'ocaml', 'prolog'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express',
                'django', 'flask', 'spring', 'asp.net', 'laravel', 'jquery',
                'bootstrap', 'sass', 'less', 'webpack', 'babel', 'next.js',
                'nuxt.js', 'ember', 'backbone', 'jsp', 'servlet', 'jsf',
                'thymeleaf', 'handlebars', 'mustache', 'ejs'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'cassandra', 'dynamodb', 'sqlite', 'oracle', 'sql server',
                'neo4j', 'couchdb', 'firebase', 'mariadb', 'influxdb',
                'couchbase', 'riak', 'hbase', 'bigtable'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
                'linode', 'vultr', 'cloudflare', 'vercel', 'netlify', 'ibm cloud',
                'oracle cloud', 'alibaba cloud', 'salesforce', 'snowflake'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
                'bitbucket', 'ansible', 'terraform', 'vagrant', 'chef', 'puppet',
                'circleci', 'travis ci', 'github actions', 'azure devops',
                'jira', 'confluence', 'slack', 'teams', 'datadog', 'newrelic',
                'splunk', 'grafana', 'prometheus', 'elk stack'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'tensorflow', 'pytorch',
                'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
                'jupyter', 'tableau', 'power bi', 'spark', 'hadoop', 'kafka',
                'airflow', 'dbt', 'snowflake', 'databricks', 'mlflow',
                'xgboost', 'lightgbm', 'catboost', 'h2o', 'rapids'
            ],
            'mobile_development': [
                'ios', 'android', 'react native', 'flutter', 'xamarin',
                'cordova', 'phonegap', 'ionic', 'swift', 'kotlin', 'objective-c',
                'java', 'dart', 'c#', 'xamarin forms', 'unity'
            ],
            'methodologies': [
                'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd',
                'microservices', 'rest api', 'graphql', 'soap', 'api design',
                'test driven development', 'behavior driven development',
                'domain driven design', 'clean architecture', 'solid principles'
            ],
            'testing': [
                'unit testing', 'integration testing', 'end-to-end testing',
                'junit', 'pytest', 'jest', 'mocha', 'chai', 'cypress',
                'selenium', 'playwright', 'testcafe', 'karma', 'jasmine'
            ],
            'security': [
                'oauth', 'jwt', 'ssl', 'tls', 'encryption', 'authentication',
                'authorization', 'penetration testing', 'vulnerability assessment',
                'owasp', 'security scanning', 'code review', 'static analysis'
            ]
        }
    
    def extract_experience_level(self, text: str) -> str:
        """
        Extract experience level from job text.
        
        Args:
            text: Job text to analyze
            
        Returns:
            Experience level string
        """
        if not text:
            return ""
        
        text = text.lower()
        
        experience_patterns = {
            'Internship': ['intern', 'internship', 'trainee', 'graduate program', 'co-op'],
            'Entry level': ['entry level', 'junior', 'associate', '0-2 years', 'new grad', 
                           'recent graduate', 'fresh graduate', 'entry-level'],
            'Mid level': ['mid level', 'mid-level', '3-5 years', '2-4 years', 'experienced',
                         'intermediate', 'mid-senior'],
            'Senior level': ['senior', 'sr.', '5+ years', '6+ years', 'lead', 'principal',
                            'staff', 'senior level', 'expert'],
            'Executive': ['director', 'vp', 'vice president', 'cto', 'ceo', 'head of',
                         'executive', 'c-level', 'management']
        }
        
        for level, patterns in experience_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    logger.debug(f"Found experience level: {level}")
                    return level
        
        return ""
    
    def extract_job_type(self, text: str) -> str:
        """
        Extract job type from job text.
        
        Args:
            text: Job text to analyze
            
        Returns:
            Job type string
        """
        if not text:
            return ""
        
        text = text.lower()
        
        job_type_patterns = {
            'Full-time': ['full time', 'full-time', 'permanent', 'staff', 'regular'],
            'Part-time': ['part time', 'part-time', 'parttime'],
            'Contract': ['contract', 'contractor', 'freelance', 'consulting', 'consultant'],
            'Temporary': ['temporary', 'temp', 'interim', 'seasonal'],
            'Internship': ['intern', 'internship', 'co-op', 'coop', 'trainee']
        }
        
        for job_type, patterns in job_type_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    logger.debug(f"Found job type: {job_type}")
                    return job_type
        
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
        remote_keywords = ['remote', 'work from home', 'wfh', 'distributed', 'anywhere', 'virtual']
        if any(keyword in location_text.lower() for keyword in remote_keywords):
            location_data['remote'] = True
        
        # Detect hybrid work
        hybrid_keywords = ['hybrid', 'flexible', 'partial remote']
        if any(keyword in location_text.lower() for keyword in hybrid_keywords):
            location_data['hybrid'] = True
        
        logger.debug(f"Parsed location data: {location_data}")
        return location_data
    
    def calculate_days_since_posted(self, date_text: str) -> int:
        """
        Calculate days since job was posted.
        
        Args:
            date_text: Date text to parse
            
        Returns:
            Number of days since posted
        """
        if not date_text:
            return 0
        
        try:
            # Handle relative dates (e.g., "2 days ago", "1 week ago")
            date_text = date_text.lower().strip()
            
            if 'hour' in date_text or 'minute' in date_text or 'today' in date_text:
                return 0
            elif 'yesterday' in date_text:
                return 1
            elif 'day' in date_text:
                days_match = re.search(r'(\d+)', date_text)
                if days_match:
                    return int(days_match.group(1))
            elif 'week' in date_text:
                weeks_match = re.search(r'(\d+)', date_text)
                if weeks_match:
                    return int(weeks_match.group(1)) * 7
            elif 'month' in date_text:
                months_match = re.search(r'(\d+)', date_text)
                if months_match:
                    return int(months_match.group(1)) * 30
            
            # Handle actual dates
            try:
                # Try common date formats
                for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%B %d, %Y', '%b %d, %Y']:
                    try:
                        posted_date = datetime.strptime(date_text, date_format)
                        days_diff = (datetime.now() - posted_date).days
                        return max(0, days_diff)
                    except ValueError:
                        continue
            except:
                pass
        
        except Exception as e:
            logger.error(f"Error parsing date '{date_text}': {str(e)}")
        
        return 0
    
    def normalize_company_name(self, company_name: str) -> str:
        """
        Normalize company names for consistency.
        
        Args:
            company_name: Company name to normalize
            
        Returns:
            Normalized company name
        """
        if not company_name:
            return ""
        
        company_name = company_name.strip()
        
        # Remove common suffixes
        suffixes = ['Inc.', 'LLC', 'Corp.', 'Corporation', 'Ltd.', 'Limited', 'Co.', 'Company',
                   'Inc', 'LLC.', 'Corp', 'Ltd', 'Co', 'GmbH', 'AG', 'SA', 'S.A.', 'S.L.',
                   'Ltd.', 'Limited', 'Pvt.', 'Private', 'Limited']
        
        for suffix in suffixes:
            if company_name.endswith(suffix):
                company_name = company_name[:-len(suffix)].strip()
        
        # Remove extra whitespace
        company_name = ' '.join(company_name.split())
        
        logger.debug(f"Normalized company name: {company_name}")
        return company_name
    
    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """
        Extract contact information from text.
        
        Args:
            text: Text to extract contact info from
            
        Returns:
            Dictionary containing contact information
        """
        contact_info = {}
        
        try:
            # Email extraction
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            if emails:
                contact_info['emails'] = list(set(emails))  # Remove duplicates
            
            # Phone number extraction (multiple formats)
            phone_patterns = [
                r'\b(?:\+1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',  # US format
                r'\b(?:\+44[-.\s]?)?\(?([0-9]{4})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{3})\b',  # UK format
                r'\b(?:\+91[-.\s]?)?\(?([0-9]{5})\)?[-.\s]?([0-9]{5})\b'  # Indian format
            ]
            
            phones = []
            for pattern in phone_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if isinstance(match, tuple):
                        phone = '-'.join(match)
                    else:
                        phone = match
                    phones.append(phone)
            
            if phones:
                contact_info['phones'] = list(set(phones))  # Remove duplicates
            
            # URL extraction
            url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
            urls = re.findall(url_pattern, text)
            if urls:
                contact_info['urls'] = list(set(urls))  # Remove duplicates
            
            logger.debug(f"Extracted contact info: {len(contact_info.get('emails', []))} emails, "
                        f"{len(contact_info.get('phones', []))} phones, {len(contact_info.get('urls', []))} urls")
            
        except Exception as e:
            logger.error(f"Error extracting contact info: {str(e)}")
        
        return contact_info
    
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
            tokens1 = {word for word in tokens1 if word not in self.stop_words and word.isalpha()}
            tokens2 = {word for word in tokens2 if word not in self.stop_words and word.isalpha()}
            
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
    
    def generate_job_summary(self, job_data: Dict) -> str:
        """
        Generate a concise summary of a job posting.
        
        Args:
            job_data: Job data dictionary
            
        Returns:
            Job summary string
        """
        try:
            title = job_data.get('title', 'Unknown Position')
            company = job_data.get('company', 'Unknown Company')
            location = job_data.get('location', 'Unknown Location')
            
            summary_parts = [f"{title} at {company}"]
            
            if location:
                summary_parts.append(f"in {location}")
            
            job_type = job_data.get('job_type', '')
            experience_level = job_data.get('experience_level', '')
            
            if job_type or experience_level:
                details = []
                if job_type:
                    details.append(job_type)
                if experience_level:
                    details.append(experience_level)
                summary_parts.append(f"({', '.join(details)})")
            
            skills = job_data.get('skills', [])
            if skills:
                top_skills = skills[:3]  # Show top 3 skills
                summary_parts.append(f"Skills: {', '.join(top_skills)}")
            
            summary = ' '.join(summary_parts)
            logger.debug(f"Generated job summary: {summary}")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating job summary: {str(e)}")
            return "Job summary unavailable"
    
    def validate_job_data(self, job_data: Dict) -> Dict[str, Any]:
        """
        Validate and return validation results for job data.
        
        Args:
            job_data: Job data dictionary to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'score': 0
        }
        
        try:
            # Required fields
            required_fields = ['title', 'company']
            for field in required_fields:
                if not job_data.get(field):
                    validation_result['errors'].append(f"Missing required field: {field}")
                    validation_result['is_valid'] = False
            
            # Validate job title length
            title = job_data.get('title', '')
            if title and len(title) > 100:
                validation_result['warnings'].append("Job title is unusually long")
            elif title and len(title) < 5:
                validation_result['warnings'].append("Job title is unusually short")
            
            # Validate company name
            company = job_data.get('company', '')
            if company and len(company) > 50:
                validation_result['warnings'].append("Company name is unusually long")
            elif company and len(company) < 2:
                validation_result['warnings'].append("Company name is unusually short")
            
            # Validate description length
            description = job_data.get('description', '')
            if description and len(description) < 50:
                validation_result['warnings'].append("Job description is very short")
            elif description and len(description) > 10000:
                validation_result['warnings'].append("Job description is very long")
            
            # Validate URL format
            url = job_data.get('url', '')
            if url and not url.startswith(('http://', 'https://')):
                validation_result['warnings'].append("URL format appears invalid")
            
            # Calculate validation score
            score = 100
            score -= len(validation_result['errors']) * 20
            score -= len(validation_result['warnings']) * 5
            validation_result['score'] = max(0, score)
            
            logger.debug(f"Job validation completed: {validation_result['score']}/100")
            
        except Exception as e:
            logger.error(f"Error validating job data: {str(e)}")
            validation_result['errors'].append(f"Validation error: {str(e)}")
            validation_result['is_valid'] = False
        
        return validation_result
    
    def format_currency(self, amount: str, currency: str = 'USD') -> str:
        """
        Format currency amounts consistently.
        
        Args:
            amount: Currency amount string
            currency: Currency code
            
        Returns:
            Formatted currency string
        """
        if not amount:
            return ""
        
        try:
            # Extract numeric values
            numbers = re.findall(r'[\d,]+', str(amount))
            if not numbers:
                return amount
            
            # Format each number
            formatted_numbers = []
            for num in numbers:
                clean_num = num.replace(',', '')
                if clean_num.isdigit():
                    formatted_num = f"{int(clean_num):,}"
                    formatted_numbers.append(formatted_num)
            
            if len(formatted_numbers) == 1:
                return f"${formatted_numbers[0]}"
            elif len(formatted_numbers) == 2:
                return f"${formatted_numbers[0]} - ${formatted_numbers[1]}"
            else:
                return amount
                
        except Exception as e:
            logger.error(f"Error formatting currency: {str(e)}")
            return amount
    
    def create_job_hash(self, job_data: Dict) -> str:
        """
        Create a unique hash for a job posting to detect duplicates.
        
        Args:
            job_data: Job data dictionary
            
        Returns:
            MD5 hash string
        """
        try:
            # Use key fields to create hash
            hash_components = [
                job_data.get('title', '').lower().strip(),
                job_data.get('company', '').lower().strip(),
                job_data.get('location', '').lower().strip()
            ]
            
            # Create hash
            hash_string = '|'.join(hash_components)
            job_hash = hashlib.md5(hash_string.encode()).hexdigest()
            
            logger.debug(f"Generated job hash: {job_hash}")
            return job_hash
            
        except Exception as e:
            logger.error(f"Error creating job hash: {str(e)}")
            return hashlib.md5(str(datetime.now()).encode()).hexdigest()
    
    def batch_process_jobs(self, jobs_data: List[Dict], processing_func, 
                          batch_size: int = 100) -> List[Any]:
        """
        Process jobs in batches for better performance.
        
        Args:
            jobs_data: List of job data dictionaries
            processing_func: Function to process each job
            batch_size: Size of each batch
            
        Returns:
            List of processed results
        """
        results = []
        
        try:
            logger.info(f"Processing {len(jobs_data)} jobs in batches of {batch_size}")
            
            for i in range(0, len(jobs_data), batch_size):
                batch = jobs_data[i:i + batch_size]
                batch_results = [processing_func(job) for job in batch]
                results.extend(batch_results)
                
                logger.info(f"Processed batch {i//batch_size + 1}/{(len(jobs_data)-1)//batch_size + 1}")
            
            logger.info(f"Batch processing completed: {len(results)} results")
            
        except Exception as e:
            logger.error(f"Error in batch processing: {str(e)}")
        
        return results
    
    def get_date_range_filter(self, days_back: int) -> str:
        """
        Get date string for filtering jobs within a certain time range.
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            Date string in YYYY-MM-DD format
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        return cutoff_date.strftime('%Y-%m-%d')
    
    def clean_html_tags(self, html_text: str) -> str:
        """
        Remove HTML tags from text.
        
        Args:
            html_text: HTML text to clean
            
        Returns:
            Clean text without HTML tags
        """
        if not html_text:
            return ""
        
        try:
            soup = BeautifulSoup(html_text, "html.parser")
            return soup.get_text()
        except Exception as e:
            logger.error(f"Error cleaning HTML tags: {str(e)}")
            return html_text
    
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
            r'(\d+)-\d+\s*years?',
            r'(\d+)\s*to\s*\d+\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                years = int(match.group(1))
                logger.debug(f"Extracted years of experience: {years}")
                return years
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dictionary containing processing statistics
        """
        return {
            'texts_processed': self.stats.texts_processed,
            'characters_processed': self.stats.characters_processed,
            'html_tags_removed': self.stats.html_tags_removed,
            'special_chars_removed': self.stats.special_chars_removed,
            'duplicates_found': self.stats.duplicates_found,
            'processing_errors': self.stats.processing_errors,
            'processing_level': self.processing_level.value
        }
    
    def reset_statistics(self):
        """Reset processing statistics."""
        self.stats = ProcessingStats()
        logger.info("Processing statistics reset")

# Legacy functions for backward compatibility
def clean_text(text: str) -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.clean_text(text)

def extract_skills(text: str) -> List[str]:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.extract_skills(text)

def extract_experience_level(text: str) -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.extract_experience_level(text)

def extract_job_type(text: str) -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.extract_job_type(text)

def parse_location(location_text: str) -> Dict[str, str]:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.parse_location(location_text)

def calculate_days_since_posted(date_text: str) -> int:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.calculate_days_since_posted(date_text)

def normalize_company_name(company_name: str) -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.normalize_company_name(company_name)

def extract_contact_info(text: str) -> Dict[str, Any]:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.extract_contact_info(text)

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.calculate_text_similarity(text1, text2)

def generate_job_summary(job_data: Dict) -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.generate_job_summary(job_data)

def validate_job_data(job_data: Dict) -> Dict[str, Any]:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.validate_job_data(job_data)

def format_currency(amount: str, currency: str = 'USD') -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.format_currency(amount, currency)

def create_job_hash(job_data: Dict) -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.create_job_hash(job_data)

def batch_process_jobs(jobs_data: List[Dict], processing_func, batch_size: int = 100) -> List[Any]:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.batch_process_jobs(jobs_data, processing_func, batch_size)

def get_date_range_filter(days_back: int) -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.get_date_range_filter(days_back)

def clean_html_tags(html_text: str) -> str:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.clean_html_tags(html_text)

def extract_years_of_experience(text: str) -> Optional[int]:
    """Legacy function for backward compatibility."""
    processor = TextProcessor()
    return processor.extract_years_of_experience(text)

# Export all functions
__all__ = [
    'TextProcessor',
    'TextProcessingLevel',
    'ProcessingStats',
    'clean_text',
    'extract_skills',
    'extract_experience_level',
    'extract_job_type',
    'parse_location',
    'calculate_days_since_posted',
    'normalize_company_name',
    'extract_contact_info',
    'calculate_text_similarity',
    'generate_job_summary',
    'validate_job_data',
    'format_currency',
    'create_job_hash',
    'batch_process_jobs',
    'get_date_range_filter',
    'clean_html_tags',
    'extract_years_of_experience'
]

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    processor = TextProcessor(TextProcessingLevel.ADVANCED)
    
    # Sample job data
    sample_job = {
        'title': 'Senior Data Scientist',
        'company': 'TechCorp Inc.',
        'location': 'San Francisco, CA',
        'description': 'Looking for an experienced data scientist with Python and machine learning skills. Contact us at jobs@techcorp.com or call (555) 123-4567.',
        'salary': '$120,000 - $150,000 per year',
        'date_posted': '2 days ago'
    }
    
    # Process the job
    cleaned_description = processor.clean_text(sample_job['description'])
    skills = processor.extract_skills(cleaned_description)
    experience_level = processor.extract_experience_level(cleaned_description)
    contact_info = processor.extract_contact_info(cleaned_description)
    
    print(f"Cleaned description: {cleaned_description[:100]}...")
    print(f"Skills: {skills}")
    print(f"Experience level: {experience_level}")
    print(f"Contact info: {contact_info}")
    
    # Generate summary
    summary = processor.generate_job_summary(sample_job)
    print(f"Job summary: {summary}")
    
    # Validate job data
    validation = processor.validate_job_data(sample_job)
    print(f"Validation result: {validation}")
    
    # Get statistics
    stats = processor.get_statistics()
    print(f"Processing statistics: {stats}")
