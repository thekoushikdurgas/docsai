"""Utility functions module."""
from . import ingest_utils
from .cleaning import (
    clean_company_name,
    clean_keyword,
    clean_keyword_array,
    clean_title,
    is_valid_company_name,
    is_valid_keyword,
    is_valid_title,
)

# Export log_error for backward compatibility
from .ingest_utils import log_error

__all__ = [
    "ingest_utils",
    "clean_company_name",
    "clean_keyword",
    "clean_keyword_array",
    "clean_title",
    "is_valid_company_name",
    "is_valid_keyword",
    "is_valid_title",
    "log_error",
]
