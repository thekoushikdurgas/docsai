"""
S3 company data ingestion module.

This module handles ingesting company data from S3 CSV objects.
"""

from typing import List, Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from threading import Lock
from uuid import uuid5, NAMESPACE_URL
import boto3

from ..base import S3Ingester
from ...models import Company, CompanyMetadata, SessionLocal
from ...utils.cleaning import clean_company_name
from ...utils.cleaning import clean_keyword_array
from ...utils import log_error
from ...utils.s3_client import get_s3_client, get_s3_bucket_name
from ...config import get_default

# Thread locks for safe concurrent operations
company_insert_lock = Lock()
metadata_insert_lock = Lock()

# Defaults used if not overridden by caller
DEFAULT_BATCH_SIZE = get_default("batch_size", 1000)
DEFAULT_MAX_THREADS = get_default("max_threads", 3)
S3_OBJECT_KEY_COMPANIES = "apollo_sample_5000_cleaned.csv"  # Default object key


class S3CompanyIngester(S3Ingester):
    """Ingester for company data from S3 CSV objects."""
    
    def insert_data(self, data_list: List[Dict]) -> None:
        """Insert company data into the database."""
        if len(data_list) == 0:
            return
        
        company_lst, meta_lst, server_time = [], [], datetime.now(timezone.utc)
        for data in data_list:
            try:
                # Get raw company name and clean it
                raw_company_name = data.get('company')
                company_name = clean_company_name(raw_company_name) if raw_company_name else None
                
                # Use original name for UUID generation to maintain consistency across imports
                # but store the cleaned name in the database
                linkedin_url = data.get('company_linkedin_url') or "_"
                company_name_for_emails = data.get('company_name_for_emails') or "_"
                company_address = data.get('company_address') or "_"
                company_city = data.get('company_city') or "_"
                company_state = data.get('company_state') or "_"
                company_country = data.get('company_country') or "_"
                
                uuid_company_name = raw_company_name if raw_company_name else "_"
                hash_str = uuid_company_name + linkedin_url + company_name_for_emails
                company_uuid = str(uuid5(NAMESPACE_URL, hash_str))

                industry_list = [industry.strip() for industry in data.get('industry', "").split(",")]
                # Clean keywords using specialized function
                raw_keywords = [keyword.strip() for keyword in data.get('keywords', "").split(",") if keyword.strip()]
                keywords_list = clean_keyword_array(raw_keywords) or []
                technologies_list = [technology.strip() for technology in data.get('technologies', "").split(",")]
                    
                company = {
                    "uuid": company_uuid,
                    "name": company_name,
                    "employees_count": int(float(data.get('employees') or 0)),
                    "industries": industry_list,
                    "keywords": keywords_list,
                    "address": company_address,
                    "annual_revenue": int(float(data.get('annual_revenue') or 0)),
                    "total_funding": int(float(data.get('total_funding') or 0)),
                    "technologies": technologies_list,
                    "text_search": company_address + ' ' + company_city + ' ' + company_state + ' ' + company_country,
                    "created_at": server_time,
                    "updated_at": server_time,
                }
                company_lst.append(company)
                
                company_metadata = {
                    "uuid": str(company_uuid),
                    "linkedin_url": linkedin_url,
                    "facebook_url": data.get('facebook_url') or "_",
                    "twitter_url": data.get('twitter_url') or "_",
                    "website": data.get('website') or "_",
                    "company_name_for_emails": company_name_for_emails,
                    "phone_number": data.get('company_phone') or "_",
                    "last_raised_at": data.get('last_raised_at') or "_",
                    "latest_funding": data.get('latest_funding') or "_",
                    "latest_funding_amount": int(float(data.get('Latest_funding_amount', 0) or 0)),
                    "city": company_city,
                    "state": company_state,
                    "country": company_country,
                }
                meta_lst.append(company_metadata)
            except Exception as e:
                error_msg = str(e)
                print(f"Error processing company row: {error_msg}")
                log_error(data, error_msg, "company")
                continue  # Continue processing other rows
        
        with SessionLocal() as session:
            try:
                if company_lst:
                    stmt = insert(Company).on_conflict_do_nothing(index_elements=['uuid'])
                    with company_insert_lock:
                        session.execute(stmt, company_lst)
                
                if meta_lst:
                    stmt = insert(CompanyMetadata).on_conflict_do_nothing(index_elements=['uuid'])
                    with metadata_insert_lock:
                        session.execute(stmt, meta_lst)
                session.commit()
            except Exception as e:
                session.rollback()
                error_msg = f"Database insert error: {str(e)}"
                print(error_msg)
                # Log all rows that failed to insert
                for data in data_list:
                    log_error(data, error_msg, "company_db")


def ingest_companies_from_s3(
    batch_size: int = DEFAULT_BATCH_SIZE,
    max_threads: int = DEFAULT_MAX_THREADS,
    object_key: Optional[str] = None
) -> None:
    """
    Ingest company data from an S3 CSV object.
    
    Args:
        batch_size: Number of rows to process per batch
        max_threads: Maximum number of concurrent threads
        object_key: S3 object key (path to CSV file). If None, uses default.
    """
    key_to_use = object_key or S3_OBJECT_KEY_COMPANIES
    s3_client = get_s3_client()
    bucket_name = get_s3_bucket_name()
    
    ingester = S3CompanyIngester(
        s3_client=s3_client,
        bucket_name=bucket_name,
        object_key=key_to_use,
        batch_size=batch_size,
        max_threads=max_threads
    )
    ingester.ingest()


if __name__ == "__main__":
    ingest_companies_from_s3()

