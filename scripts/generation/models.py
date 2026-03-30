"""
Data models for synthetic data generation.

This module defines the data structures used for generated companies and contacts.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class CompanyData:
    """Company data structure for PostgreSQL."""
    uuid: str
    name: str
    employees_count: int
    industries: List[str]
    keywords: List[str]
    address: str
    annual_revenue: int
    total_funding: int
    technologies: List[str]
    city: str
    state: str
    country: str
    linkedin_url: str
    website: str
    normalized_domain: str
    # Extra PG fields
    facebook_url: str
    twitter_url: str
    company_name_for_emails: str
    phone_number: str
    latest_funding: str
    latest_funding_amount: int
    last_raised_at: str
    created_at: datetime
    updated_at: datetime


@dataclass
class ElasticCompanyData:
    """Company data structure for Elasticsearch (subset of CompanyData)."""
    id: str  # UUID
    name: str
    employees_count: int
    industries: List[str]
    keywords: List[str]
    address: str
    annual_revenue: int
    total_funding: int
    technologies: List[str]
    city: str
    state: str
    country: str
    linkedin_url: str
    website: str
    normalized_domain: str
    created_at: datetime


@dataclass
class ContactData:
    """Contact data structure for PostgreSQL."""
    uuid: str
    first_name: str
    last_name: str
    company_id: str  # Company UUID
    email: str
    title: str
    departments: List[str]
    mobile_phone: str
    email_status: str
    seniority: str
    city: str
    state: str
    country: str
    linkedin_url: str
    # Extra PG fields
    facebook_url: str
    twitter_url: str
    website: str
    work_direct_phone: str
    home_phone: str
    other_phone: str
    stage: str
    created_at: datetime
    updated_at: datetime


@dataclass
class ElasticContactData:
    """Contact data structure for Elasticsearch with denormalized company data."""
    id: str  # UUID
    first_name: str
    last_name: str
    company_id: str  # Company UUID
    email: str
    title: str
    departments: List[str]
    mobile_phone: str
    email_status: str
    seniority: str
    city: str
    state: str
    country: str
    linkedin_url: str
    created_at: datetime
    # Denormalized company fields
    company_name: str
    company_employees_count: int
    company_industries: List[str]
    company_keywords: List[str]
    company_address: str
    company_annual_revenue: int
    company_total_funding: int
    company_technologies: List[str]
    company_city: str
    company_state: str
    company_country: str
    company_linkedin_url: str
    company_website: str
    company_normalized_domain: str


@dataclass
class GeneratedBatch:
    """Container for a batch of generated companies and contacts."""
    batch_num: int
    companies: List[CompanyData]
    contacts: List[ContactData]
    elastic_companies: List[ElasticCompanyData]
    elastic_contacts: List[ElasticContactData]

