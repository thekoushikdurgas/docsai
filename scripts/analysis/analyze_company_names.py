"""
Analysis script to identify and report invalid company names in the database.

This script queries the database and categorizes company names into:
- Valid names
- Invalid names (should be NULL)
- Names needing cleaning
"""

import os
import csv
from typing import List, Dict, Tuple
from datetime import datetime

from ..config import get_default
from ..models import Company, SessionLocal
from ..utils.cleaning import (
    clean_company_name, 
    is_valid_company_name,
    clean_company_name_preserve_invalid
)
from ..utils import log_error

# PostgreSQL Connection Configuration
POSTGRES_USER = get_default("postgres.user")
POSTGRES_PASS = get_default("postgres.password")
POSTGRES_HOST = get_default("postgres.host")
POSTGRES_PORT = get_default("postgres.port")
POSTGRES_DB = get_default("postgres.database")


def categorize_company_names(batch_size: int = 1000) -> Dict[str, List[Tuple[int, str]]]:
    """
    Categorize all company names in the database.
    
    Returns:
        Dictionary with categories as keys and lists of (id, name) tuples as values
    """
    categories = {
        "valid": [],
        "invalid": [],
        "needs_cleaning": [],
        "null_or_empty": []
    }
    
    with SessionLocal() as session:
        # Get total count
        total_count = session.query(Company).count()
        print(f"Analyzing {total_count} company records...")
        print()
        
        offset = 0
        while offset < total_count:
            # Fetch batch
            companies = session.query(Company.id, Company.name).offset(offset).limit(batch_size).all()
            
            if not companies:
                break
            
            for company_id, company_name in companies:
                if company_name is None or company_name.strip() == "":
                    categories["null_or_empty"].append((company_id, company_name or ""))
                else:
                    # Try cleaning
                    cleaned, is_valid = clean_company_name_preserve_invalid(company_name)
                    
                    if is_valid:
                        if cleaned != company_name:
                            categories["needs_cleaning"].append((company_id, company_name))
                        else:
                            categories["valid"].append((company_id, company_name))
                    else:
                        categories["invalid"].append((company_id, company_name))
            
            offset += batch_size
            if offset % 10000 == 0:
                print(f"  Processed {offset}/{total_count} records...")
    
    return categories


def generate_report(categories: Dict[str, List[Tuple[int, str]]], output_dir: str = None) -> None:
    """
    Generate a detailed report of company name analysis.
    
    Args:
        categories: Dictionary of categorized company names
        output_dir: Directory to save report files (default: script directory)
    """
    if output_dir is None:
        output_dir = os.path.dirname(__file__)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"company_name_analysis_{timestamp}.txt")
    csv_file = os.path.join(output_dir, f"company_name_analysis_{timestamp}.csv")
    
    # Calculate statistics
    total = sum(len(cat) for cat in categories.values())
    valid_count = len(categories["valid"])
    invalid_count = len(categories["invalid"])
    needs_cleaning_count = len(categories["needs_cleaning"])
    null_count = len(categories["null_or_empty"])
    
    # Generate text report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("Company Name Analysis Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Companies:        {total:,}\n")
        f.write(f"Valid Names:            {valid_count:,} ({valid_count/total*100:.1f}%)\n")
        f.write(f"Invalid Names:          {invalid_count:,} ({invalid_count/total*100:.1f}%)\n")
        f.write(f"Needs Cleaning:         {needs_cleaning_count:,} ({needs_cleaning_count/total*100:.1f}%)\n")
        f.write(f"NULL or Empty:          {null_count:,} ({null_count/total*100:.1f}%)\n")
        f.write("\n")
        
        # Invalid names section
        f.write("INVALID NAMES (Should be set to NULL)\n")
        f.write("-" * 80 + "\n")
        if categories["invalid"]:
            f.write(f"Found {len(categories['invalid'])} invalid company names.\n\n")
            f.write("Sample invalid names (first 50):\n")
            for i, (company_id, name) in enumerate(categories["invalid"][:50], 1):
                f.write(f"  {i:3d}. ID {company_id:10d}: {repr(name)}\n")
            if len(categories["invalid"]) > 50:
                f.write(f"  ... and {len(categories['invalid']) - 50} more\n")
        else:
            f.write("No invalid names found.\n")
        f.write("\n")
        
        # Needs cleaning section
        f.write("NAMES NEEDING CLEANING\n")
        f.write("-" * 80 + "\n")
        if categories["needs_cleaning"]:
            f.write(f"Found {len(categories['needs_cleaning'])} names that need cleaning.\n\n")
            f.write("Sample names needing cleaning (first 50):\n")
            for i, (company_id, name) in enumerate(categories["needs_cleaning"][:50], 1):
                cleaned = clean_company_name(name)
                f.write(f"  {i:3d}. ID {company_id:10d}: {repr(name)}\n")
                f.write(f"       -> {repr(cleaned)}\n")
            if len(categories["needs_cleaning"]) > 50:
                f.write(f"  ... and {len(categories['needs_cleaning']) - 50} more\n")
        else:
            f.write("No names need cleaning.\n")
        f.write("\n")
        
        # Valid names sample
        f.write("VALID NAMES (Sample)\n")
        f.write("-" * 80 + "\n")
        if categories["valid"]:
            f.write(f"Found {len(categories['valid'])} valid company names.\n\n")
            f.write("Sample valid names (first 20):\n")
            for i, (company_id, name) in enumerate(categories["valid"][:20], 1):
                f.write(f"  {i:3d}. ID {company_id:10d}: {name}\n")
        else:
            f.write("No valid names found.\n")
        f.write("\n")
    
    # Generate CSV file
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['company_id', 'original_name', 'category', 'cleaned_name'])
        
        for category, items in categories.items():
            for company_id, name in items:
                if category == "needs_cleaning":
                    cleaned = clean_company_name(name)
                    writer.writerow([company_id, name, category, cleaned])
                else:
                    writer.writerow([company_id, name, category, name if category == "valid" else ""])
    
    print(f"\nReport saved to: {report_file}")
    print(f"CSV data saved to: {csv_file}")
    print()
    
    # Print summary to console
    print("=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Total Companies:        {total:,}")
    print(f"Valid Names:            {valid_count:,} ({valid_count/total*100:.1f}%)")
    print(f"Invalid Names:          {invalid_count:,} ({invalid_count/total*100:.1f}%)")
    print(f"Needs Cleaning:         {needs_cleaning_count:,} ({needs_cleaning_count/total*100:.1f}%)")
    print(f"NULL or Empty:          {null_count:,} ({null_count/total*100:.1f}%)")
    print("=" * 80)


def main():
    """Main entry point for company name analysis."""
    print("=" * 80)
    print("Company Name Analysis Script")
    print("=" * 80)
    print(f"Database: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    print(f"Start time: {datetime.now().isoformat()}")
    print("=" * 80)
    print()
    
    try:
        # Categorize company names
        categories = categorize_company_names(batch_size=1000)
        
        # Generate report
        generate_report(categories)
        
        print(f"\nEnd time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        return 0
    
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        # Log a single high-level analysis error to the centralized error log
        log_error(
            {"script": "analyze_company_names"},
            error_reason=str(e),
            error_type="analysis_fatal",
        )
        return 1


if __name__ == "__main__":
    exit(main())

