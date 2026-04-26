"""
URL Builder Module
Handles construction of LinkedIn job search URLs with various filters and parameters.
Enhanced with comprehensive logging and error handling.
"""

import logging
from urllib.parse import urlencode, quote_plus
from typing import Dict, List, Optional, Any
from enum import Enum

# Set up logging
logger = logging.getLogger(__name__)

class JobType(Enum):
    """Enum for LinkedIn job types"""
    FULL_TIME = "F"
    PART_TIME = "P"
    CONTRACT = "C"
    TEMPORARY = "T"
    INTERNSHIP = "I"

class ExperienceLevel(Enum):
    """Enum for LinkedIn experience levels"""
    INTERNSHIP = "1"
    ENTRY_LEVEL = "2"
    ASSOCIATE = "3"
    MID_SENIOR = "4"
    DIRECTOR = "5"
    EXECUTIVE = "6"

class DatePosted(Enum):
    """Enum for LinkedIn date posted filters"""
    PAST_24_HOURS = "r86400"
    PAST_WEEK = "r604800"
    PAST_MONTH = "r2592000"
    ANY_TIME = "r86400"

class SortBy(Enum):
    """Enum for LinkedIn sort options"""
    RELEVANCE = "R"
    DATE_POSTED = "DD"
    MOST_RELEVANT = "R"

