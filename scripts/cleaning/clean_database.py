"""
Database cleaning script to clean all data in companies, companies_metadata, contacts, and contacts_metadata tables.

Cleaning rules:
- Company names: Use comprehensive cleaning with validation (preserves legitimate special chars)
- Other text fields: Remove special characters (keep only alphanumeric, spaces, hyphens, periods)
- Convert placeholder values ("_" and "") to NULL
- Clean array field elements (industries, keywords, technologies, departments)
"""

import re
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from ..config import get_default
from ..models import Company, CompanyMetadata, Contact, ContactMetadata, SessionLocal
from ..utils.cleaning import clean_company_name
from ..utils.cleaning import clean_keyword_array
from ..utils.cleaning import clean_title
from ..utils import log_error

# PostgreSQL Connection Configuration
POSTGRES_USER = get_default("postgres.user")
POSTGRES_PASS = get_default("postgres.password")
POSTGRES_HOST = get_default("postgres.host")
POSTGRES_PORT = get_default("postgres.port")
POSTGRES_DB = get_default("postgres.database")


def log_clean_error(row_id: Any, table_name: str, error_reason: str, error_type: str = "cleaning_error") -> None:
    """
    Log cleaning errors via the centralized error logger.

    Cleaning errors are recorded in the shared timestamped error CSV alongside
    ingestion and analysis errors, with contextual information about the table
    and row that failed to clean.
    """
    row_context = {"table": table_name, "row_id": row_id}
    log_error(row_context, error_reason, error_type=error_type)


def clean_text(value: Optional[str]) -> Optional[str]:
    """
    Clean text value by:
    1. Removing special characters (keep only alphanumeric, spaces, hyphens, periods)
    2. Converting "_" and "" to None (NULL)
    
    Args:
        value: The text value to clean
        
    Returns:
        Cleaned text or None if value is "_" or empty string
    """
    if value is None:
        return None
    
    # Convert to string if not already
    if not isinstance(value, str):
        value = str(value)
    
    # Convert "_" and empty strings to None
    if value == "_" or value == "":
        return None
    
    # Remove special characters, keep only alphanumeric, spaces, hyphens, and periods
    # Pattern: [^a-zA-Z0-9\s\-\.] means "not alphanumeric, space, hyphen, or period"
    cleaned = re.sub(r'[^a-zA-Z0-9\s\-\.]', '', value)
    
    # Strip whitespace
    cleaned = cleaned.strip()
    
    # Return None if result is empty
    if cleaned == "":
        return None
    
    return cleaned


def clean_array(value: Optional[List[str]]) -> Optional[List[str]]:
    """
    Clean array by cleaning each element.
    
    Args:
        value: List of strings to clean
        
    Returns:
        Cleaned list or None if all elements are None/empty
    """
    if value is None:
        return None
    
    if not isinstance(value, list):
        return None
    
    cleaned_list = []
    for item in value:
        cleaned_item = clean_text(item)
        if cleaned_item is not None:
            cleaned_list.append(cleaned_item)
    
    # Return None if list is empty after cleaning
    if len(cleaned_list) == 0:
        return None
    
    return cleaned_list


