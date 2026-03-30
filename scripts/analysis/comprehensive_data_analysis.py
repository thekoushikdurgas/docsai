"""
Comprehensive Data Analysis Script

This script performs deep analysis of company.name, company.keywords, and contact.title fields
in the database to:
1. Identify data quality issues
2. Categorize problematic patterns
3. Validate cleaning logic effectiveness
4. Generate detailed reports

Usage:
    python -m scripts.data.analysis.comprehensive_data_analysis
"""

import os
import csv
import json
from typing import List, Dict, Tuple, Set, Optional
from datetime import datetime
from collections import Counter, defaultdict

from ..config import get_default
from ..models import Company, Contact, SessionLocal
from ..utils.cleaning import (
    clean_company_name, 
    is_valid_company_name,
    clean_company_name_preserve_invalid
)
from ..utils.cleaning import clean_keyword, clean_keyword_array, is_valid_keyword
from ..utils.cleaning import clean_title, is_valid_title
from ..utils import log_error

# PostgreSQL Connection Configuration
POSTGRES_USER = get_default("postgres.user")
POSTGRES_PASS = get_default("postgres.password")
POSTGRES_HOST = get_default("postgres.host")
POSTGRES_PORT = get_default("postgres.port")
POSTGRES_DB = get_default("postgres.database")


def analyze_company_names(batch_size: int = 1000) -> Dict:
    """Analyze company names in the database."""
    print("\n" + "=" * 80)
    print("ANALYZING COMPANY NAMES")
    print("=" * 80)
    
    stats = {
        "total": 0,
        "null_or_empty": 0,
        "valid": 0,
        "invalid": 0,
        "needs_cleaning": 0,
        "invalid_patterns": defaultdict(int),
        "encoding_issues": [],
        "unicode_variants": [],
        "emoji_issues": [],
        "placeholder_examples": [],
        "international_names": 0,
        "special_char_examples": []
    }
    
    with SessionLocal() as session:
        total_count = session.query(Company).count()
        print(f"Total companies: {total_count:,}")
        
        offset = 0
        while offset < total_count:
            companies = session.query(Company.id, Company.name).offset(offset).limit(batch_size).all()
            
            if not companies:
                break
            
            for company_id, name in companies:
                stats["total"] += 1
                
                if name is None or name.strip() == "":
                    stats["null_or_empty"] += 1
                    continue
                
                # Check for international characters
                if any(ord(c) > 127 for c in name):
                    stats["international_names"] += 1
                
                # Try cleaning
                cleaned, is_valid = clean_company_name_preserve_invalid(name)
                
                if is_valid:
                    if cleaned != name:
                        stats["needs_cleaning"] += 1
                        # Categorize cleaning needs
                        if "?" in name:
                            stats["encoding_issues"].append((company_id, name, cleaned))
                        if any(ord(c) > 127 and c not in name for c in cleaned or ""):
                            stats["unicode_variants"].append((company_id, name, cleaned))
                        if any(c in name for c in ["👋", "☘️", "🔗", "✨"]):
                            stats["emoji_issues"].append((company_id, name, cleaned))
                    else:
                        stats["valid"] += 1
                else:
                    stats["invalid"] += 1
                    # Categorize invalid patterns
                    if name.strip() in ["_", "__", "___"]:
                        stats["invalid_patterns"]["underscores"] += 1
                        if len(stats["placeholder_examples"]) < 10:
                            stats["placeholder_examples"].append((company_id, name))
                    elif name.strip() in [".", "..", "..."]:
                        stats["invalid_patterns"]["dots"] += 1
                        if len(stats["placeholder_examples"]) < 10:
                            stats["placeholder_examples"].append((company_id, name))
                    elif name.strip() in ["?", "??", "???"]:
                        stats["invalid_patterns"]["question_marks"] += 1
                        if len(stats["encoding_issues"]) < 10:
                            stats["encoding_issues"].append((company_id, name, None))
                    elif name.strip() in ["0", "00", "000"]:
                        stats["invalid_patterns"]["zeros"] += 1
                        if len(stats["placeholder_examples"]) < 10:
                            stats["placeholder_examples"].append((company_id, name))
                    else:
                        stats["invalid_patterns"]["other"] += 1
                        if len(stats["placeholder_examples"]) < 10:
                            stats["placeholder_examples"].append((company_id, name))
                
                # Collect examples of special characters
                if any(c in name for c in ["&", "'", "(", ")", "-", ".", "/", ":", ";"]):
                    if len(stats["special_char_examples"]) < 20:
                        stats["special_char_examples"].append((company_id, name))
            
            offset += batch_size
            if offset % 10000 == 0:
                print(f"  Processed {offset:,}/{total_count:,} records...")
    
    return stats


