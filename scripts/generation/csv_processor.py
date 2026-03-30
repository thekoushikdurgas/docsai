"""
CSV processor for converting CSV data to generation format.

This module processes CSV files (like apollo_sample_5000_cleaned.csv) and
converts them to CompanyData and ContactData structures for dual-write processing.
"""

import csv
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from uuid import uuid5, NAMESPACE_URL

from .models import CompanyData, ElasticCompanyData, ContactData, ElasticContactData, GeneratedBatch
from ..utils.cleaning import clean_company_name, clean_keyword_array, clean_title


def generate_deterministic_uuid(seed: str) -> str:
    """Generate a deterministic UUID from a seed string (using uuid5 for consistency)."""
    return str(uuid5(NAMESPACE_URL, seed))


def parse_industry_string(industry_str: str) -> List[str]:
    """Parse industry string into list."""
    if not industry_str:
        return []
    return [i.strip() for i in industry_str.split(",") if i.strip()]


def parse_keywords_string(keywords_str: str) -> List[str]:
    """Parse keywords string into list, with cleaning."""
    if not keywords_str:
        return []
    raw_keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
    return clean_keyword_array(raw_keywords) or []


def parse_technologies_string(tech_str: str) -> List[str]:
    """Parse technologies string into list."""
    if not tech_str:
        return []
    return [t.strip() for t in tech_str.split(",") if t.strip()]


def parse_departments_string(dept_str: str) -> List[str]:
    """Parse departments string into list."""
    if not dept_str:
        return []
    return [d.strip() for d in dept_str.split(",") if d.strip()]


def safe_int(value: any, default: int = 0) -> int:
    """Safely convert value to int."""
    if not value or value == "":
        return default
    try:
        return int(float(str(value)))
    except (ValueError, TypeError):
        return default


def safe_str(value: any, default: str = "") -> str:
    """Safely convert value to string."""
    if value is None:
        return default
    return str(value).strip() if str(value).strip() else default


def extract_domain_from_website(website: str) -> str:
    """Extract normalized domain from website URL."""
    if not website:
        return ""
    # Remove protocol
    domain = website.replace("https://", "").replace("http://", "").replace("www.", "")
    # Get first part before /
    domain = domain.split("/")[0]
    # Remove port if present
    domain = domain.split(":")[0]
    return domain.lower()


