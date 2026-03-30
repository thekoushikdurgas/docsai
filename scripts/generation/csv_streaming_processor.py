"""
Streaming CSV processor for large files.

This module processes CSV files incrementally, writing batches as they're created
to avoid loading entire files into memory. Designed for files 4-8GB+ in size.
"""

import csv
from typing import Dict, Generator, Tuple, Optional, Callable
from datetime import datetime
from uuid import uuid5, NAMESPACE_URL

from .models import CompanyData, ElasticCompanyData, ContactData, ElasticContactData, GeneratedBatch
from .csv_processor import (
    csv_row_to_company_data,
    csv_row_to_contact_data,
    safe_str,
    safe_int,
    parse_industry_string,
    parse_keywords_string,
    parse_technologies_string,
    parse_departments_string,
)
from ..utils.cleaning import clean_company_name, clean_keyword_array, clean_title


def process_csv_streaming(
    csv_path: str,
    batch_size: int = 1000,
    progress_callback: Optional[Callable[[int, int, int], None]] = None
) -> Generator[GeneratedBatch, None, None]:
    """
    Process a CSV file in streaming mode, yielding batches as they're created.
    
    This function processes the CSV row-by-row, grouping companies and contacts,
    and yields batches incrementally to avoid loading the entire file into memory.
    
    Args:
        csv_path: Path to the CSV file
        batch_size: Number of companies per batch
        progress_callback: Optional callback function(row_count, companies_count, contacts_count)
        
    Yields:
        GeneratedBatch objects as they're created
    """
    server_time = datetime.now()
    
    # Track companies by UUID to avoid duplicates (only current batch window)
    companies_by_uuid: Dict[str, Tuple[CompanyData, ElasticCompanyData]] = {}
    contacts_by_company: Dict[str, list] = {}
    
    print(f"Reading CSV file: {csv_path}")
    print(f"Processing in streaming mode with batch size: {batch_size}")
    
    row_count = 0
    batch_num = 0
    
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            row_count += 1
            
            try:
                # Extract company data
                pg_company, es_company = csv_row_to_company_data(row, server_time)
                company_uuid = pg_company.uuid
                
                # Store company (will overwrite duplicates, keeping first occurrence)
                if company_uuid not in companies_by_uuid:
                    companies_by_uuid[company_uuid] = (pg_company, es_company)
                    contacts_by_company[company_uuid] = []
                
                # Extract contact data
                pg_contact, es_contact = csv_row_to_contact_data(
                    row, company_uuid, pg_company, es_company, server_time
                )
                
                # Add contact to company's contact list
                contacts_by_company[company_uuid].append((pg_contact, es_contact))
                
                # When we have enough companies, yield a batch
                if len(companies_by_uuid) >= batch_size:
                    batch = _create_batch_from_dicts(
                        companies_by_uuid,
                        contacts_by_company,
                        batch_num
                    )
                    yield batch
                    
                    # Report progress
                    if progress_callback:
                        total_contacts = sum(len(contacts) for contacts in contacts_by_company.values())
                        progress_callback(row_count, len(companies_by_uuid), total_contacts)
                    
                    # Reset for next batch
                    companies_by_uuid.clear()
                    contacts_by_company.clear()
                    batch_num += 1
                
                # Progress reporting every 10k rows
                if row_count % 10000 == 0:
                    print(f"Processed {row_count:,} rows, {len(companies_by_uuid):,} companies in current batch...")
                    
            except Exception as e:
                print(f"Error processing row {row_count}: {e}")
                continue
        
        # Yield final batch if there's remaining data
        if companies_by_uuid:
            batch = _create_batch_from_dicts(
                companies_by_uuid,
                contacts_by_company,
                batch_num
            )
            yield batch
            
            if progress_callback:
                total_contacts = sum(len(contacts) for contacts in contacts_by_company.values())
                progress_callback(row_count, len(companies_by_uuid), total_contacts)
    
    print(f"\nCompleted processing {row_count:,} rows")
    print(f"Created {batch_num + 1} batches")


def _create_batch_from_dicts(
    companies_by_uuid: Dict[str, Tuple[CompanyData, ElasticCompanyData]],
    contacts_by_company: Dict[str, list],
    batch_num: int
) -> GeneratedBatch:
    """Create a GeneratedBatch from company and contact dictionaries."""
    pg_companies = []
    es_companies = []
    pg_contacts = []
    es_contacts = []
    
    for company_uuid, (pg_company, es_company) in companies_by_uuid.items():
        pg_companies.append(pg_company)
        es_companies.append(es_company)
        
        # Add all contacts for this company
        for pg_contact, es_contact in contacts_by_company.get(company_uuid, []):
            pg_contacts.append(pg_contact)
            es_contacts.append(es_contact)
    
    return GeneratedBatch(
        batch_num=batch_num,
        companies=pg_companies,
        contacts=pg_contacts,
        elastic_companies=es_companies,
        elastic_contacts=es_contacts,
    )

