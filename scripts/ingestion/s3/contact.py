"""
S3 contact data ingestion module.

This module handles ingesting contact data from S3 CSV objects.
"""

from typing import List, Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from threading import Lock
from uuid import uuid5, NAMESPACE_URL

from ..base import S3Ingester
from ...models import Contact, ContactMetadata, SessionLocal
from ...utils.cleaning import clean_title
from ...utils import log_error
from ...utils.s3_client import get_s3_client, get_s3_bucket_name
from ...config import get_default

# Thread locks for safe concurrent operations
contact_insert_lock = Lock()
metadata_insert_lock = Lock()

# Defaults used if not overridden by caller
DEFAULT_BATCH_SIZE = get_default("batch_size", 1000)
DEFAULT_MAX_THREADS = get_default("max_threads", 3)
S3_OBJECT_KEY_CONTACTS = "apollo_sample_5000_cleaned.csv"  # Default object key


class S3ContactIngester(S3Ingester):
    """Ingester for contact data from S3 CSV objects."""
    
    def insert_data(self, data_list: List[Dict]) -> None:
        """Insert contact data into the database."""
        if len(data_list) == 0:
            return
        
        contact_lst, meta_lst, server_time = [], [], datetime.now(timezone.utc)
        for data in data_list:
            try:
                company_name = data.get('company') or "_"
                linkedin_url = data.get('company_linkedin_url') or "_"
                company_name_for_emails = data.get('company_name_for_emails') or "_"
                person_linkedin_url = data.get('person_linkedin_url') or "_"
                
                hash_str = company_name + linkedin_url + company_name_for_emails
                company_uuid = str(uuid5(NAMESPACE_URL, hash_str))

                departments = [department.strip() for department in data.get('departments', "").split(",")]
                
                city = data.get('city') or "_"
                state = data.get('state') or "_"
                country = data.get('country') or "_"
                email = data.get('email') or "_"
                data_uuid = str(uuid5(NAMESPACE_URL, person_linkedin_url + email))
                
                # Clean title using specialized function
                raw_title = data.get('title')
                cleaned_title = clean_title(raw_title) if raw_title else None
                    
                contact = {
                    "uuid": data_uuid,
                    "first_name": data.get('first_name') or "_",
                    "last_name": data.get('last_name') or "_",
                    "company_id": company_uuid,
                    "email": data.get('email') or "_",
                    "title": cleaned_title,  # Use cleaned title (can be None if invalid)
                    "departments": departments,
                    "mobile_phone": data.get('mobile_phone') or "_",
                    "email_status": data.get('email_status') or "_",
                    'text_search': city + ' ' + state + ' ' + country,
                    'seniority': data.get('seniority') or "_",
                    "created_at": server_time,
                    "updated_at": server_time,
                }
                contact_lst.append(contact)

                contact_metadata = {
                    "uuid": data_uuid,
                    "linkedin_url": data.get('person_linkedin_url') or "_",
                    "website": data.get('website') or "_",
                    "work_direct_phone": data.get('work_direct_phone') or "_",
                    "home_phone": data.get('home_phone') or "_",
                    "city": data.get('city') or "_",
                    "state": data.get('state') or "_",
                    "country": data.get('country') or "_",
                    "other_phone": data.get('other_phone') or "_",
                    "stage": data.get('stage') or "_",
                }
                meta_lst.append(contact_metadata)
            except Exception as e:
                error_msg = str(e)
                print(f"Error processing contact row: {error_msg}")
                log_error(data, error_msg, "contact")
                continue  # Continue processing other rows
        
        with SessionLocal() as session:
            try:
                if contact_lst:
                    stmt = insert(Contact).on_conflict_do_nothing(index_elements=['uuid'])
                    with contact_insert_lock:
                        session.execute(stmt, contact_lst)
                
                if meta_lst:
                    stmt = insert(ContactMetadata).on_conflict_do_nothing(index_elements=['uuid'])
                    with metadata_insert_lock:
                        session.execute(stmt, meta_lst)
                session.commit()
            except Exception as e:
                session.rollback()
                error_msg = f"Database insert error: {str(e)}"
                print(error_msg)
                # Log all rows that failed to insert
                for data in data_list:
                    log_error(data, error_msg, "contact_db")


def ingest_contacts_from_s3(
    batch_size: int = DEFAULT_BATCH_SIZE,
    max_threads: int = DEFAULT_MAX_THREADS,
    object_key: Optional[str] = None
) -> None:
    """
    Ingest contact data from an S3 CSV object.
    
    Args:
        batch_size: Number of rows to process per batch
        max_threads: Maximum number of concurrent threads
        object_key: S3 object key (path to CSV file). If None, uses default.
    """
    key_to_use = object_key or S3_OBJECT_KEY_CONTACTS
    s3_client = get_s3_client()
    bucket_name = get_s3_bucket_name()
    
    ingester = S3ContactIngester(
        s3_client=s3_client,
        bucket_name=bucket_name,
        object_key=key_to_use,
        batch_size=batch_size,
        max_threads=max_threads
    )
    ingester.ingest()


if __name__ == "__main__":
    ingest_contacts_from_s3()