def clean_companies(batch_size: int = 1000) -> Dict[str, int]:
    """
    Clean all rows in the companies table.
    
    Args:
        batch_size: Number of rows to process per batch
        
    Returns:
        Dictionary with statistics: processed, updated, errors, invalid_names
    """
    stats = {"processed": 0, "updated": 0, "errors": 0, "invalid_names": 0}
    server_time = datetime.now(timezone.utc)
    
    with SessionLocal() as session:
        try:
            # Get total count
            total_count = session.query(Company).count()
            print(f"\n=== Cleaning Companies Table ===")
            print(f"Total rows: {total_count}")
            
            offset = 0
            while offset < total_count:
                # Fetch batch
                batch = session.query(Company).offset(offset).limit(batch_size).all()
                
                if not batch:
                    break
                
                updated_count = 0
                for company in batch:
                    try:
                        stats["processed"] += 1
                        modified = False
                        
                        # Clean company name using specialized function
                        if company.name is not None:
                            original_name = company.name
                            cleaned_name = clean_company_name(company.name)
                            if cleaned_name != original_name:
                                company.name = cleaned_name
                                modified = True
                                # Track if name became invalid (None)
                                if cleaned_name is None:
                                    stats["invalid_names"] += 1
                        
                        if company.address is not None:
                            cleaned_address = clean_text(company.address)
                            if cleaned_address != company.address:
                                company.address = cleaned_address
                                modified = True
                        
                        if company.text_search is not None:
                            cleaned_text_search = clean_text(company.text_search)
                            if cleaned_text_search != company.text_search:
                                company.text_search = cleaned_text_search
                                modified = True
                        
                        # Clean array fields
                        if company.industries is not None:
                            cleaned_industries = clean_array(company.industries)
                            if cleaned_industries != company.industries:
                                company.industries = cleaned_industries
                                modified = True
                        
                        # Use specialized keyword cleaning function
                        if company.keywords is not None:
                            cleaned_keywords = clean_keyword_array(company.keywords)
                            if cleaned_keywords != company.keywords:
                                company.keywords = cleaned_keywords
                                modified = True
                        
                        if company.technologies is not None:
                            cleaned_technologies = clean_array(company.technologies)
                            if cleaned_technologies != company.technologies:
                                company.technologies = cleaned_technologies
                                modified = True
                        
                        # Update timestamp if modified
                        if modified:
                            company.updated_at = server_time
                            updated_count += 1
                            stats["updated"] += 1
                    
                    except Exception as e:
                        stats["errors"] += 1
                        error_msg = f"Error cleaning company id={company.id}: {str(e)}"
                        print(f"  ERROR: {error_msg}")
                        log_clean_error(company.id, "companies", error_msg)
                
                # Commit batch
                try:
                    session.commit()
                    if updated_count > 0:
                        print(f"  Processed {stats['processed']}/{total_count} rows, updated {updated_count} in this batch")
                except Exception as e:
                    session.rollback()
                    stats["errors"] += updated_count
                    print(f"  ERROR committing batch: {str(e)}")
                
                offset += batch_size
            
            print(f"  Completed: {stats['processed']} processed, {stats['updated']} updated, {stats['errors']} errors")
        
        except Exception as e:
            session.rollback()
            error_msg = f"Fatal error in clean_companies: {str(e)}"
            print(f"  FATAL ERROR: {error_msg}")
            log_clean_error("N/A", "companies", error_msg, "fatal_error")
            stats["errors"] += 1
    
    return stats


def clean_companies_metadata(batch_size: int = 1000) -> Dict[str, int]:
    """
    Clean all rows in the companies_metadata table.
    
    Args:
        batch_size: Number of rows to process per batch
        
    Returns:
        Dictionary with statistics: processed, updated, errors
    """
    stats = {"processed": 0, "updated": 0, "errors": 0}
    
    # Note: company_name_for_emails could use clean_company_name, but keeping clean_text
    # for consistency with other metadata fields
    
    with SessionLocal() as session:
        try:
            # Get total count
            total_count = session.query(CompanyMetadata).count()
            print(f"\n=== Cleaning Companies Metadata Table ===")
            print(f"Total rows: {total_count}")
            
            offset = 0
            while offset < total_count:
                # Fetch batch
                batch = session.query(CompanyMetadata).offset(offset).limit(batch_size).all()
                
                if not batch:
                    break
                
                updated_count = 0
                for meta in batch:
                    try:
                        stats["processed"] += 1
                        modified = False
                        
                        # Clean all text fields
                        text_fields = [
                            'linkedin_url', 'facebook_url', 'twitter_url', 'website',
                            'company_name_for_emails', 'phone_number', 'latest_funding',
                            'last_raised_at', 'city', 'state', 'country'
                        ]
                        
                        for field_name in text_fields:
                            current_value = getattr(meta, field_name)
                            if current_value is not None:
                                cleaned_value = clean_text(current_value)
                                if cleaned_value != current_value:
                                    setattr(meta, field_name, cleaned_value)
                                    modified = True
                        
                        if modified:
                            updated_count += 1
                            stats["updated"] += 1
                    
                    except Exception as e:
                        stats["errors"] += 1
                        error_msg = f"Error cleaning company_metadata id={meta.id}: {str(e)}"
                        print(f"  ERROR: {error_msg}")
                        log_clean_error(meta.id, "companies_metadata", error_msg)
                
                # Commit batch
                try:
                    session.commit()
                    if updated_count > 0:
                        print(f"  Processed {stats['processed']}/{total_count} rows, updated {updated_count} in this batch")
                except Exception as e:
                    session.rollback()
                    stats["errors"] += updated_count
                    print(f"  ERROR committing batch: {str(e)}")
                
                offset += batch_size
            
            print(f"  Completed: {stats['processed']} processed, {stats['updated']} updated, {stats['errors']} errors")
        
        except Exception as e:
            session.rollback()
            error_msg = f"Fatal error in clean_companies_metadata: {str(e)}"
            print(f"  FATAL ERROR: {error_msg}")
            log_clean_error("N/A", "companies_metadata", error_msg, "fatal_error")
            stats["errors"] += 1
    
    return stats


