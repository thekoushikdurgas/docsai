"""
Data generation functions for creating synthetic companies and contacts.

This module provides functions to generate realistic company and contact data
using weighted random selection and deterministic UUID generation.
"""

import random
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
from uuid import uuid5, NAMESPACE_URL

from faker import Faker

from .models import CompanyData, ElasticCompanyData, ContactData, ElasticContactData, GeneratedBatch
from . import sample_data as sd

# Initialize Faker
fake = Faker()


def weighted_choice(weights: Dict[str, float]) -> str:
    """Select an item based on probability weights."""
    total = sum(weights.values())
    r = random.uniform(0, total)
    cumulative = 0.0
    
    for key, weight in weights.items():
        cumulative += weight
        if r <= cumulative:
            return key
    
    # Fallback to first key
    return list(weights.keys())[0]


def random_sample(items: List[str], n: int) -> List[str]:
    """Pick N random items from a list without replacement."""
    if n > len(items):
        n = len(items)
    return random.sample(items, n)


def random_int_in_range(min_val: int, max_val: int) -> int:
    """Generate a random integer in the given range (inclusive)."""
    if max_val <= min_val:
        return min_val
    return random.randint(min_val, max_val)


def generate_company_name() -> str:
    """Generate a company name using various patterns."""
    name_type = random.randint(0, 3)
    
    if name_type == 0:  # prefix_suffix
        return random.choice(sd.COMPANY_NAME_PREFIXES) + random.choice(sd.COMPANY_NAME_SUFFIXES)
    elif name_type == 1:  # word_suffix
        return random.choice(sd.COMPANY_NAME_WORDS) + " " + random.choice(sd.COMPANY_NAME_SUFFIXES)
    elif name_type == 2:  # two_words
        return random.choice(sd.COMPANY_NAME_WORDS) + " " + random.choice(sd.COMPANY_NAME_WORDS)
    else:  # single_word
        return random.choice(sd.COMPANY_NAME_WORDS)


def generate_domain_from_name(company_name: str) -> str:
    """Generate a domain name from a company name."""
    domain_name = company_name.lower().replace(" ", "").replace("-", "")
    
    if random.random() < 0.2:
        domain_name += str(random.randint(1, 999))
    
    extension = random.choice(sd.DOMAIN_EXTENSIONS)
    return domain_name + extension


def generate_deterministic_uuid(seed: str) -> str:
    """Generate a deterministic UUID from a seed string (using uuid5 for consistency)."""
    return str(uuid5(NAMESPACE_URL, seed))


def generate_company() -> Tuple[CompanyData, ElasticCompanyData]:
    """Generate a single company record with both PostgreSQL and Elasticsearch formats."""
    country = random.choice(sd.COUNTRIES)
    
    # Select state
    state = ""
    if country in sd.STATES_BY_COUNTRY and sd.STATES_BY_COUNTRY[country]:
        state = random.choice(sd.STATES_BY_COUNTRY[country])
    
    # Select city
    city = ""
    if country in sd.CITIES_BY_COUNTRY and sd.CITIES_BY_COUNTRY[country]:
        city = random.choice(sd.CITIES_BY_COUNTRY[country])
    else:
        city = fake.city()
    
    # Generate company name and related fields
    company_name = generate_company_name()
    domain = generate_domain_from_name(company_name)
    normalized_domain = domain.split(".")[0]
    website = f"https://www.{domain}"
    linkedin_url = f"https://linkedin.com/company/{normalized_domain}-{random.randint(100000, 999999)}"
    
    # Determine company size and funding stage
    company_size = weighted_choice(sd.COMPANY_SIZE_WEIGHTS)
    funding_stage = weighted_choice(sd.FUNDING_STAGE_WEIGHTS)
    
    # Generate employees count based on company size
    emp_range = sd.EMPLOYEE_COUNT_RANGES[company_size]
    employees_count = random_int_in_range(emp_range[0], emp_range[1])
    
    # Generate annual revenue based on company size
    rev_range = sd.ANNUAL_REVENUE_RANGES[company_size]
    annual_revenue = random_int_in_range(rev_range[0], rev_range[1])
    
    # Generate total funding based on funding stage
    fund_range = sd.TOTAL_FUNDING_RANGES[funding_stage]
    total_funding = 0
    if fund_range[1] > 0:
        total_funding = random_int_in_range(fund_range[0], fund_range[1])
    
    # Generate arrays
    num_industries = random.randint(1, 3)
    industries = random_sample(sd.INDUSTRIES, num_industries)
    
    num_keywords = random.randint(2, 6)
    keywords = random_sample(sd.KEYWORDS, num_keywords)
    
    num_technologies = random.randint(3, 11)
    technologies = random_sample(sd.TECHNOLOGIES, num_technologies)
    
    # Generate address
    street = fake.street_name() + " " + fake.street_suffix()
    zip_code = fake.zipcode()
    address = f"{street}, {city}, {state} {zip_code}, {country}"
    
    # Generate created_at date (within last 5 years)
    days_ago = random.randint(0, 1825)
    created_at = datetime.now() - timedelta(days=days_ago)
    
    # Generate deterministic UUID
    uuid_seed = f"{company_name}{normalized_domain}{linkedin_url}"
    company_uuid = generate_deterministic_uuid(uuid_seed)
    
    # Generate extra PG fields
    facebook_url = f"https://facebook.com/{normalized_domain}"
    twitter_url = f"https://twitter.com/{normalized_domain}"
    company_name_for_emails = company_name.lower().replace(" ", "")
    phone_number = fake.phone_number()
    latest_funding = random.choice(sd.FUNDING_STAGES)
    latest_funding_amount = random_int_in_range(100000, 50000000)
    last_raised_at = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
    
    # Create PostgreSQL company
    pg_company = CompanyData(
        uuid=company_uuid,
        name=company_name,
        employees_count=employees_count,
        industries=industries,
        keywords=keywords,
        address=address,
        annual_revenue=annual_revenue,
        total_funding=total_funding,
        technologies=technologies,
        city=city,
        state=state,
        country=country,
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
        created_at=created_at,
        updated_at=datetime.now(),
    )
    
    # Create Elasticsearch company
    es_company = ElasticCompanyData(
        id=company_uuid,
        name=company_name,
        employees_count=employees_count,
        industries=industries,
        keywords=keywords,
        address=address,
        annual_revenue=annual_revenue,
        total_funding=total_funding,
        technologies=technologies,
        city=city,
        state=state,
        country=country,
        linkedin_url=linkedin_url,
        website=website,
        normalized_domain=normalized_domain,
        created_at=created_at,
    )
    
    return pg_company, es_company


