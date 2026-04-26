"""
Configuration Management Module
Handles application configuration, environment variables, and settings.
Enhanced with comprehensive logging and validation.
"""

import os
import json
import yaml
import logging
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import toml

# Set up logging
logger = logging.getLogger(__name__)

class ConfigFormat(Enum):
    """Enum for configuration file formats"""
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    ENV = "env"

@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    persist_directory: str = "./chroma_db"
    collection_name: str = "job_postings"
    embedding_model: str = "all-MiniLM-L6-v2"
    max_results: int = 1000
    similarity_threshold: float = 0.7
    batch_size: int = 100
    cache_embeddings: bool = True
    cache_directory: str = "./embedding_cache"

@dataclass
class ScrapingConfig:
    """Scraping configuration settings"""
    delay_range: tuple = (2, 5)
    max_retries: int = 3
    max_pages: int = 5
    respect_robots_txt: bool = True
    user_agent_rotation: bool = True
    timeout: int = 30
    follow_redirects: bool = True
    max_jobs_per_search: int = 1000

@dataclass
class DashboardConfig:
    """Dashboard configuration settings"""
    page_title: str = "LinkedIn Job Analytics Dashboard"
    theme: str = "light"
    cache_ttl: int = 3600
    max_display_jobs: int = 50
    items_per_page: int = 25
    enable_analytics: bool = True
    enable_export: bool = True

