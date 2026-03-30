"""
S3 client utility module.

Provides a shared S3 client instance for use across ingestion modules.
"""

import boto3
from ..config import get_default

# S3 Configuration
S3_ACCESS_KEY = get_default("s3.access_key")
S3_SECRET_KEY = get_default("s3.secret_key")
S3_REGION = get_default("s3.region")
S3_BUCKET_NAME = get_default("s3.bucket_name")

# Initialize S3 client
_s3_client = None


def get_s3_client():
    """
    Get or create the S3 client instance.
    
    Returns:
        Boto3 S3 client
    """
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name=S3_REGION
        )
    return _s3_client


def get_s3_bucket_name() -> str:
    """Get the S3 bucket name from config."""
    return S3_BUCKET_NAME