def generate_contact(
    pg_company: CompanyData,
    es_company: ElasticCompanyData,
    company_domain: str
) -> Tuple[ContactData, ElasticContactData]:
    """Generate a contact record linked to a company."""
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@{company_domain}"
    
    # Generate departments (1-3 departments per person)
    num_departments = random.randint(1, 3)
    departments = random_sample(sd.DEPARTMENTS, num_departments)
    
    # Generate LinkedIn URL
    linkedin_url = f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random.randint(100000, 999999)}"
    
    # Generate created_at date (within last 5 years)
    days_ago = random.randint(0, 1825)
    created_at = datetime.now() - timedelta(days=days_ago)
    
    # Generate deterministic UUID
    uuid_seed = f"{first_name}{last_name}{email}{linkedin_url}"
    contact_uuid = generate_deterministic_uuid(uuid_seed)
    
    # Generate extra PG fields
    facebook_url = f"https://facebook.com/{first_name.lower()}.{last_name.lower()}"
    twitter_url = f"https://twitter.com/{first_name.lower()}{last_name.lower()}"
    website = f"https://{first_name.lower()}{last_name.lower()}.com"
    work_direct_phone = fake.phone_number()
    home_phone = fake.phone_number()
    other_phone = fake.phone_number()
    stage = random.choice(sd.CONTACT_STAGES)
    
    # Generate contact-specific fields
    title = random.choice(sd.TITLES)
    mobile_phone = fake.phone_number()
    email_status = random.choice(sd.EMAIL_STATUSES)
    seniority = random.choice(sd.SENIORITY_LEVELS)
    
    # Create PostgreSQL contact
    pg_contact = ContactData(
        uuid=contact_uuid,
        first_name=first_name,
        last_name=last_name,
        company_id=pg_company.uuid,
        email=email,
        title=title,
        departments=departments,
        mobile_phone=mobile_phone,
        email_status=email_status,
        seniority=seniority,
        city=pg_company.city,
        state=pg_company.state,
        country=pg_company.country,
        linkedin_url=linkedin_url,
        facebook_url=facebook_url,
        twitter_url=twitter_url,
        website=website,
        work_direct_phone=work_direct_phone,
        home_phone=home_phone,
        other_phone=other_phone,
        stage=stage,
        created_at=created_at,
        updated_at=datetime.now(),
    )
    
    # Create Elasticsearch contact with denormalized company data
    es_contact = ElasticContactData(
        id=contact_uuid,
        first_name=first_name,
        last_name=last_name,
        company_id=es_company.id,
        email=email,
        title=title,
        departments=departments,
        mobile_phone=mobile_phone,
        email_status=email_status,
        seniority=seniority,
        city=es_company.city,
        state=es_company.state,
        country=es_company.country,
        linkedin_url=linkedin_url,
        created_at=created_at,
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


def generate_batch(batch_num: int, batch_size: int, contacts_per_company: int) -> GeneratedBatch:
    """Generate a batch of companies and their contacts."""
    companies = []
    elastic_companies = []
    contacts = []
    elastic_contacts = []
    
    for _ in range(batch_size):
        pg_company, es_company = generate_company()
        companies.append(pg_company)
        elastic_companies.append(es_company)
        
        # Generate contacts for this company
        domain = pg_company.website.replace("https://www.", "")
        for _ in range(contacts_per_company):
            pg_contact, es_contact = generate_contact(pg_company, es_company, domain)
            contacts.append(pg_contact)
            elastic_contacts.append(es_contact)
    
    return GeneratedBatch(
        batch_num=batch_num,
        companies=companies,
        contacts=contacts,
        elastic_companies=elastic_companies,
        elastic_contacts=elastic_contacts,
    )