@dataclass
class LoggingConfig:
    """Logging configuration settings"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "./logs/app.log"
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5
    enable_console: bool = True
    enable_file: bool = True

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    enable_rate_limiting: bool = True
    max_requests_per_minute: int = 60
    max_requests_per_hour: int = 1000
    enable_cors: bool = True
    allowed_origins: List[str] = field(default_factory=lambda: ["*"])
    enable_https: bool = False
    secret_key: str = ""

@dataclass
class Config:
    """Main configuration class"""
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    scraping: ScrapingConfig = field(default_factory=ScrapingConfig)
    dashboard: DashboardConfig = field(default_factory=DashboardConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    # Application settings
    app_name: str = "LinkedIn Job Scraper"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # File paths
    config_file: str = "config.yaml"
    env_file: str = ".env"
    
    def __post_init__(self):
        """Initialize configuration after creation."""
        self._load_environment_variables()
        self._validate_config()
    
    def _load_environment_variables(self):
        """Load configuration from environment variables."""
        try:
            # Database settings
            if os.getenv('DB_PERSIST_DIRECTORY'):
                self.database.persist_directory = os.getenv('DB_PERSIST_DIRECTORY')
            if os.getenv('DB_COLLECTION_NAME'):
                self.database.collection_name = os.getenv('DB_COLLECTION_NAME')
            if os.getenv('DB_EMBEDDING_MODEL'):
                self.database.embedding_model = os.getenv('DB_EMBEDDING_MODEL')
            
            # Scraping settings
            if os.getenv('SCRAPER_MAX_PAGES'):
                self.scraping.max_pages = int(os.getenv('SCRAPER_MAX_PAGES'))
            if os.getenv('SCRAPER_DELAY_MIN'):
                delay_min = int(os.getenv('SCRAPER_DELAY_MIN'))
                delay_max = int(os.getenv('SCRAPER_DELAY_MAX', str(delay_min + 3)))
                self.scraping.delay_range = (delay_min, delay_max)
            
            # Dashboard settings
            if os.getenv('DASHBOARD_THEME'):
                self.dashboard.theme = os.getenv('DASHBOARD_THEME')
            if os.getenv('DASHBOARD_MAX_JOBS'):
                self.dashboard.max_display_jobs = int(os.getenv('DASHBOARD_MAX_JOBS'))
            
            # Logging settings
            if os.getenv('LOG_LEVEL'):
                self.logging.level = os.getenv('LOG_LEVEL')
            if os.getenv('LOG_FILE'):
                self.logging.file_path = os.getenv('LOG_FILE')
            
            # Security settings
            if os.getenv('SECRET_KEY'):
                self.security.secret_key = os.getenv('SECRET_KEY')
            if os.getenv('ENABLE_RATE_LIMITING'):
                self.security.enable_rate_limiting = os.getenv('ENABLE_RATE_LIMITING').lower() == 'true'
            
            # Application settings
            if os.getenv('DEBUG'):
                self.debug = os.getenv('DEBUG').lower() == 'true'
            if os.getenv('ENVIRONMENT'):
                self.environment = os.getenv('ENVIRONMENT')
            
            logger.info("Environment variables loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading environment variables: {str(e)}")
    
    def _validate_config(self):
        """Validate configuration settings."""
        try:
            # Validate database settings
            if not self.database.persist_directory:
                raise ValueError("Database persist directory cannot be empty")
            
            if self.database.max_results <= 0:
                raise ValueError("Database max_results must be positive")
            
            if not 0 <= self.database.similarity_threshold <= 1:
                raise ValueError("Database similarity_threshold must be between 0 and 1")
            
            # Validate scraping settings
            if self.scraping.delay_range[0] < 0 or self.scraping.delay_range[1] < 0:
                raise ValueError("Scraping delay range must be non-negative")
            
            if self.scraping.delay_range[0] > self.scraping.delay_range[1]:
                raise ValueError("Scraping delay min must be less than or equal to max")
            
            if self.scraping.max_retries < 0:
                raise ValueError("Scraping max_retries must be non-negative")
            
            # Validate dashboard settings
            if self.dashboard.max_display_jobs <= 0:
                raise ValueError("Dashboard max_display_jobs must be positive")
            
            if self.dashboard.items_per_page <= 0:
                raise ValueError("Dashboard items_per_page must be positive")
            
            # Validate logging settings
            valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if self.logging.level.upper() not in valid_log_levels:
                raise ValueError(f"Logging level must be one of: {valid_log_levels}")
            
            # Validate security settings
            if self.security.max_requests_per_minute <= 0:
                raise ValueError("Security max_requests_per_minute must be positive")
            
            if self.security.max_requests_per_hour <= 0:
                raise ValueError("Security max_requests_per_hour must be positive")
            
            logger.info("Configuration validation completed successfully")
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            raise
    
    def load_from_file(self, file_path: str, format: ConfigFormat = ConfigFormat.YAML) -> bool:
        """
        Load configuration from file.
        
        Args:
            file_path: Path to configuration file
            format: Configuration file format
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                logger.warning(f"Configuration file not found: {file_path}")
                return False
            
            logger.info(f"Loading configuration from {file_path}")
            
            with open(file_path, 'r') as f:
                if format == ConfigFormat.JSON:
                    data = json.load(f)
                elif format == ConfigFormat.YAML:
                    data = yaml.safe_load(f)
                elif format == ConfigFormat.TOML:
                    data = toml.load(f)
                else:
                    logger.error(f"Unsupported configuration format: {format}")
                    return False
            
            # Update configuration
            self._update_from_dict(data)
            
            logger.info("Configuration loaded successfully from file")
            return True
            
        except Exception as e:
            logger.error(f"Error loading configuration from file: {str(e)}")
            return False
    
    def save_to_file(self, file_path: str, format: ConfigFormat = ConfigFormat.YAML) -> bool:
        """
        Save configuration to file.
        
        Args:
            file_path: Path to save configuration file
            format: Configuration file format
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Saving configuration to {file_path}")
            
            # Convert to dictionary
            data = self.to_dict()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                if format == ConfigFormat.JSON:
                    json.dump(data, f, indent=2)
                elif format == ConfigFormat.YAML:
                    yaml.dump(data, f, default_flow_style=False)
                elif format == ConfigFormat.TOML:
                    toml.dump(data, f)
                else:
                    logger.error(f"Unsupported configuration format: {format}")
                    return False
            
            logger.info("Configuration saved successfully to file")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration to file: {str(e)}")
            return False
    
    def _update_from_dict(self, data: Dict[str, Any]):
        """Update configuration from dictionary."""
        try:
            # Update database settings
            if 'database' in data:
                db_data = data['database']
                for key, value in db_data.items():
                    if hasattr(self.database, key):
                        setattr(self.database, key, value)
            
            # Update scraping settings
            if 'scraping' in data:
                scrap_data = data['scraping']
                for key, value in scrap_data.items():
                    if hasattr(self.scraping, key):
                        setattr(self.scraping, key, value)
            
            # Update dashboard settings
            if 'dashboard' in data:
                dash_data = data['dashboard']
                for key, value in dash_data.items():
                    if hasattr(self.dashboard, key):
                        setattr(self.dashboard, key, value)
            
            # Update logging settings
            if 'logging' in data:
                log_data = data['logging']
                for key, value in log_data.items():
                    if hasattr(self.logging, key):
                        setattr(self.logging, key, value)
            
            # Update security settings
            if 'security' in data:
                sec_data = data['security']
                for key, value in sec_data.items():
                    if hasattr(self.security, key):
                        setattr(self.security, key, value)
            
            # Update application settings
            for key, value in data.items():
                if hasattr(self, key) and not key.startswith('_'):
                    setattr(self, key, value)
            
            logger.debug("Configuration updated from dictionary")
            
        except Exception as e:
            logger.error(f"Error updating configuration from dictionary: {str(e)}")
            raise
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'database': {
                'persist_directory': self.database.persist_directory,
                'collection_name': self.database.collection_name,
                'embedding_model': self.database.embedding_model,
                'max_results': self.database.max_results,
                'similarity_threshold': self.database.similarity_threshold,
                'batch_size': self.database.batch_size,
                'cache_embeddings': self.database.cache_embeddings,
                'cache_directory': self.database.cache_directory
            },
            'scraping': {
                'delay_range': list(self.scraping.delay_range),
                'max_retries': self.scraping.max_retries,
                'max_pages': self.scraping.max_pages,
                'respect_robots_txt': self.scraping.respect_robots_txt,
                'user_agent_rotation': self.scraping.user_agent_rotation,
                'timeout': self.scraping.timeout,
                'follow_redirects': self.scraping.follow_redirects,
                'max_jobs_per_search': self.scraping.max_jobs_per_search
            },
            'dashboard': {
                'page_title': self.dashboard.page_title,
                'theme': self.dashboard.theme,
                'cache_ttl': self.dashboard.cache_ttl,
                'max_display_jobs': self.dashboard.max_display_jobs,
                'items_per_page': self.dashboard.items_per_page,
                'enable_analytics': self.dashboard.enable_analytics,
                'enable_export': self.dashboard.enable_export
            },
            'logging': {
                'level': self.logging.level,
                'format': self.logging.format,
                'file_path': self.logging.file_path,
                'max_file_size': self.logging.max_file_size,
                'backup_count': self.logging.backup_count,
                'enable_console': self.logging.enable_console,
                'enable_file': self.logging.enable_file
            },
            'security': {
                'enable_rate_limiting': self.security.enable_rate_limiting,
                'max_requests_per_minute': self.security.max_requests_per_minute,
                'max_requests_per_hour': self.security.max_requests_per_hour,
                'enable_cors': self.security.enable_cors,
                'allowed_origins': self.security.allowed_origins,
                'enable_https': self.security.enable_https,
                'secret_key': self.security.secret_key
            },
            'app_name': self.app_name,
            'app_version': self.app_version,
            'debug': self.debug,
            'environment': self.environment
        }
    
    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration."""
        return self.database
    
    def get_scraping_config(self) -> ScrapingConfig:
        """Get scraping configuration."""
        return self.scraping
    
    def get_dashboard_config(self) -> DashboardConfig:
        """Get dashboard configuration."""
        return self.dashboard
    
    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self.logging
    
    def get_security_config(self) -> SecurityConfig:
        """Get security configuration."""
        return self.security
    
    def update_database_config(self, **kwargs):
        """Update database configuration."""
        for key, value in kwargs.items():
            if hasattr(self.database, key):
                setattr(self.database, key, value)
        logger.info("Database configuration updated")
    
    def update_scraping_config(self, **kwargs):
        """Update scraping configuration."""
        for key, value in kwargs.items():
            if hasattr(self.scraping, key):
                setattr(self.scraping, key, value)
        logger.info("Scraping configuration updated")
    
    def update_dashboard_config(self, **kwargs):
        """Update dashboard configuration."""
        for key, value in kwargs.items():
            if hasattr(self.dashboard, key):
                setattr(self.dashboard, key, value)
        logger.info("Dashboard configuration updated")
    
    def update_logging_config(self, **kwargs):
        """Update logging configuration."""
        for key, value in kwargs.items():
            if hasattr(self.logging, key):
                setattr(self.logging, key, value)
        logger.info("Logging configuration updated")
    
    def update_security_config(self, **kwargs):
        """Update security configuration."""
        for key, value in kwargs.items():
            if hasattr(self.security, key):
                setattr(self.security, key, value)
        logger.info("Security configuration updated")