class URLBuilder:
    """
    URL builder for LinkedIn job search URLs.
    Enhanced with comprehensive logging and error handling.
    """
    
    def __init__(self, base_url: str = "https://www.linkedin.com/jobs/search"):
        """
        Initialize the URL builder.
        
        Args:
            base_url: Base URL for LinkedIn job search
        """
        self.base_url = base_url
        logger.info(f"Initialized URLBuilder with base URL: {base_url}")
        
        # Default parameters
        self.default_params = {
            'sortBy': SortBy.DATE_POSTED.value,
            'f_TPR': DatePosted.PAST_WEEK.value
        }
        
        # Parameter mappings
        self.job_type_mapping = {
            'Full-time': JobType.FULL_TIME.value,
            'Part-time': JobType.PART_TIME.value,
            'Contract': JobType.CONTRACT.value,
            'Temporary': JobType.TEMPORARY.value,
            'Internship': JobType.INTERNSHIP.value
        }
        
        self.experience_mapping = {
            'Internship': ExperienceLevel.INTERNSHIP.value,
            'Entry level': ExperienceLevel.ENTRY_LEVEL.value,
            'Associate': ExperienceLevel.ASSOCIATE.value,
            'Mid-Senior level': ExperienceLevel.MID_SENIOR.value,
            'Director': ExperienceLevel.DIRECTOR.value,
            'Executive': ExperienceLevel.EXECUTIVE.value
        }
        
        self.date_mapping = {
            'Past 24 hours': DatePosted.PAST_24_HOURS.value,
            'Past week': DatePosted.PAST_WEEK.value,
            'Past month': DatePosted.PAST_MONTH.value,
            'Any time': DatePosted.ANY_TIME.value
        }
        
        self.sort_mapping = {
            'Relevance': SortBy.RELEVANCE.value,
            'Date posted': SortBy.DATE_POSTED.value,
            'Most relevant': SortBy.MOST_RELEVANT.value
        }
    
    def build_search_url(self, 
                        job_title: str = "",
                        location: str = "",
                        start: int = 0,
                        filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Build a LinkedIn job search URL with parameters.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            start: Starting position for pagination (0-based)
            filters: Additional filters to apply
            
        Returns:
            Complete LinkedIn search URL
        """
        logger.debug(f"Building URL for: title='{job_title}', location='{location}', start={start}")
        
        try:
            # Start with default parameters
            params = self.default_params.copy()
            
            # Add basic search parameters
            if job_title:
                params['keywords'] = job_title
            if location:
                params['location'] = location
            if start > 0:
                params['start'] = start
            
            # Add filters if provided
            if filters:
                params.update(self._process_filters(filters))
            
            # Build URL
            url = f"{self.base_url}?{urlencode(params)}"
            
            logger.debug(f"Built URL: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Error building URL: {str(e)}")
            # Return basic URL if building fails
            return f"{self.base_url}?keywords={quote_plus(job_title)}&location={quote_plus(location)}"
    
    def _process_filters(self, filters: Dict[str, Any]) -> Dict[str, str]:
        """
        Process and convert filters to LinkedIn URL parameters.
        
        Args:
            filters: Dictionary of filters
            
        Returns:
            Dictionary of URL parameters
        """
        params = {}
        
        try:
            # Job type filter
            if filters.get('job_type') and filters['job_type'] != 'All':
                job_type_value = self.job_type_mapping.get(filters['job_type'])
                if job_type_value:
                    params['f_JT'] = job_type_value
                    logger.debug(f"Added job type filter: {filters['job_type']} -> {job_type_value}")
            
            # Experience level filter
            if filters.get('experience_level') and filters['experience_level'] != 'All':
                exp_value = self.experience_mapping.get(filters['experience_level'])
                if exp_value:
                    params['f_E'] = exp_value
                    logger.debug(f"Added experience filter: {filters['experience_level']} -> {exp_value}")
            
            # Date posted filter
            if filters.get('date_posted') and filters['date_posted'] != 'All':
                date_value = self.date_mapping.get(filters['date_posted'])
                if date_value:
                    params['f_TPR'] = date_value
                    logger.debug(f"Added date filter: {filters['date_posted']} -> {date_value}")
            
            # Sort by filter
            if filters.get('sort_by'):
                sort_value = self.sort_mapping.get(filters['sort_by'])
                if sort_value:
                    params['sortBy'] = sort_value
                    logger.debug(f"Added sort filter: {filters['sort_by']} -> {sort_value}")
            
            # Company filter
            if filters.get('company'):
                params['f_C'] = filters['company']
                logger.debug(f"Added company filter: {filters['company']}")
            
            # Industry filter
            if filters.get('industry'):
                params['f_I'] = filters['industry']
                logger.debug(f"Added industry filter: {filters['industry']}")
            
            # Salary filter
            if filters.get('salary_min') or filters.get('salary_max'):
                salary_filter = self._build_salary_filter(filters)
                if salary_filter:
                    params.update(salary_filter)
                    logger.debug(f"Added salary filter: {salary_filter}")
            
            # Remote work filter
            if filters.get('remote_only'):
                params['f_WT'] = '2'  # Remote work filter
                logger.debug("Added remote work filter")
            
            # Job function filter
            if filters.get('job_function'):
                params['f_F'] = filters['job_function']
                logger.debug(f"Added job function filter: {filters['job_function']}")
            
            # Employment type filter
            if filters.get('employment_type'):
                params['f_E'] = filters['employment_type']
                logger.debug(f"Added employment type filter: {filters['employment_type']}")
            
        except Exception as e:
            logger.error(f"Error processing filters: {str(e)}")
        
        return params
    
    def _build_salary_filter(self, filters: Dict[str, Any]) -> Dict[str, str]:
        """
        Build salary filter parameters.
        
        Args:
            filters: Dictionary containing salary filters
            
        Returns:
            Dictionary of salary filter parameters
        """
        salary_params = {}
        
        try:
            salary_min = filters.get('salary_min')
            salary_max = filters.get('salary_max')
            
            if salary_min is not None:
                # Convert to LinkedIn salary format (multiply by 1000 for K values)
                if salary_min < 1000:
                    salary_min *= 1000
                salary_params['f_SB2'] = str(salary_min)
            
            if salary_max is not None:
                if salary_max < 1000:
                    salary_max *= 1000
                salary_params['f_SB3'] = str(salary_max)
            
        except Exception as e:
            logger.error(f"Error building salary filter: {str(e)}")
        
        return salary_params
    
    def build_advanced_search_url(self, search_config: Dict[str, Any]) -> str:
        """
        Build an advanced search URL with complex filters.
        
        Args:
            search_config: Dictionary containing advanced search configuration
            
        Returns:
            Complete LinkedIn search URL
        """
        logger.info("Building advanced search URL")
        
        try:
            # Extract basic parameters
            job_title = search_config.get('job_title', '')
            location = search_config.get('location', '')
            start = search_config.get('start', 0)
            
            # Extract filters
            filters = search_config.get('filters', {})
            
            # Build URL
            url = self.build_search_url(job_title, location, start, filters)
            
            logger.info(f"Built advanced search URL: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Error building advanced search URL: {str(e)}")
            return self.base_url
    
    def build_pagination_urls(self, 
                            job_title: str,
                            location: str,
                            max_pages: int,
                            filters: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Build URLs for multiple pages of results.
        
        Args:
            job_title: Job title to search for
            location: Location to search in
            max_pages: Maximum number of pages to generate URLs for
            filters: Additional filters to apply
            
        Returns:
            List of URLs for each page
        """
        logger.info(f"Building pagination URLs for {max_pages} pages")
        
        urls = []
        
        try:
            for page in range(max_pages):
                start = page * 25  # LinkedIn shows 25 jobs per page
                url = self.build_search_url(job_title, location, start, filters)
                urls.append(url)
                logger.debug(f"Generated URL for page {page + 1}: {url}")
            
            logger.info(f"Generated {len(urls)} pagination URLs")
            return urls
            
        except Exception as e:
            logger.error(f"Error building pagination URLs: {str(e)}")
            return []
    
    def validate_url(self, url: str) -> bool:
        """
        Validate a LinkedIn job search URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is valid, False otherwise
        """
        try:
            if not url.startswith(self.base_url):
                logger.warning(f"URL does not start with base URL: {url}")
                return False
            
            # Check for required parameters
            if 'keywords' not in url and 'location' not in url:
                logger.warning("URL missing required parameters")
                return False
            
            logger.debug(f"URL validation passed: {url}")
            return True
            
        except Exception as e:
            logger.error(f"Error validating URL: {str(e)}")
            return False
    
    def get_available_filters(self) -> Dict[str, List[str]]:
        """
        Get list of available filters and their options.
        
        Returns:
            Dictionary of available filters and their options
        """
        return {
            'job_type': list(self.job_type_mapping.keys()),
            'experience_level': list(self.experience_mapping.keys()),
            'date_posted': list(self.date_mapping.keys()),
            'sort_by': list(self.sort_mapping.keys())
        }
    
    def get_filter_mapping(self, filter_type: str) -> Dict[str, str]:
        """
        Get the mapping for a specific filter type.
        
        Args:
            filter_type: Type of filter ('job_type', 'experience_level', etc.)
            
        Returns:
            Dictionary mapping display names to URL values
        """
        mapping_dicts = {
            'job_type': self.job_type_mapping,
            'experience_level': self.experience_mapping,
            'date_posted': self.date_mapping,
            'sort_by': self.sort_mapping
        }
        
        return mapping_dicts.get(filter_type, {})

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    url_builder = URLBuilder()
    
    # Basic search
    basic_url = url_builder.build_search_url(
        job_title="Data Scientist",
        location="San Francisco, CA"
    )
    print(f"Basic URL: {basic_url}")
    
    # Advanced search with filters
    filters = {
        'job_type': 'Full-time',
        'experience_level': 'Mid-Senior level',
        'date_posted': 'Past week',
        'remote_only': True
    }
    
    advanced_url = url_builder.build_search_url(
        job_title="Python Developer",
        location="Remote",
        filters=filters
    )
    print(f"Advanced URL: {advanced_url}")
    
    # Pagination URLs
    pagination_urls = url_builder.build_pagination_urls(
        job_title="Software Engineer",
        location="New York, NY",
        max_pages=3,
        filters=filters
    )
    print(f"Pagination URLs: {len(pagination_urls)}")
    
    # Available filters
    available_filters = url_builder.get_available_filters()
    print(f"Available filters: {available_filters}")
