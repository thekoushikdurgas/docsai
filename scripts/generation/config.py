"""
Configuration management for synthetic data generation.

This module provides configuration loading and validation for the generator.
"""

from dataclasses import dataclass
from typing import Optional

from ..config import get_default, get_all_defaults


@dataclass
class GeneratorConfig:
    """Configuration for synthetic data generation."""
    
    # Generation parameters
    total_companies: int
    contacts_per_company: int
    batch_size: int
    
    # Concurrency settings
    num_generator_processes: int
    num_pg_threads: int
    num_es_threads: int
    queue_buffer_size: int
    
    # PostgreSQL settings (from main config)
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_database: str
    
    # Elasticsearch settings
    es_host: str
    es_port: int
    es_username: str
    es_password: str
    es_companies_index: str
    es_contacts_index: str
    
    @property
    def total_contacts(self) -> int:
        """Calculate total contacts to generate."""
        return self.total_companies * self.contacts_per_company
    
    @property
    def total_batches(self) -> int:
        """Calculate total batches to generate."""
        return self.total_companies // self.batch_size
    
    def validate(self) -> None:
        """Validate configuration values."""
        if self.total_companies <= 0:
            raise ValueError("total_companies must be > 0")
        if self.contacts_per_company <= 0:
            raise ValueError("contacts_per_company must be > 0")
        if self.batch_size <= 0:
            raise ValueError("batch_size must be > 0")
        if self.num_generator_processes <= 0:
            raise ValueError("num_generator_processes must be > 0")
        if self.num_pg_threads <= 0:
            raise ValueError("num_pg_threads must be > 0")
        if self.num_es_threads <= 0:
            raise ValueError("num_es_threads must be > 0")
        if not self.es_host:
            raise ValueError("es_host must be set")
        if self.es_port <= 0:
            raise ValueError("es_port must be > 0")


def load_generator_config() -> GeneratorConfig:
    """
    Load generator configuration from config.json.
    
    Returns:
        GeneratorConfig instance with loaded values
    """
    defaults = get_all_defaults()
    generation_config = defaults.get("generation", {})
    
    # Get PostgreSQL settings from main config
    postgres_config = defaults.get("postgres", {})
    
    # Get Elasticsearch settings
    es_config = generation_config.get("elasticsearch", {})
    
    config = GeneratorConfig(
        # Generation parameters
        total_companies=generation_config.get("total_companies", 1_000_000),
        contacts_per_company=generation_config.get("contacts_per_company", 5),
        batch_size=generation_config.get("batch_size", 1000),
        
        # Concurrency settings
        num_generator_processes=generation_config.get("num_generator_processes", 4),
        num_pg_threads=generation_config.get("num_pg_threads", 8),
        num_es_threads=generation_config.get("num_es_threads", 6),
        queue_buffer_size=generation_config.get("queue_buffer_size", 1000),
        
        # PostgreSQL settings
        postgres_user=postgres_config.get("user", "postgres"),
        postgres_password=postgres_config.get("password", ""),
        postgres_host=postgres_config.get("host", "localhost"),
        postgres_port=postgres_config.get("port", 5432),
        postgres_database=postgres_config.get("database", "postgres"),
        
        # Elasticsearch settings
        es_host=es_config.get("host", "localhost"),
        es_port=es_config.get("port", 9200),
        es_username=es_config.get("username", ""),
        es_password=es_config.get("password", ""),
        es_companies_index=es_config.get("companies_index", "companies_index"),
        es_contacts_index=es_config.get("contacts_index", "contacts_index"),
    )
    
    config.validate()
    return config

