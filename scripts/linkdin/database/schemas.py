"""
Data Schemas and Models
Defines data structures and validation schemas for job postings and search operations.
Enhanced with comprehensive validation and type hints.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
from enum import Enum
import re
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

class JobType(Enum):
    """Enum for job types"""
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    TEMPORARY = "Temporary"
    INTERNSHIP = "Internship"

class ExperienceLevel(Enum):
    """Enum for experience levels"""
    INTERNSHIP = "Internship"
    ENTRY_LEVEL = "Entry level"
    MID_LEVEL = "Mid level"
    SENIOR_LEVEL = "Senior level"
    EXECUTIVE = "Executive"

class JobStatus(Enum):
    """Enum for job status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    FILLED = "filled"

@dataclass
class LocationData:
    """Location data structure"""
    city: str = ""
    state_or_country: str = ""
    country: str = ""
    remote: bool = False
    coordinates: Optional[Dict[str, float]] = None
    
    def __post_init__(self):
        """Validate location data after initialization."""
        if not self.city and not self.state_or_country:
            logger.warning("Location data is empty")
    
    def to_string(self) -> str:
        """Convert location data to string representation."""
        parts = []
        if self.city:
            parts.append(self.city)
        if self.state_or_country:
            parts.append(self.state_or_country)
        if self.country and self.country != self.state_or_country:
            parts.append(self.country)
        
        location_str = ", ".join(parts)
        if self.remote:
            location_str += " (Remote)"
        
        return location_str

