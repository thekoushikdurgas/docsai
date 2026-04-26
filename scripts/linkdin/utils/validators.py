"""
Data Validation Module
Provides comprehensive data validation for job postings and user inputs.
Enhanced with detailed error reporting and validation rules.
"""

import re
import logging
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime, date
from dataclasses import dataclass
from enum import Enum
import urllib.parse
import email_validator
from email_validator import validate_email, EmailNotValidError

# Set up logging
logger = logging.getLogger(__name__)

class ValidationLevel(Enum):
    """Enum for validation levels"""
    STRICT = "strict"
    MODERATE = "moderate"
    LENIENT = "lenient"

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

@dataclass
class ValidationResult:
    """Result of validation operation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    score: int
    validated_data: Dict[str, Any]
    
    def __post_init__(self):
        """Calculate validation score if not provided."""
        if self.score == 0 and self.is_valid:
            self.score = 100
        elif self.score == 0:
            # Calculate score based on errors and warnings
            self.score = max(0, 100 - len(self.errors) * 20 - len(self.warnings) * 5)

class DataValidator:
    """
    Comprehensive data validator for job postings and user inputs.
    """
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.MODERATE):
        """
        Initialize data validator.
        
        Args:
            validation_level: Level of validation strictness
        """
        self.validation_level = validation_level
        self.stats = {
            'validations_performed': 0,
            'valid_items': 0,
            'invalid_items': 0,
            'warnings_generated': 0
        }
        
        # Validation patterns
        self.patterns = self._load_validation_patterns()
        
        logger.info(f"DataValidator initialized with level: {validation_level.value}")
    
    def _load_validation_patterns(self) -> Dict[str, str]:
        """Load validation patterns for different data types."""
        return {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone_us': r'^\+?1[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$',
            'phone_international': r'^\+[1-9]\d{1,14}$',
            'url': r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$',
            'date_iso': r'^\d{4}-\d{2}-\d{2}$',
            'date_us': r'^\d{2}/\d{2}/\d{4}$',
            'date_eu': r'^\d{2}/\d{2}/\d{4}$',
            'salary_range': r'^\$?[\d,]+(?: - \$?[\d,]+)?$',
            'job_id': r'^[a-zA-Z0-9_-]+$',
            'company_name': r'^[a-zA-Z0-9\s&.,-]+$',
            'job_title': r'^[a-zA-Z0-9\s&.,-]+$'
        }
    
    def validate_job_posting(self, job_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate a complete job posting.
        
        Args:
            job_data: Job posting data dictionary
            
        Returns:
            ValidationResult object
        """
        self.stats['validations_performed'] += 1
        
        errors = []
        warnings = []
        validated_data = job_data.copy()
        
        try:
            # Validate required fields
            required_fields = ['title', 'company']
            for field in required_fields:
                if not job_data.get(field):
                    errors.append(f"Missing required field: {field}")
                else:
                    # Validate field content
                    field_errors, field_warnings = self._validate_field(field, job_data[field])
                    errors.extend(field_errors)
                    warnings.extend(field_warnings)
            
            # Validate optional fields
            optional_fields = ['location', 'description', 'url', 'salary', 'date_posted']
            for field in optional_fields:
                if job_data.get(field):
                    field_errors, field_warnings = self._validate_field(field, job_data[field])
                    errors.extend(field_errors)
                    warnings.extend(field_warnings)
            
            # Validate job-specific fields
            self._validate_job_specific_fields(job_data, errors, warnings)
            
            # Validate data consistency
            self._validate_data_consistency(job_data, errors, warnings)
            
            # Calculate validation score
            score = self._calculate_validation_score(errors, warnings)
            
            is_valid = len(errors) == 0
            
            if is_valid:
                self.stats['valid_items'] += 1
            else:
                self.stats['invalid_items'] += 1
            
            self.stats['warnings_generated'] += len(warnings)
            
            logger.debug(f"Job validation completed: {len(errors)} errors, {len(warnings)} warnings")
            
            return ValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                score=score,
                validated_data=validated_data
            )
            
        except Exception as e:
            logger.error(f"Error validating job posting: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                score=0,
                validated_data=job_data
            )
    
    def _validate_field(self, field_name: str, value: Any) -> Tuple[List[str], List[str]]:
        """
        Validate a specific field.
        
        Args:
            field_name: Name of the field
            value: Value to validate
            
        Returns:
            Tuple of (errors, warnings)
        """
        errors = []
        warnings = []
        
        if value is None or value == "":
            return errors, warnings
        
        try:
            if field_name == 'title':
                errors.extend(self._validate_job_title(value))
            elif field_name == 'company':
                errors.extend(self._validate_company_name(value))
            elif field_name == 'location':
                errors.extend(self._validate_location(value))
            elif field_name == 'description':
                errors.extend(self._validate_description(value))
            elif field_name == 'url':
                errors.extend(self._validate_url(value))
            elif field_name == 'salary':
                errors.extend(self._validate_salary(value))
            elif field_name == 'date_posted':
                errors.extend(self._validate_date(value))
            elif field_name == 'email':
                errors.extend(self._validate_email(value))
            elif field_name == 'phone':
                errors.extend(self._validate_phone(value))
            else:
                # Generic validation
                if isinstance(value, str):
                    if len(value) > 1000:
                        warnings.append(f"{field_name} is very long")
                elif isinstance(value, (int, float)):
                    if value < 0:
                        warnings.append(f"{field_name} is negative")
        
        except Exception as e:
            errors.append(f"Error validating {field_name}: {str(e)}")
        
        return errors, warnings
    
    def _validate_job_title(self, title: str) -> List[str]:
        """Validate job title."""
        errors = []
        
        if not isinstance(title, str):
            errors.append("Job title must be a string")
            return errors
        
        if len(title.strip()) == 0:
            errors.append("Job title cannot be empty")
        elif len(title) < 3:
            errors.append("Job title is too short")
        elif len(title) > 200:
            errors.append("Job title is too long")
        
        # Check for suspicious patterns
        if re.search(r'[<>{}]', title):
            errors.append("Job title contains invalid characters")
        
        # Check for excessive repetition
        words = title.lower().split()
        if len(words) > 1:
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            max_repetition = max(word_counts.values())
            if max_repetition > len(words) // 2:
                errors.append("Job title has excessive word repetition")
        
        return errors
    
    def _validate_company_name(self, company: str) -> List[str]:
        """Validate company name."""
        errors = []
        
        if not isinstance(company, str):
            errors.append("Company name must be a string")
            return errors
        
        if len(company.strip()) == 0:
            errors.append("Company name cannot be empty")
        elif len(company) < 2:
            errors.append("Company name is too short")
        elif len(company) > 100:
            errors.append("Company name is too long")
        
        # Check for suspicious patterns
        if re.search(r'[<>{}]', company):
            errors.append("Company name contains invalid characters")
        
        # Check for excessive repetition
        if len(set(company.lower())) < len(company) // 2:
            errors.append("Company name has excessive character repetition")
        
        return errors
    
    def _validate_location(self, location: str) -> List[str]:
        """Validate location."""
        errors = []
        
        if not isinstance(location, str):
            errors.append("Location must be a string")
            return errors
        
        if len(location.strip()) == 0:
            errors.append("Location cannot be empty")
        elif len(location) > 200:
            errors.append("Location is too long")
        
        # Check for suspicious patterns
        if re.search(r'[<>{}]', location):
            errors.append("Location contains invalid characters")
        
        return errors
    
    def _validate_description(self, description: str) -> List[str]:
        """Validate job description."""
        errors = []
        
        if not isinstance(description, str):
            errors.append("Description must be a string")
            return errors
        
        if len(description.strip()) == 0:
            errors.append("Description cannot be empty")
        elif len(description) < 50:
            errors.append("Description is too short")
        elif len(description) > 10000:
            errors.append("Description is too long")
        
        # Check for suspicious patterns
        if re.search(r'[<>{}]', description):
            errors.append("Description contains invalid characters")
        
        # Check for excessive repetition
        words = description.lower().split()
        if len(words) > 10:
            word_counts = {}
            for word in words:
                if len(word) > 3:  # Only count longer words
                    word_counts[word] = word_counts.get(word, 0) + 1
            if word_counts:
                max_repetition = max(word_counts.values())
                if max_repetition > len(words) // 4:
                    errors.append("Description has excessive word repetition")
        
        return errors
    
    def _validate_url(self, url: str) -> List[str]:
        """Validate URL."""
        errors = []
        
        if not isinstance(url, str):
            errors.append("URL must be a string")
            return errors
        
        if len(url.strip()) == 0:
            errors.append("URL cannot be empty")
            return errors
        
        try:
            parsed = urllib.parse.urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                errors.append("Invalid URL format")
            elif parsed.scheme not in ['http', 'https']:
                errors.append("URL must use HTTP or HTTPS protocol")
        except Exception:
            errors.append("Invalid URL format")
        
        return errors
    
    def _validate_salary(self, salary: str) -> List[str]:
        """Validate salary information."""
        errors = []
        
        if not isinstance(salary, str):
            errors.append("Salary must be a string")
            return errors
        
        if len(salary.strip()) == 0:
            return errors  # Empty salary is allowed
        
        # Check for valid salary patterns
        if not re.match(self.patterns['salary_range'], salary):
            errors.append("Invalid salary format")
        
        # Extract numbers and validate
        numbers = re.findall(r'[\d,]+', salary.replace(',', ''))
        if numbers:
            try:
                for num_str in numbers:
                    num = int(num_str)
                    if num < 0:
                        errors.append("Salary cannot be negative")
                    elif num > 10000000:  # 10 million
                        errors.append("Salary seems unreasonably high")
            except ValueError:
                errors.append("Invalid salary numbers")
        
        return errors
    
    def _validate_date(self, date_str: str) -> List[str]:
        """Validate date string."""
        errors = []
        
        if not isinstance(date_str, str):
            errors.append("Date must be a string")
            return errors
        
        if len(date_str.strip()) == 0:
            return errors  # Empty date is allowed
        
        # Try different date formats
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%B %d, %Y',
            '%b %d, %Y'
        ]
        
        valid_date = False
        for fmt in date_formats:
            try:
                datetime.strptime(date_str, fmt)
                valid_date = True
                break
            except ValueError:
                continue
        
        if not valid_date:
            errors.append("Invalid date format")
        
        return errors
    
    def _validate_email(self, email: str) -> List[str]:
        """Validate email address."""
        errors = []
        
        if not isinstance(email, str):
            errors.append("Email must be a string")
            return errors
        
        if len(email.strip()) == 0:
            return errors  # Empty email is allowed
        
        try:
            validate_email(email)
        except EmailNotValidError as e:
            errors.append(f"Invalid email format: {str(e)}")
        
        return errors
    
    def _validate_phone(self, phone: str) -> List[str]:
        """Validate phone number."""
        errors = []
        
        if not isinstance(phone, str):
            errors.append("Phone must be a string")
            return errors
        
        if len(phone.strip()) == 0:
            return errors  # Empty phone is allowed
        
        # Check for valid phone patterns
        if not (re.match(self.patterns['phone_us'], phone) or 
                re.match(self.patterns['phone_international'], phone)):
            errors.append("Invalid phone number format")
        
        return errors
    
    def _validate_job_specific_fields(self, job_data: Dict[str, Any], 
                                    errors: List[str], warnings: List[str]):
        """Validate job-specific fields."""
        # Validate job type
        if job_data.get('job_type'):
            valid_types = ['Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship']
            if job_data['job_type'] not in valid_types:
                errors.append(f"Invalid job type: {job_data['job_type']}")
        
        # Validate experience level
        if job_data.get('experience_level'):
            valid_levels = ['Internship', 'Entry level', 'Mid level', 'Senior level', 'Executive']
            if job_data['experience_level'] not in valid_levels:
                errors.append(f"Invalid experience level: {job_data['experience_level']}")
        
        # Validate years of experience
        if job_data.get('years_experience'):
            try:
                years = int(job_data['years_experience'])
                if years < 0 or years > 50:
                    errors.append("Years of experience must be between 0 and 50")
            except (ValueError, TypeError):
                errors.append("Years of experience must be a number")
    
    def _validate_data_consistency(self, job_data: Dict[str, Any], 
                                 errors: List[str], warnings: List[str]):
        """Validate data consistency across fields."""
        # Check if job title and company are too similar
        title = job_data.get('title', '').lower()
        company = job_data.get('company', '').lower()
        
        if title and company:
            # Check for excessive overlap
            title_words = set(title.split())
            company_words = set(company.split())
            overlap = len(title_words.intersection(company_words))
            
            if overlap > len(title_words) // 2:
                warnings.append("Job title and company name are very similar")
        
        # Check if description is too similar to title
        description = job_data.get('description', '').lower()
        if title and description:
            title_words = set(title.split())
            desc_words = set(description.split())
            overlap = len(title_words.intersection(desc_words))
            
            if overlap > len(title_words) // 2:
                warnings.append("Job description is very similar to title")
    
    def _calculate_validation_score(self, errors: List[str], warnings: List[str]) -> int:
        """Calculate validation score based on errors and warnings."""
        score = 100
        
        # Deduct points for errors
        score -= len(errors) * 20
        
        # Deduct points for warnings
        score -= len(warnings) * 5
        
        return max(0, score)
    
    def validate_search_query(self, query: str) -> ValidationResult:
        """
        Validate search query.
        
        Args:
            query: Search query string
            
        Returns:
            ValidationResult object
        """
        errors = []
        warnings = []
        
        if not isinstance(query, str):
            errors.append("Search query must be a string")
        elif len(query.strip()) == 0:
            errors.append("Search query cannot be empty")
        elif len(query) > 500:
            errors.append("Search query is too long")
        
        # Check for suspicious patterns
        if query and re.search(r'[<>{}]', query):
            errors.append("Search query contains invalid characters")
        
        # Check for excessive repetition
        words = query.lower().split()
        if len(words) > 1:
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            max_repetition = max(word_counts.values())
            if max_repetition > len(words) // 2:
                warnings.append("Search query has excessive word repetition")
        
        score = self._calculate_validation_score(errors, warnings)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            score=score,
            validated_data={'query': query}
        )
    
    def validate_filters(self, filters: Dict[str, Any]) -> ValidationResult:
        """
        Validate search filters.
        
        Args:
            filters: Dictionary of search filters
            
        Returns:
            ValidationResult object
        """
        errors = []
        warnings = []
        validated_filters = {}
        
        # Validate each filter
        for key, value in filters.items():
            if value is None or value == "":
                continue
            
            if key == 'salary_min':
                try:
                    min_sal = float(value)
                    if min_sal < 0:
                        errors.append("Minimum salary cannot be negative")
                    elif min_sal > 1000000:
                        warnings.append("Minimum salary seems very high")
                    else:
                        validated_filters[key] = min_sal
                except (ValueError, TypeError):
                    errors.append("Minimum salary must be a number")
            
            elif key == 'salary_max':
                try:
                    max_sal = float(value)
                    if max_sal < 0:
                        errors.append("Maximum salary cannot be negative")
                    elif max_sal > 1000000:
                        warnings.append("Maximum salary seems very high")
                    else:
                        validated_filters[key] = max_sal
                except (ValueError, TypeError):
                    errors.append("Maximum salary must be a number")
            
            elif key in ['job_type', 'experience_level', 'date_posted']:
                if isinstance(value, str) and len(value) <= 100:
                    validated_filters[key] = value
                else:
                    errors.append(f"Invalid {key} value")
            
            elif key in ['company', 'location']:
                if isinstance(value, str) and len(value) <= 200:
                    validated_filters[key] = value
                else:
                    errors.append(f"Invalid {key} value")
            
            else:
                warnings.append(f"Unknown filter: {key}")
        
        # Validate salary range consistency
        if 'salary_min' in validated_filters and 'salary_max' in validated_filters:
            if validated_filters['salary_min'] > validated_filters['salary_max']:
                errors.append("Minimum salary cannot be greater than maximum salary")
        
        score = self._calculate_validation_score(errors, warnings)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            score=score,
            validated_data=validated_filters
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get validation statistics."""
        total = self.stats['validations_performed']
        valid_rate = self.stats['valid_items'] / total if total > 0 else 0
        
        return {
            **self.stats,
            'validation_level': self.validation_level.value,
            'valid_rate': valid_rate,
            'average_warnings': self.stats['warnings_generated'] / total if total > 0 else 0
        }
    
    def reset_statistics(self):
        """Reset validation statistics."""
        self.stats = {
            'validations_performed': 0,
            'valid_items': 0,
            'invalid_items': 0,
            'warnings_generated': 0
        }
        logger.info("Validation statistics reset")

# Global validator instance
validator = DataValidator()

def validate_job_data(job_data: Dict[str, Any]) -> ValidationResult:
    """Validate job data using global validator."""
    return validator.validate_job_posting(job_data)

def validate_search_query(query: str) -> ValidationResult:
    """Validate search query using global validator."""
    return validator.validate_search_query(query)

def validate_filters(filters: Dict[str, Any]) -> ValidationResult:
    """Validate search filters using global validator."""
    return validator.validate_filters(filters)

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    validator = DataValidator(ValidationLevel.STRICT)
    
    # Test job data validation
    job_data = {
        'title': 'Senior Data Scientist',
        'company': 'TechCorp Inc.',
        'location': 'San Francisco, CA',
        'description': 'Looking for an experienced data scientist with Python and machine learning skills.',
        'url': 'https://linkedin.com/jobs/view/123456',
        'salary': '$120,000 - $150,000',
        'date_posted': '2024-01-15',
        'job_type': 'Full-time',
        'experience_level': 'Mid-Senior level'
    }
    
    result = validator.validate_job_posting(job_data)
    print(f"Validation result: {result.is_valid}")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")
    print(f"Score: {result.score}")
    
    # Test search query validation
    query_result = validator.validate_search_query("python machine learning")
    print(f"Query validation: {query_result.is_valid}")
    
    # Test filter validation
    filters = {
        'job_type': 'Full-time',
        'salary_min': 100000,
        'salary_max': 200000
    }
    
    filter_result = validator.validate_filters(filters)
    print(f"Filter validation: {filter_result.is_valid}")
    
    # Get statistics
    stats = validator.get_statistics()
    print(f"Validation statistics: {stats}")