def clean_contacts(batch_size: int = 1000) -> Dict[str, int]:
    """
    Clean all rows in the contacts table.
    
    Args:
        batch_size: Number of rows to process per batch
        
    Returns:
        Dictionary with statistics: processed, updated, errors
    """
    stats = {"processed": 0, "updated": 0, "errors": 0}
    server_time = datetime.now(timezone.utc)
    
    with SessionLocal() as session:
        try:
            # Get total count
            total_count = session.query(Contact).count()
            print(f"\n=== Cleaning Contacts Table ===")
            print(f"Total rows: {total_count}")
            
            offset = 0
            while offset < total_count:
                # Fetch batch
                batch = session.query(Contact).offset(offset).limit(batch_size).all()
                
                if not batch:
                    break
                
                updated_count = 0
                for contact in batch:
                    try:
                        stats["processed"] += 1
                        modified = False
                        
                        # Clean text fields
                        # Use specialized cleaning for title field
                        if contact.title is not None:
                            original_title = contact.title
                            cleaned_title = clean_title(contact.title)
                            if cleaned_title != original_title:
                                contact.title = cleaned_title
                                modified = True
                        
                        # Clean other text fields with standard clean_text
                        text_fields = [
                            'first_name', 'last_name', 'email',
                            'mobile_phone', 'email_status', 'text_search', 'seniority'
                        ]
                        
                        for field_name in text_fields:
                            current_value = getattr(contact, field_name)
                            if current_value is not None:
                                cleaned_value = clean_text(current_value)
                                if cleaned_value != current_value:
                                    setattr(contact, field_name, cleaned_value)
                                    modified = True
                        
                        # Clean array fields
                        if contact.departments is not None:
                            cleaned_departments = clean_array(contact.departments)
                            if cleaned_departments != contact.departments:
                                contact.departments = cleaned_departments
                                modified = True
                        
                        # Update timestamp if modified
                        if modified:
                            contact.updated_at = server_time
                            updated_count += 1
                            stats["updated"] += 1
                    
                    except Exception as e:
                        stats["errors"] += 1
                        error_msg = f"Error cleaning contact id={contact.id}: {str(e)}"
                        print(f"  ERROR: {error_msg}")
                        log_clean_error(contact.id, "contacts", error_msg)
                
                # Commit batch
                try:
                    session.commit()
                    if updated_count > 0:
                        print(f"  Processed {stats['processed']}/{total_count} rows, updated {updated_count} in this batch")
                except Exception as e:
                    session.rollback()
                    stats["errors"] += updated_count
                    print(f"  ERROR committing batch: {str(e)}")
                
                offset += batch_size
            
            print(f"  Completed: {stats['processed']} processed, {stats['updated']} updated, {stats['errors']} errors")
        
        except Exception as e:
            session.rollback()
            error_msg = f"Fatal error in clean_contacts: {str(e)}"
            print(f"  FATAL ERROR: {error_msg}")
            log_clean_error("N/A", "contacts", error_msg, "fatal_error")
            stats["errors"] += 1
    
    return stats