def csv_row_to_company_data(row: Dict[str, str], server_time: datetime) -> Tuple[CompanyData, ElasticCompanyData]:
    """Convert a CSV row to company data structures."""
    # Generate company UUID (deterministic)
    company_name = safe_str(row.get('company', ''))
    linkedin_url = safe_str(row.get('company_linkedin_url', ''))
    company_name_for_emails = safe_str(row.get('company_name_for_emails', ''))
    
    uuid_seed = f"{company_name}{linkedin_url}{company_name_for_emails}"
    company_uuid = generate_deterministic_uuid(uuid_seed)
    
    # Clean company name
    cleaned_company_name = clean_company_name(company_name) if company_name else ""
    
    # Parse arrays
    industries = parse_industry_string(safe_str(row.get('industry', '')))
    keywords = parse_keywords_string(safe_str(row.get('keywords', '')))
    technologies = parse_technologies_string(safe_str(row.get('technologies', '')))
    
    # Extract location
    company_city = safe_str(row.get('company_city', ''))
    company_state = safe_str(row.get('company_state', ''))
    company_country = safe_str(row.get('company_country', ''))
    company_address = safe_str(row.get('company_address', ''))
    
    # If company location is missing, use contact location
    if not company_city:
        company_city = safe_str(row.get('city', ''))
    if not company_state:
        company_state = safe_str(row.get('state', ''))
    if not company_country:
        company_country = safe_str(row.get('country', ''))
    
    # Extract website and domain
    website = safe_str(row.get('website', ''))
    normalized_domain = extract_domain_from_website(website)
    if not normalized_domain and company_name:
        # Fallback: generate domain from company name
        normalized_domain = company_name.lower().replace(" ", "").replace("-", "")
    
    # Parse numeric fields
    employees_count = safe_int(row.get('employees', 0))
    annual_revenue = safe_int(row.get('annual_revenue', 0))
    total_funding = safe_int(row.get('total_funding', 0))
    latest_funding_amount = safe_int(row.get('Latest_funding_amount', 0))
    
    # Other fields
    latest_funding = safe_str(row.get('latest_funding', ''))
    last_raised_at = safe_str(row.get('last_raised_at', ''))
    phone_number = safe_str(row.get('company_phone', ''))
    facebook_url = safe_str(row.get('facebook_url', ''))
    twitter_url = safe_str(row.get('twitter_url', ''))
    
    # Create PostgreSQL company
    pg_company = CompanyData(
        uuid=company_uuid,
        name=cleaned_company_name,
        employees_count=employees_count,
        industries=industries,
        keywords=keywords,
        address=company_address,
        annual_revenue=annual_revenue,
        total_funding=total_funding,
        technologies=technologies,
        city=company_city,
        state=company_state,
        country=company_country,
        linkedin_url=linkedin_url,
        website=website,
        normalized_domain=normalized_domain,
        facebook_url=facebook_url,
        twitter_url=twitter_url,
        company_name_for_emails=company_name_for_emails,
        phone_number=phone_number,
        latest_funding=latest_funding,
        latest_funding_amount=latest_funding_amount,
        last_raised_at=last_raised_at,
        created_at=server_time,
        updated_at=server_time,
    )
    
    # Create Elasticsearch company
    es_company = ElasticCompanyData(
        id=company_uuid,
        name=cleaned_company_name,
        employees_count=employees_count,
        industries=industries,
        keywords=keywords,
        address=company_address,
        annual_revenue=annual_revenue,
        total_funding=total_funding,
        technologies=technologies,
        city=company_city,
        state=company_state,
        country=company_country,
        linkedin_url=linkedin_url,
        website=website,
        normalized_domain=normalized_domain,
        created_at=server_time,
    )
    
    return pg_company, es_company


