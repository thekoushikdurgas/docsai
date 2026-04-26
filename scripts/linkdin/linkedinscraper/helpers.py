"""
Utility Helper Functions
Contains various helper functions for data processing, formatting, and analysis.
"""

import re
import string
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Set up logging
logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text data"""
    if not text or not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def format_salary(salary_text: str) -> str:
    """Format and standardize salary information"""
    if not salary_text:
        return ""
    
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
            return f"${min_sal} - ${max_sal}"
        else:
            return f"${min_sal}"
    
    return salary_text

def extract_skills(text: str) -> List[str]:
    """Extract technical skills and technologies from text"""
    if not text:
        return []
    
    text = text.lower()
    
    # Comprehensive list of technical skills
    skill_patterns = {
        'programming_languages': [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 
            'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
            'perl', 'shell', 'bash', 'powershell'
        ],
        'web_technologies': [
            'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express',
            'django', 'flask', 'spring', 'asp.net', 'laravel', 'jquery',
            'bootstrap', 'sass', 'less', 'webpack', 'babel'
        ],
        'databases': [
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'cassandra', 'dynamodb', 'sqlite', 'oracle', 'sql server',
            'neo4j', 'couchdb', 'firebase'
        ],
        'cloud_platforms': [
            'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'digitalocean',
            'linode', 'vultr', 'cloudflare', 'vercel', 'netlify'
        ],
        'devops_tools': [
            'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
            'bitbucket', 'ansible', 'terraform', 'vagrant', 'chef', 'puppet',
            'circleci', 'travis ci', 'github actions'
        ],
        'data_science': [
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'jupyter', 'tableau', 'power bi', 'spark', 'hadoop', 'kafka',
            'airflow', 'dbt', 'snowflake'
        ],
        'mobile_development': [
            'ios', 'android', 'react native', 'flutter', 'xamarin',
            'cordova', 'phonegap', 'ionic'
        ],
        'methodologies': [
            'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd',
            'microservices', 'rest api', 'graphql', 'soap'
        ]
    }
    
    found_skills = []
    
    for category, skills in skill_patterns.items():
        for skill in skills:
            # Use word boundaries to avoid false positives
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(skill)
    
    # Remove duplicates and return
    return list(set(found_skills))

def extract_experience_level(text: str) -> str:
    """Extract experience level from job text"""
    if not text:
        return ""
    
    text = text.lower()
    
    experience_patterns = {
        'internship': ['intern', 'internship', 'trainee', 'graduate program'],
        'entry level': ['entry level', 'junior', 'associate', '0-2 years', 'new grad', 'recent graduate'],
        'mid level': ['mid level', 'mid-level', '3-5 years', '2-4 years', 'experienced'],
        'senior level': ['senior', 'sr.', '5+ years', '6+ years', 'lead', 'principal'],
        'executive': ['director', 'vp', 'vice president', 'cto', 'ceo', 'head of']
    }
    
    for level, patterns in experience_patterns.items():
        for pattern in patterns:
            if pattern in text:
                return level
    
    return ""

def extract_job_type(text: str) -> str:
    """Extract job type from job text"""
    if not text:
        return ""
    
    text = text.lower()
    
    job_type_patterns = {
        'full-time': ['full time', 'full-time', 'permanent', 'staff'],
        'part-time': ['part time', 'part-time'],
        'contract': ['contract', 'contractor', 'freelance', 'consulting'],
        'temporary': ['temporary', 'temp', 'interim'],
        'internship': ['intern', 'internship', 'co-op']
    }
    
    for job_type, patterns in job_type_patterns.items():
        for pattern in patterns:
            if pattern in text:
                return job_type
    
    return ""

def parse_location(location_text: str) -> Dict[str, str]:
    """Parse location text into components"""
    if not location_text:
        return {}
    
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
    
    return location_data

def calculate_days_since_posted(date_text: str) -> int:
    """Calculate days since job was posted"""
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
            for date_format in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%B %d, %Y']:
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

def normalize_company_name(company_name: str) -> str:
    """Normalize company names for consistency"""
    if not company_name:
        return ""
    
    company_name = company_name.strip()
    
    # Remove common suffixes
    suffixes = ['Inc.', 'LLC', 'Corp.', 'Corporation', 'Ltd.', 'Limited', 'Co.', 'Company']
    for suffix in suffixes:
        if company_name.endswith(suffix):
            company_name = company_name[:-len(suffix)].strip()
    
    return company_name

def extract_contact_info(text: str) -> Dict[str, Any]:
    """Extract contact information from text"""
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

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate text similarity using Jaccard similarity"""
    if not text1 or not text2:
        return 0.0
    
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
    
    return len(intersection) / len(union)

def generate_job_summary(job_data: Dict) -> str:
    """Generate a concise summary of a job posting"""
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
    
    return ' '.join(summary_parts)

def validate_job_data(job_data: Dict) -> Dict[str, Any]:
    """Validate and return validation results for job data"""
    validation_result = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
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
    
    # Validate company name
    company = job_data.get('company', '')
    if company and len(company) > 50:
        validation_result['warnings'].append("Company name is unusually long")
    
    # Validate description length
    description = job_data.get('description', '')
    if description and len(description) < 50:
        validation_result['warnings'].append("Job description is very short")
    
    # Validate URL format
    url = job_data.get('url', '')
    if url and not url.startswith(('http://', 'https://')):
        validation_result['warnings'].append("URL format appears invalid")
    
    return validation_result

def format_currency(amount: str, currency: str = 'USD') -> str:
    """Format currency amounts consistently"""
    if not amount:
        return ""
    
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

def create_job_hash(job_data: Dict) -> str:
    """Create a unique hash for a job posting to detect duplicates"""
    import hashlib
    
    # Use key fields to create hash
    hash_components = [
        job_data.get('title', '').lower().strip(),
        job_data.get('company', '').lower().strip(),
        job_data.get('location', '').lower().strip()
    ]
    
    # Create hash
    hash_string = '|'.join(hash_components)
    return hashlib.md5(hash_string.encode()).hexdigest()

def batch_process_jobs(jobs_data: List[Dict], processing_func, batch_size: int = 100) -> List[Any]:
    """Process jobs in batches for better performance"""
    results = []
    
    for i in range(0, len(jobs_data), batch_size):
        batch = jobs_data[i:i + batch_size]
        batch_results = [processing_func(job) for job in batch]
        results.extend(batch_results)
        
        logger.info(f"Processed batch {i//batch_size + 1}/{(len(jobs_data)-1)//batch_size + 1}")
    
    return results

def get_date_range_filter(days_back: int) -> str:
    """Get date string for filtering jobs within a certain time range"""
    cutoff_date = datetime.now() - timedelta(days=days_back)
    return cutoff_date.strftime('%Y-%m-%d')

def clean_html_tags(html_text: str) -> str:
    """Remove HTML tags from text"""
    if not html_text:
        return ""
    
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text()

def extract_years_of_experience(text: str) -> Optional[int]:
    """Extract years of experience requirement from job description"""
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
            return int(match.group(1))
    
    return None

# Export all functions
__all__ = [
    'clean_text',
    'format_salary', 
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