class ConfigManager:
    """
    Configuration manager for handling multiple configuration sources.
    """
    
    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = Config()
        self.load_config()
        
        logger.info("ConfigManager initialized")
    
    def load_config(self) -> bool:
        """Load configuration from file and environment."""
        try:
            # Load from file if it exists
            if os.path.exists(self.config_file):
                file_format = ConfigFormat.YAML
                if self.config_file.endswith('.json'):
                    file_format = ConfigFormat.JSON
                elif self.config_file.endswith('.toml'):
                    file_format = ConfigFormat.TOML
                
                success = self.config.load_from_file(self.config_file, file_format)
                if not success:
                    logger.warning("Failed to load configuration from file, using defaults")
            
            # Environment variables are loaded in __post_init__
            logger.info("Configuration loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            return False
    
    def save_config(self) -> bool:
        """Save current configuration to file."""
        try:
            file_format = ConfigFormat.YAML
            if self.config_file.endswith('.json'):
                file_format = ConfigFormat.JSON
            elif self.config_file.endswith('.toml'):
                file_format = ConfigFormat.TOML
            
            return self.config.save_to_file(self.config_file, file_format)
            
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            return False
    
    def get_config(self) -> Config:
        """Get current configuration."""
        return self.config
    
    def reload_config(self) -> bool:
        """Reload configuration from file and environment."""
        self.config = Config()
        return self.load_config()

# Global configuration instance
config_manager = ConfigManager()

def get_config() -> Config:
    """Get global configuration instance."""
    return config_manager.get_config()

def reload_config() -> bool:
    """Reload global configuration."""
    return config_manager.reload_config()

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    config = Config()
    
    # Load from file
    config.load_from_file("config.yaml")
    
    # Update settings
    config.update_database_config(
        persist_directory="./custom_db",
        max_results=2000
    )
    
    # Save configuration
    config.save_to_file("custom_config.yaml")
    
    # Print configuration
    print("Database config:", config.get_database_config())
    print("Scraping config:", config.get_scraping_config())
    
    # Test configuration manager
    manager = ConfigManager("test_config.yaml")
    test_config = manager.get_config()
    print("Test config loaded:", test_config.app_name)
