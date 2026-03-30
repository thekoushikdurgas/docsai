"""S3 ingestion module."""
from .company import ingest_companies_from_s3
from .contact import ingest_contacts_from_s3

__all__ = [
    "ingest_companies_from_s3",
    "ingest_contacts_from_s3",
]