def analyze_keywords(batch_size: int = 1000) -> Dict:
    """Analyze keywords in the database."""
    print("\n" + "=" * 80)
    print("ANALYZING KEYWORDS")
    print("=" * 80)
    
    stats = {
        "total_companies": 0,
        "companies_with_keywords": 0,
        "companies_without_keywords": 0,
        "total_keywords": 0,
        "valid_keywords": 0,
        "invalid_keywords": 0,
        "needs_cleaning": 0,
        "invalid_patterns": defaultdict(int),
        "encoding_issues": [],
        "placeholder_examples": [],
        "keyword_frequency": Counter(),
        "unique_keywords": set()
    }
    
    with SessionLocal() as session:
        total_count = session.query(Company).count()
        print(f"Total companies: {total_count:,}")
        
        offset = 0
        while offset < total_count:
            companies = session.query(Company.id, Company.keywords).offset(offset).limit(batch_size).all()
            
            if not companies:
                break
            
            for company_id, keywords in companies:
                stats["total_companies"] += 1
                
                if keywords is None or len(keywords) == 0:
                    stats["companies_without_keywords"] += 1
                    continue
                
                stats["companies_with_keywords"] += 1
                
                for keyword in keywords:
                    if keyword is None:
                        continue
                    
                    stats["total_keywords"] += 1
                    stats["unique_keywords"].add(keyword.lower().strip())
                    
                    # Check if valid
                    if is_valid_keyword(keyword):
                        cleaned = clean_keyword(keyword)
                        if cleaned != keyword:
                            stats["needs_cleaning"] += 1
                        else:
                            stats["valid_keywords"] += 1
                            stats["keyword_frequency"][keyword.lower().strip()] += 1
                    else:
                        stats["invalid_keywords"] += 1
                        # Categorize
                        if keyword.strip() in ["??", "???", "????"]:
                            stats["invalid_patterns"]["question_marks"] += 1
                            if len(stats["encoding_issues"]) < 10:
                                stats["encoding_issues"].append((company_id, keyword))
                        elif keyword.strip() in ["0", "00", "000"]:
                            stats["invalid_patterns"]["zeros"] += 1
                            if len(stats["placeholder_examples"]) < 10:
                                stats["placeholder_examples"].append((company_id, keyword))
                        elif keyword.strip() in ["_", "__", "___"]:
                            stats["invalid_patterns"]["underscores"] += 1
                            if len(stats["placeholder_examples"]) < 10:
                                stats["placeholder_examples"].append((company_id, keyword))
                        else:
                            stats["invalid_patterns"]["other"] += 1
                            if len(stats["placeholder_examples"]) < 10:
                                stats["placeholder_examples"].append((company_id, keyword))
            
            offset += batch_size
            if offset % 10000 == 0:
                print(f"  Processed {offset:,}/{total_count:,} records...")
    
    return stats