@dataclass
class ContactInfo:
    """Contact information structure"""
    emails: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)
    
    def add_email(self, email: str):
        """Add email if valid."""
        if self._is_valid_email(email):
            self.emails.append(email)
        else:
            logger.warning(f"Invalid email format: {email}")
    
    def add_phone(self, phone: str):
        """Add phone if valid."""
        if self._is_valid_phone(phone):
            self.phones.append(phone)
        else:
            logger.warning(f"Invalid phone format: {phone}")
    
    def add_url(self, url: str):
        """Add URL if valid."""
        if self._is_valid_url(url):
            self.urls.append(url)
        else:
            logger.warning(f"Invalid URL format: {url}")
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Validate phone format."""
        pattern = r'^\+?[\d\s\-\(\)]{10,}$'
        return bool(re.match(pattern, phone))
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        pattern = r'^https?://.+'
        return bool(re.match(pattern, url))

@dataclass
class SalaryInfo:
    """Salary information structure"""
    min_salary: Optional[float] = None
    max_salary: Optional[float] = None
    currency: str = "USD"
    period: str = "year"  # year, month, hour
    raw_text: str = ""
    
    def __post_init__(self):
        """Parse raw salary text if provided."""
        if self.raw_text and not self.min_salary:
            self._parse_salary_text()
    
    def _parse_salary_text(self):
        """Parse salary from raw text."""
        try:
            # Remove currency symbols and common words
            text = re.sub(r'[^\d\-\$,\s]', '', self.raw_text)
            text = re.sub(r'\$', '', text)
            
            # Extract numbers
            numbers = re.findall(r'\d+', text.replace(',', ''))
            if numbers:
                numbers = [int(num) for num in numbers]
                
                if len(numbers) == 1:
                    self.min_salary = numbers[0]
                elif len(numbers) >= 2:
                    self.min_salary = min(numbers)
                    self.max_salary = max(numbers)
                
                # Detect if in thousands
                if 'k' in self.raw_text.lower() or 'thousand' in self.raw_text.lower():
                    if self.min_salary:
                        self.min_salary *= 1000
                    if self.max_salary:
                        self.max_salary *= 1000
                
                logger.debug(f"Parsed salary: {self.min_salary} - {self.max_salary}")
                
        except Exception as e:
            logger.error(f"Error parsing salary text: {str(e)}")
    
    def to_string(self) -> str:
        """Convert salary info to string representation."""
        if self.min_salary and self.max_salary:
            return f"${self.min_salary:,.0f} - ${self.max_salary:,.0f}"
        elif self.min_salary:
            return f"${self.min_salary:,.0f}+"
        else:
            return self.raw_text or "Not specified"

@dataclass
class JobSchema:
    """Main job posting schema"""
    # Basic information
    id: str = ""
    title: str = ""
    company: str = ""
    location: str = ""
    description: str = ""
    url: str = ""
    
    # Job details
    job_type: str = ""
    experience_level: str = ""
    years_experience: Optional[int] = None
    
    # Salary and benefits
    salary: str = ""
    salary_info: Optional[SalaryInfo] = None
    
    # Location details
    location_data: Optional[LocationData] = None
    
    # Contact information
    contact_info: Optional[ContactInfo] = None
    
    # Skills and requirements
    skills: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    
    # Dates
    date_posted: str = ""
    date_expires: Optional[str] = None
    scraped_date: str = ""
    
    # Metadata
    source: str = "linkedin"
    status: JobStatus = JobStatus.ACTIVE
    job_hash: str = ""
    
    # Additional fields
    industry: str = ""
    company_size: str = ""
    employment_type: str = ""
    
    def __post_init__(self):
        """Validate and process data after initialization."""
        self._validate_required_fields()
        self._process_location()
        self._process_salary()
        self._process_contact_info()
        self._generate_job_hash()
    
    def _validate_required_fields(self):
        """Validate required fields."""
        required_fields = ['title', 'company']
        
        for field_name in required_fields:
            if not getattr(self, field_name):
                logger.warning(f"Missing required field: {field_name}")
    
    def _process_location(self):
        """Process location string into LocationData."""
        if self.location and not self.location_data:
            self.location_data = self._parse_location(self.location)
    
    def _parse_location(self, location_str: str) -> LocationData:
        """Parse location string into components."""
        location_data = LocationData()
        
        if not location_str:
            return location_data
        
        # Check for remote work indicators
        remote_keywords = ['remote', 'work from home', 'wfh', 'distributed', 'anywhere']
        if any(keyword in location_str.lower() for keyword in remote_keywords):
            location_data.remote = True
        
        # Parse city, state/country format
        if ',' in location_str:
            parts = [part.strip() for part in location_str.split(',')]
            if len(parts) >= 2:
                location_data.city = parts[0]
                location_data.state_or_country = parts[1]
                if len(parts) > 2:
                    location_data.country = parts[2]
        else:
            location_data.city = location_str
        
        return location_data
    
    def _process_salary(self):
        """Process salary string into SalaryInfo."""
        if self.salary and not self.salary_info:
            self.salary_info = SalaryInfo(raw_text=self.salary)
    
    def _process_contact_info(self):
        """Extract contact information from description."""
        if self.description and not self.contact_info:
            self.contact_info = self._extract_contact_info(self.description)
    
    def _extract_contact_info(self, text: str) -> ContactInfo:
        """Extract contact information from text."""
        contact_info = ContactInfo()
        
        # Extract emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        for email in emails:
            contact_info.add_email(email)
        
        # Extract phone numbers
        phone_pattern = r'\b(?:\+1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        phones = re.findall(phone_pattern, text)
        for phone in phones:
            contact_info.add_phone('-'.join(phone))
        
        # Extract URLs
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        urls = re.findall(url_pattern, text)
        for url in urls:
            contact_info.add_url(url)
        
        return contact_info
    
    def _generate_job_hash(self):
        """Generate hash for duplicate detection."""
        if not self.job_hash:
            hash_components = [
                self.title.lower().strip(),
                self.company.lower().strip(),
                self.location.lower().strip()
            ]
            hash_string = '|'.join(hash_components)
            self.job_hash = str(hash(hash_string.encode())).replace('-', '')[:16]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job schema to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'url': self.url,
            'job_type': self.job_type,
            'experience_level': self.experience_level,
            'years_experience': self.years_experience,
            'salary': self.salary,
            'salary_info': self.salary_info.to_dict() if self.salary_info else None,
            'location_data': self.location_data.to_dict() if self.location_data else None,
            'contact_info': self.contact_info.to_dict() if self.contact_info else None,
            'skills': self.skills,
            'requirements': self.requirements,
            'benefits': self.benefits,
            'date_posted': self.date_posted,
            'date_expires': self.date_expires,
            'scraped_date': self.scraped_date,
            'source': self.source,
            'status': self.status.value,
            'job_hash': self.job_hash,
            'industry': self.industry,
            'company_size': self.company_size,
            'employment_type': self.employment_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobSchema':
        """Create JobSchema from dictionary."""
        # Extract nested objects
        salary_info = None
        if data.get('salary_info'):
            salary_info = SalaryInfo(**data['salary_info'])
        
        location_data = None
        if data.get('location_data'):
            location_data = LocationData(**data['location_data'])
        
        contact_info = None
        if data.get('contact_info'):
            contact_info = ContactInfo(**data['contact_info'])
        
        # Create job schema
        job = cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            company=data.get('company', ''),
            location=data.get('location', ''),
            description=data.get('description', ''),
            url=data.get('url', ''),
            job_type=data.get('job_type', ''),
            experience_level=data.get('experience_level', ''),
            years_experience=data.get('years_experience'),
            salary=data.get('salary', ''),
            salary_info=salary_info,
            location_data=location_data,
            contact_info=contact_info,
            skills=data.get('skills', []),
            requirements=data.get('requirements', []),
            benefits=data.get('benefits', []),
            date_posted=data.get('date_posted', ''),
            date_expires=data.get('date_expires'),
            scraped_date=data.get('scraped_date', ''),
            source=data.get('source', 'linkedin'),
            status=JobStatus(data.get('status', 'active')),
            job_hash=data.get('job_hash', ''),
            industry=data.get('industry', ''),
            company_size=data.get('company_size', ''),
            employment_type=data.get('employment_type', '')
        )
        
        return job

@dataclass
class SearchSchema:
    """Search query schema"""
    query: str = ""
    job_title: str = ""
    company: str = ""
    location: str = ""
    job_type: str = "All"
    experience_level: str = "All"
    date_posted: str = "All"
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    remote_only: bool = False
    skills: List[str] = field(default_factory=list)
    industry: str = ""
    sort_by: str = "Relevance"
    limit: int = 10
    
    def to_filters(self) -> Dict[str, Any]:
        """Convert search schema to filter dictionary."""
        filters = {}
        
        if self.job_type != "All":
            filters['job_type'] = self.job_type
        
        if self.experience_level != "All":
            filters['experience_level'] = self.experience_level
        
        if self.date_posted != "All":
            filters['date_posted'] = self.date_posted
        
        if self.company:
            filters['company'] = self.company
        
        if self.location:
            filters['location'] = self.location
        
        if self.industry:
            filters['industry'] = self.industry
        
        if self.remote_only:
            filters['remote_only'] = True
        
        if self.salary_min is not None:
            filters['salary_min'] = self.salary_min
        
        if self.salary_max is not None:
            filters['salary_max'] = self.salary_max
        
        return filters
    
    def get_search_text(self) -> str:
        """Get the main search text for semantic search."""
        search_parts = []
        
        if self.query:
            search_parts.append(self.query)
        else:
            if self.job_title:
                search_parts.append(self.job_title)
            if self.skills:
                search_parts.extend(self.skills)
        
        return ' '.join(search_parts)

# Validation functions
def validate_job_schema(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate job data against schema.
    
    Args:
        job_data: Job data dictionary to validate
        
    Returns:
        Dictionary with validation results
    """
    validation_result = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    try:
        # Required fields validation
        required_fields = ['title', 'company']
        for field in required_fields:
            if not job_data.get(field):
                validation_result['errors'].append(f"Missing required field: {field}")
                validation_result['is_valid'] = False
        
        # Field length validation
        if job_data.get('title') and len(job_data['title']) > 200:
            validation_result['warnings'].append("Job title is unusually long")
        
        if job_data.get('company') and len(job_data['company']) > 100:
            validation_result['warnings'].append("Company name is unusually long")
        
        if job_data.get('description') and len(job_data['description']) < 50:
            validation_result['warnings'].append("Job description is very short")
        
        # URL validation
        url = job_data.get('url', '')
        if url and not url.startswith(('http://', 'https://')):
            validation_result['warnings'].append("URL format appears invalid")
        
        # Date validation
        date_posted = job_data.get('date_posted', '')
        if date_posted:
            try:
                datetime.strptime(date_posted, '%Y-%m-%d')
            except ValueError:
                validation_result['warnings'].append("Date format appears invalid")
        
        logger.debug(f"Job validation result: {validation_result}")
        
    except Exception as e:
        logger.error(f"Error validating job schema: {str(e)}")
        validation_result['errors'].append(f"Validation error: {str(e)}")
        validation_result['is_valid'] = False
    
    return validation_result

