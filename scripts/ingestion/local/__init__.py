"""Local file ingestion module."""
from .company import ingest_companies_from_local
from .contact import ingest_contacts_from_local
from .email_pattern import ingest_email_patterns_from_local

__all__ = [
    "ingest_companies_from_local",
    "ingest_contacts_from_local",
    "ingest_email_patterns_from_local",
]