def analyze_titles(batch_size: int = 1000) -> Dict:
    """Analyze contact titles in the database."""
    print("\n" + "=" * 80)
    print("ANALYZING CONTACT TITLES")
    print("=" * 80)
    
    stats = {
        "total_contacts": 0,
        "null_or_empty": 0,
        "valid": 0,
        "invalid": 0,
        "needs_cleaning": 0,
        "invalid_patterns": defaultdict(int),
        "encoding_issues": [],
        "unicode_variants": [],
        "emoji_issues": [],
        "ascii_art_issues": [],
        "placeholder_examples": [],
        "international_titles": 0,
        "title_frequency": Counter()
    }
    
    with SessionLocal() as session:
        total_count = session.query(Contact).count()
        print(f"Total contacts: {total_count:,}")
        
        offset = 0
        while offset < total_count:
            contacts = session.query(Contact.id, Contact.title).offset(offset).limit(batch_size).all()
            
            if not contacts:
                break
            
            for contact_id, title in contacts:
                stats["total_contacts"] += 1
                
                if title is None or title.strip() == "":
                    stats["null_or_empty"] += 1
                    continue
                
                # Check for international characters
                if any(ord(c) > 127 for c in title):
                    stats["international_titles"] += 1
                
                # Track frequency
                stats["title_frequency"][title.lower().strip()] += 1
                
                # Try cleaning
                cleaned = clean_title(title)
                
                if cleaned is None:
                    stats["invalid"] += 1
                    # Categorize
                    if title.strip() in ["0", "00", "000", "0000"]:
                        stats["invalid_patterns"]["zeros"] += 1
                        if len(stats["placeholder_examples"]) < 10:
                            stats["placeholder_examples"].append((contact_id, title))
                    elif "¯\\_" in title or "\\_(ツ)_/" in title or "ᕕ(" in title:
                        stats["invalid_patterns"]["ascii_art"] += 1
                        if len(stats["ascii_art_issues"]) < 10:
                            stats["ascii_art_issues"].append((contact_id, title))
                    elif title.strip() in ["?", "??", "???"]:
                        stats["invalid_patterns"]["question_marks"] += 1
                        if len(stats["encoding_issues"]) < 10:
                            stats["encoding_issues"].append((contact_id, title))
                    else:
                        stats["invalid_patterns"]["other"] += 1
                        if len(stats["placeholder_examples"]) < 10:
                            stats["placeholder_examples"].append((contact_id, title))
                elif cleaned != title:
                    stats["needs_cleaning"] += 1
                    # Categorize cleaning needs
                    if "?" in title:
                        stats["encoding_issues"].append((contact_id, title, cleaned))
                    if any(ord(c) > 127 and c not in title for c in cleaned or ""):
                        stats["unicode_variants"].append((contact_id, title, cleaned))
                    if any(c in title for c in ["👋", "☘️", "🔗", "✨", "🌏"]):
                        stats["emoji_issues"].append((contact_id, title, cleaned))
                else:
                    stats["valid"] += 1
            
            offset += batch_size
            if offset % 10000 == 0:
                print(f"  Processed {offset:,}/{total_count:,} records...")
    
    return stats