def validate_search_schema(search_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate search data against schema.
    
    Args:
        search_data: Search data dictionary to validate
        
    Returns:
        Dictionary with validation results
    """
    validation_result = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    try:
        # Check if at least one search criterion is provided
        search_fields = ['query', 'job_title', 'company', 'location', 'skills']
        has_search_criteria = any(search_data.get(field) for field in search_fields)
        
        if not has_search_criteria:
            validation_result['warnings'].append("No search criteria provided")
        
        # Validate numeric fields
        if search_data.get('salary_min') is not None:
            try:
                float(search_data['salary_min'])
            except (ValueError, TypeError):
                validation_result['errors'].append("Invalid salary_min value")
                validation_result['is_valid'] = False
        
        if search_data.get('salary_max') is not None:
            try:
                float(search_data['salary_max'])
            except (ValueError, TypeError):
                validation_result['errors'].append("Invalid salary_max value")
                validation_result['is_valid'] = False
        
        # Validate limit
        limit = search_data.get('limit', 10)
        if not isinstance(limit, int) or limit <= 0:
            validation_result['errors'].append("Invalid limit value")
            validation_result['is_valid'] = False
        
        logger.debug(f"Search validation result: {validation_result}")
        
    except Exception as e:
        logger.error(f"Error validating search schema: {str(e)}")
        validation_result['errors'].append(f"Validation error: {str(e)}")
        validation_result['is_valid'] = False
    
    return validation_result

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example job data
    job_data = {
        'id': 'job_001',
        'title': 'Senior Data Scientist',
        'company': 'TechCorp Inc.',
        'location': 'San Francisco, CA',
        'description': 'Looking for an experienced data scientist with Python and machine learning skills. Contact us at jobs@techcorp.com or call (555) 123-4567.',
        'url': 'https://linkedin.com/jobs/view/123456',
        'job_type': 'Full-time',
        'experience_level': 'Mid-Senior level',
        'salary': '$120,000 - $150,000 per year',
        'skills': ['python', 'machine learning', 'tensorflow'],
        'date_posted': '2024-01-15',
        'scraped_date': '2024-01-15T10:30:00'
    }
    
    # Create job schema
    job = JobSchema.from_dict(job_data)
    print(f"Created job: {job.title} at {job.company}")
    print(f"Location: {job.location_data.to_string()}")
    print(f"Salary: {job.salary_info.to_string()}")
    print(f"Contact: {len(job.contact_info.emails)} emails, {len(job.contact_info.phones)} phones")
    
    # Validate job
    validation = validate_job_schema(job_data)
    print(f"Validation result: {validation}")
    
    # Example search
    search_data = {
        'query': 'python machine learning',
        'location': 'San Francisco',
        'job_type': 'Full-time',
        'experience_level': 'Mid-Senior level',
        'salary_min': 100000,
        'limit': 20
    }
    
    search = SearchSchema.from_dict(search_data)
    print(f"Search filters: {search.to_filters()}")
    print(f"Search text: {search.get_search_text()}")
