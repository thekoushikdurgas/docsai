"""Data ingestion module."""
from .local import (
    ingest_companies_from_local,
    ingest_contacts_from_local,
)
from .s3 import (
    ingest_companies_from_s3,
    ingest_contacts_from_s3,
)

__all__ = [
    "ingest_companies_from_local",
    "ingest_contacts_from_local",
    "ingest_companies_from_s3",
    "ingest_contacts_from_s3",
]