def clean_contacts_metadata(batch_size: int = 1000) -> Dict[str, int]:
    """
    Clean all rows in the contacts_metadata table.
    
    Args:
        batch_size: Number of rows to process per batch
        
    Returns:
        Dictionary with statistics: processed, updated, errors
    """
    stats = {"processed": 0, "updated": 0, "errors": 0}
    
    with SessionLocal() as session:
        try:
            # Get total count
            total_count = session.query(ContactMetadata).count()
            print(f"\n=== Cleaning Contacts Metadata Table ===")
            print(f"Total rows: {total_count}")
            
            offset = 0
            while offset < total_count:
                # Fetch batch
                batch = session.query(ContactMetadata).offset(offset).limit(batch_size).all()
                
                if not batch:
                    break
                
                updated_count = 0
                for meta in batch:
                    try:
                        stats["processed"] += 1
                        modified = False
                        
                        # Clean all text fields
                        text_fields = [
                            'linkedin_url', 'facebook_url', 'twitter_url', 'website',
                            'work_direct_phone', 'home_phone', 'city', 'state',
                            'country', 'other_phone', 'stage'
                        ]
                        
                        for field_name in text_fields:
                            current_value = getattr(meta, field_name)
                            if current_value is not None:
                                cleaned_value = clean_text(current_value)
                                if cleaned_value != current_value:
                                    setattr(meta, field_name, cleaned_value)
                                    modified = True
                        
                        if modified:
                            updated_count += 1
                            stats["updated"] += 1
                    
                    except Exception as e:
                        stats["errors"] += 1
                        error_msg = f"Error cleaning contact_metadata id={meta.id}: {str(e)}"
                        print(f"  ERROR: {error_msg}")
                        log_clean_error(meta.id, "contacts_metadata", error_msg)
                
                # Commit batch
                try:
                    session.commit()
                    if updated_count > 0:
                        print(f"  Processed {stats['processed']}/{total_count} rows, updated {updated_count} in this batch")
                except Exception as e:
                    session.rollback()
                    stats["errors"] += updated_count
                    print(f"  ERROR committing batch: {str(e)}")
                
                offset += batch_size
            
            print(f"  Completed: {stats['processed']} processed, {stats['updated']} updated, {stats['errors']} errors")
        
        except Exception as e:
            session.rollback()
            error_msg = f"Fatal error in clean_contacts_metadata: {str(e)}"
            print(f"  FATAL ERROR: {error_msg}")
            log_clean_error("N/A", "contacts_metadata", error_msg, "fatal_error")
            stats["errors"] += 1
    
    return stats


def main():
    """Main entry point for database cleaning."""
    print("=" * 60)
    print("Database Cleaning Script")
    print("=" * 60)
    print(f"Database: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    print(f"Start time: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Get batch size from defaults
    batch_size = get_default("batch_size", 1000)
    print(f"Batch size: {batch_size}")
    
    all_stats = {}
    
    try:
        # Clean all tables
        all_stats["companies"] = clean_companies(batch_size=batch_size)
        all_stats["companies_metadata"] = clean_companies_metadata(batch_size=batch_size)
        all_stats["contacts"] = clean_contacts(batch_size=batch_size)
        all_stats["contacts_metadata"] = clean_contacts_metadata(batch_size=batch_size)
        
        # Print summary
        print("\n" + "=" * 60)
        print("CLEANING SUMMARY")
        print("=" * 60)
        
        total_processed = 0
        total_updated = 0
        total_errors = 0
        total_invalid_names = 0
        
        for table_name, stats in all_stats.items():
            print(f"\n{table_name}:")
            print(f"  Processed: {stats['processed']}")
            print(f"  Updated: {stats['updated']}")
            print(f"  Errors: {stats['errors']}")
            if 'invalid_names' in stats:
                print(f"  Invalid Names (set to NULL): {stats['invalid_names']}")
                total_invalid_names += stats.get('invalid_names', 0)
            total_processed += stats['processed']
            total_updated += stats['updated']
            total_errors += stats['errors']
        
        print("\n" + "-" * 60)
        print(f"TOTALS:")
        print(f"  Processed: {total_processed}")
        print(f"  Updated: {total_updated}")
        print(f"  Errors: {total_errors}")
        if total_invalid_names > 0:
            print(f"  Invalid Company Names (set to NULL): {total_invalid_names}")
        print("=" * 60)
        
        if total_errors > 0:
            print(f"\nWARNING: {total_errors} errors occurred during cleaning.")
            print(f"Check {CLEAN_ERROR_CSV_PATH} for details.")
        else:
            print("\nSUCCESS: All tables cleaned without errors!")
        
        print(f"\nEnd time: {datetime.now().isoformat()}")
        print("=" * 60)
    
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