def generate_comprehensive_report(
    company_stats: Dict,
    keyword_stats: Dict,
    title_stats: Dict,
    output_dir: str = None
) -> None:
    """Generate comprehensive analysis report."""
    if output_dir is None:
        output_dir = os.path.dirname(__file__)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"comprehensive_data_analysis_{timestamp}.txt")
    json_file = os.path.join(output_dir, f"comprehensive_data_analysis_{timestamp}.json")
    
    # Generate text report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("COMPREHENSIVE DATA QUALITY ANALYSIS REPORT\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 100 + "\n\n")
        
        # Company Names Section
        f.write("=" * 100 + "\n")
        f.write("1. COMPANY NAMES ANALYSIS\n")
        f.write("=" * 100 + "\n\n")
        
        total = company_stats["total"]
        f.write(f"Total Companies:              {total:,}\n")
        f.write(f"  Valid Names:                {company_stats['valid']:,} ({company_stats['valid']/total*100:.1f}%)\n")
        f.write(f"  Invalid Names:               {company_stats['invalid']:,} ({company_stats['invalid']/total*100:.1f}%)\n")
        f.write(f"  Needs Cleaning:             {company_stats['needs_cleaning']:,} ({company_stats['needs_cleaning']/total*100:.1f}%)\n")
        f.write(f"  NULL or Empty:              {company_stats['null_or_empty']:,} ({company_stats['null_or_empty']/total*100:.1f}%)\n")
        f.write(f"  International Names:        {company_stats['international_names']:,} ({company_stats['international_names']/total*100:.1f}%)\n")
        f.write("\n")
        
        f.write("Invalid Patterns:\n")
        for pattern, count in company_stats["invalid_patterns"].items():
            f.write(f"  {pattern}: {count:,}\n")
        f.write("\n")
        
        if company_stats["encoding_issues"]:
            f.write("Encoding Issues (Sample):\n")
            for company_id, name, cleaned in company_stats["encoding_issues"][:10]:
                f.write(f"  ID {company_id}: {repr(name)} -> {repr(cleaned)}\n")
            f.write("\n")
        
        if company_stats["placeholder_examples"]:
            f.write("Placeholder Examples (Sample):\n")
            for company_id, name in company_stats["placeholder_examples"][:10]:
                f.write(f"  ID {company_id}: {repr(name)}\n")
            f.write("\n")
        
        # Keywords Section
        f.write("=" * 100 + "\n")
        f.write("2. KEYWORDS ANALYSIS\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"Total Companies:              {keyword_stats['total_companies']:,}\n")
        f.write(f"  With Keywords:              {keyword_stats['companies_with_keywords']:,} ({keyword_stats['companies_with_keywords']/keyword_stats['total_companies']*100:.1f}%)\n")
        f.write(f"  Without Keywords:           {keyword_stats['companies_without_keywords']:,} ({keyword_stats['companies_without_keywords']/keyword_stats['total_companies']*100:.1f}%)\n")
        f.write(f"Total Keywords:               {keyword_stats['total_keywords']:,}\n")
        f.write(f"  Valid Keywords:             {keyword_stats['valid_keywords']:,} ({keyword_stats['valid_keywords']/keyword_stats['total_keywords']*100:.1f}%)\n")
        f.write(f"  Invalid Keywords:           {keyword_stats['invalid_keywords']:,} ({keyword_stats['invalid_keywords']/keyword_stats['total_keywords']*100:.1f}%)\n")
        f.write(f"  Needs Cleaning:             {keyword_stats['needs_cleaning']:,} ({keyword_stats['needs_cleaning']/keyword_stats['total_keywords']*100:.1f}%)\n")
        f.write(f"Unique Keywords:              {len(keyword_stats['unique_keywords']):,}\n")
        f.write("\n")
        
        f.write("Invalid Patterns:\n")
        for pattern, count in keyword_stats["invalid_patterns"].items():
            f.write(f"  {pattern}: {count:,}\n")
        f.write("\n")
        
        f.write("Top 20 Most Frequent Keywords:\n")
        for keyword, count in keyword_stats["keyword_frequency"].most_common(20):
            f.write(f"  {keyword}: {count:,}\n")
        f.write("\n")
        
        if keyword_stats["encoding_issues"]:
            f.write("Encoding Issues (Sample):\n")
            for company_id, keyword in keyword_stats["encoding_issues"][:10]:
                f.write(f"  Company ID {company_id}: {repr(keyword)}\n")
            f.write("\n")
        
        # Titles Section
        f.write("=" * 100 + "\n")
        f.write("3. CONTACT TITLES ANALYSIS\n")
        f.write("=" * 100 + "\n\n")
        
        total = title_stats["total_contacts"]
        f.write(f"Total Contacts:               {total:,}\n")
        f.write(f"  Valid Titles:                {title_stats['valid']:,} ({title_stats['valid']/total*100:.1f}%)\n")
        f.write(f"  Invalid Titles:               {title_stats['invalid']:,} ({title_stats['invalid']/total*100:.1f}%)\n")
        f.write(f"  Needs Cleaning:             {title_stats['needs_cleaning']:,} ({title_stats['needs_cleaning']/total*100:.1f}%)\n")
        f.write(f"  NULL or Empty:              {title_stats['null_or_empty']:,} ({title_stats['null_or_empty']/total*100:.1f}%)\n")
        f.write(f"  International Titles:        {title_stats['international_titles']:,} ({title_stats['international_titles']/total*100:.1f}%)\n")
        f.write("\n")
        
        f.write("Invalid Patterns:\n")
        for pattern, count in title_stats["invalid_patterns"].items():
            f.write(f"  {pattern}: {count:,}\n")
        f.write("\n")
        
        f.write("Top 20 Most Frequent Titles:\n")
        for title, count in title_stats["title_frequency"].most_common(20):
            f.write(f"  {title}: {count:,}\n")
        f.write("\n")
        
        if title_stats["ascii_art_issues"]:
            f.write("ASCII Art Issues (Sample):\n")
            for contact_id, title in title_stats["ascii_art_issues"][:10]:
                f.write(f"  Contact ID {contact_id}: {repr(title)}\n")
            f.write("\n")
        
        if title_stats["encoding_issues"]:
            f.write("Encoding Issues (Sample):\n")
            for contact_id, title, cleaned in title_stats["encoding_issues"][:10]:
                f.write(f"  Contact ID {contact_id}: {repr(title)} -> {repr(cleaned)}\n")
            f.write("\n")
        
        # Summary
        f.write("=" * 100 + "\n")
        f.write("SUMMARY & RECOMMENDATIONS\n")
        f.write("=" * 100 + "\n\n")
        
        total_issues = (
            company_stats["invalid"] + company_stats["needs_cleaning"] +
            keyword_stats["invalid_keywords"] + keyword_stats["needs_cleaning"] +
            title_stats["invalid"] + title_stats["needs_cleaning"]
        )
        f.write(f"Total Data Quality Issues:     {total_issues:,}\n")
        f.write("\n")
        f.write("Recommendations:\n")
        f.write("1. Run clean_database.py to clean existing data\n")
        f.write("2. Ensure all ingestion scripts use cleaning functions\n")
        f.write("3. Monitor data quality metrics regularly\n")
        f.write("4. Review and update cleaning patterns as needed\n")
    
    # Generate JSON report
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "company_names": {
            "total": company_stats["total"],
            "valid": company_stats["valid"],
            "invalid": company_stats["invalid"],
            "needs_cleaning": company_stats["needs_cleaning"],
            "null_or_empty": company_stats["null_or_empty"],
            "international_names": company_stats["international_names"],
            "invalid_patterns": dict(company_stats["invalid_patterns"])
        },
        "keywords": {
            "total_companies": keyword_stats["total_companies"],
            "companies_with_keywords": keyword_stats["companies_with_keywords"],
            "total_keywords": keyword_stats["total_keywords"],
            "valid_keywords": keyword_stats["valid_keywords"],
            "invalid_keywords": keyword_stats["invalid_keywords"],
            "needs_cleaning": keyword_stats["needs_cleaning"],
            "unique_keywords": len(keyword_stats["unique_keywords"]),
            "invalid_patterns": dict(keyword_stats["invalid_patterns"]),
            "top_keywords": dict(keyword_stats["keyword_frequency"].most_common(50))
        },
        "titles": {
            "total_contacts": title_stats["total_contacts"],
            "valid": title_stats["valid"],
            "invalid": title_stats["invalid"],
            "needs_cleaning": title_stats["needs_cleaning"],
            "null_or_empty": title_stats["null_or_empty"],
            "international_titles": title_stats["international_titles"],
            "invalid_patterns": dict(title_stats["invalid_patterns"]),
            "top_titles": dict(title_stats["title_frequency"].most_common(50))
        }
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nReport saved to: {report_file}")
    print(f"JSON data saved to: {json_file}")


def print_summary(company_stats: Dict, keyword_stats: Dict, title_stats: Dict):
    """Print summary to console."""
    print("\n" + "=" * 100)
    print("ANALYSIS SUMMARY")
    print("=" * 100)
    
    print("\nCOMPANY NAMES:")
    total = company_stats["total"]
    print(f"  Total: {total:,}")
    print(f"  Valid: {company_stats['valid']:,} ({company_stats['valid']/total*100:.1f}%)")
    print(f"  Invalid: {company_stats['invalid']:,} ({company_stats['invalid']/total*100:.1f}%)")
    print(f"  Needs Cleaning: {company_stats['needs_cleaning']:,} ({company_stats['needs_cleaning']/total*100:.1f}%)")
    
    print("\nKEYWORDS:")
    print(f"  Total Keywords: {keyword_stats['total_keywords']:,}")
    print(f"  Valid: {keyword_stats['valid_keywords']:,} ({keyword_stats['valid_keywords']/keyword_stats['total_keywords']*100:.1f}%)")
    print(f"  Invalid: {keyword_stats['invalid_keywords']:,} ({keyword_stats['invalid_keywords']/keyword_stats['total_keywords']*100:.1f}%)")
    print(f"  Needs Cleaning: {keyword_stats['needs_cleaning']:,} ({keyword_stats['needs_cleaning']/keyword_stats['total_keywords']*100:.1f}%)")
    
    print("\nCONTACT TITLES:")
    total = title_stats["total_contacts"]
    print(f"  Total: {total:,}")
    print(f"  Valid: {title_stats['valid']:,} ({title_stats['valid']/total*100:.1f}%)")
    print(f"  Invalid: {title_stats['invalid']:,} ({title_stats['invalid']/total*100:.1f}%)")
    print(f"  Needs Cleaning: {title_stats['needs_cleaning']:,} ({title_stats['needs_cleaning']/total*100:.1f}%)")
    
    print("=" * 100)


def main():
    """Main entry point for comprehensive data analysis."""
    print("=" * 100)
    print("COMPREHENSIVE DATA QUALITY ANALYSIS")
    print("=" * 100)
    print(f"Database: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
    print(f"Start time: {datetime.now().isoformat()}")
    print("=" * 100)
    
    try:
        # Analyze all three fields
        company_stats = analyze_company_names(batch_size=1000)
        keyword_stats = analyze_keywords(batch_size=1000)
        title_stats = analyze_titles(batch_size=1000)
        
        # Generate reports
        generate_comprehensive_report(company_stats, keyword_stats, title_stats)
        
        # Print summary
        print_summary(company_stats, keyword_stats, title_stats)
        
        print(f"\nEnd time: {datetime.now().isoformat()}")
        print("=" * 100)
        
        return 0
    
    except Exception as e:
        print(f"\nFATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        # Log a single high-level analysis error to the centralized error log
        log_error(
            {"script": "comprehensive_data_analysis"},
            error_reason=str(e),
            error_type="analysis_fatal",
        )
        return 1


if __name__ == "__main__":
    exit(main())