def csv_row_to_contact_data(
    row: Dict[str, str],
    company_uuid: str,
    pg_company: CompanyData,
    es_company: ElasticCompanyData,
    server_time: datetime
) -> Tuple[ContactData, ElasticContactData]:
    """Convert a CSV row to contact data structures."""
    # Generate contact UUID (deterministic)
    first_name = safe_str(row.get('first_name', ''))
    last_name = safe_str(row.get('last_name', ''))
    email = safe_str(row.get('email', ''))
    person_linkedin_url = safe_str(row.get('person_linkedin_url', ''))
    
    uuid_seed = f"{first_name}{last_name}{email}{person_linkedin_url}"
    contact_uuid = generate_deterministic_uuid(uuid_seed)
    
    # Parse arrays
    departments = parse_departments_string(safe_str(row.get('departments', '')))
    
    # Clean title
    raw_title = safe_str(row.get('title', ''))
    cleaned_title = clean_title(raw_title) if raw_title else None
    
    # Extract location (use contact location, fallback to company)
    city = safe_str(row.get('city', '')) or pg_company.city
    state = safe_str(row.get('state', '')) or pg_company.state
    country = safe_str(row.get('country', '')) or pg_company.country
    
    # Other fields
    email_status = safe_str(row.get('email_status', ''))
    seniority = safe_str(row.get('seniority', ''))
    mobile_phone = safe_str(row.get('mobile_phone', ''))
    work_direct_phone = safe_str(row.get('work_direct_phone', ''))
    home_phone = safe_str(row.get('home_phone', ''))
    other_phone = safe_str(row.get('other_phone', ''))
    stage = safe_str(row.get('stage', ''))
    
    # Generate URLs
    website = safe_str(row.get('website', ''))
    facebook_url = f"https://facebook.com/{first_name.lower()}.{last_name.lower()}" if first_name and last_name else ""
    twitter_url = f"https://twitter.com/{first_name.lower()}{last_name.lower()}" if first_name and last_name else ""
    
    # Create PostgreSQL contact
    pg_contact = ContactData(
        uuid=contact_uuid,
        first_name=first_name,
        last_name=last_name,
        company_id=company_uuid,
        email=email,
        title=cleaned_title,
        departments=departments,
        mobile_phone=mobile_phone,
        email_status=email_status,
        seniority=seniority,
        city=city,
        state=state,
        country=country,
        linkedin_url=person_linkedin_url,
        facebook_url=facebook_url,
        twitter_url=twitter_url,
        website=website,
        work_direct_phone=work_direct_phone,
        home_phone=home_phone,
        other_phone=other_phone,
        stage=stage,
        created_at=server_time,
        updated_at=server_time,
    )
    
    # Create Elasticsearch contact with denormalized company data
    es_contact = ElasticContactData(
        id=contact_uuid,
        first_name=first_name,
        last_name=last_name,
        company_id=company_uuid,
        email=email,
        title=cleaned_title or "",
        departments=departments,
        mobile_phone=mobile_phone,
        email_status=email_status,
        seniority=seniority,
        city=city,
        state=state,
        country=country,
        linkedin_url=person_linkedin_url,
        created_at=server_time,
        # Denormalized company fields
        company_name=es_company.name,
        company_employees_count=es_company.employees_count,
        company_industries=es_company.industries,
        company_keywords=es_company.keywords,
        company_address=es_company.address,
        company_annual_revenue=es_company.annual_revenue,
        company_total_funding=es_company.total_funding,
        company_technologies=es_company.technologies,
        company_city=es_company.city,
        company_state=es_company.state,
        company_country=es_company.country,
        company_linkedin_url=es_company.linkedin_url,
        company_website=es_company.website,
        company_normalized_domain=es_company.normalized_domain,
    )
    
    return pg_contact, es_contact


def process_csv_file(csv_path: str, batch_size: int = 1000) -> List[GeneratedBatch]:
    """
    Process a CSV file and convert it to batches of GeneratedBatch.
    
    Args:
        csv_path: Path to the CSV file
        batch_size: Number of companies per batch
        
    Returns:
        List of GeneratedBatch objects
    """
    server_time = datetime.now()
    batches = []
    
    # Track companies by UUID to avoid duplicates
    companies_by_uuid: Dict[str, Tuple[CompanyData, ElasticCompanyData]] = {}
    contacts_by_company: Dict[str, List[Tuple[ContactData, ElasticContactData]]] = {}
    
    print(f"Reading CSV file: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        row_count = 0
        
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
                
            except Exception as e:
                print(f"Error processing row {row_count}: {e}")
                continue
        
        print(f"Processed {row_count} rows")
        print(f"Found {len(companies_by_uuid)} unique companies")
        print(f"Found {sum(len(contacts) for contacts in contacts_by_company.values())} contacts")
    
    # Group into batches
    company_list = list(companies_by_uuid.items())
    batch_num = 0
    
    for i in range(0, len(company_list), batch_size):
        batch_companies = company_list[i:i + batch_size]
        
        pg_companies = []
        es_companies = []
        pg_contacts = []
        es_contacts = []
        
        for company_uuid, (pg_company, es_company) in batch_companies:
            pg_companies.append(pg_company)
            es_companies.append(es_company)
            
            # Add all contacts for this company
            for pg_contact, es_contact in contacts_by_company[company_uuid]:
                pg_contacts.append(pg_contact)
                es_contacts.append(es_contact)
        
        batch = GeneratedBatch(
            batch_num=batch_num,
            companies=pg_companies,
            contacts=pg_contacts,
            elastic_companies=es_companies,
            elastic_contacts=es_contacts,
        )
        batches.append(batch)
        batch_num += 1
    
    print(f"Created {len(batches)} batches")
    return batches

