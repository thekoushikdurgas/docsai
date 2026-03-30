"""
Shared database models and connection setup.

This module provides the SQLAlchemy ORM models and database connection
configuration used across all data ingestion, analysis, and cleaning modules.
"""

from sqlalchemy import create_engine, ARRAY, Column, BigInteger, Text, DateTime, Boolean, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import get_default

# PostgreSQL Connection Configuration
POSTGRES_USER = get_default("postgres.user")
POSTGRES_PASS = get_default("postgres.password")
POSTGRES_HOST = get_default("postgres.host")
POSTGRES_PORT = get_default("postgres.port")
POSTGRES_DB = get_default("postgres.database")

# Create database connection
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(
    DATABASE_URL,
    pool_size=50,
    max_overflow=100,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Company(Base):
    """Company model."""
    __tablename__ = "companies"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Text)
    name = Column(Text)
    employees_count = Column(BigInteger)
    industries = Column(ARRAY(Text))
    keywords = Column(ARRAY(Text))
    address = Column(Text)
    annual_revenue = Column(BigInteger)
    total_funding = Column(BigInteger)
    technologies = Column(ARRAY(Text))
    text_search = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CompanyMetadata(Base):
    """Company metadata model."""
    __tablename__ = "companies_metadata"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Text)
    linkedin_url = Column(Text)
    linkedin_sales_url = Column(Text)
    facebook_url = Column(Text)
    twitter_url = Column(Text)
    website = Column(Text)
    company_name_for_emails = Column(Text)
    phone_number = Column(Text)
    latest_funding = Column(Text)
    latest_funding_amount = Column(BigInteger)
    last_raised_at = Column(Text)
    city = Column(Text)
    state = Column(Text)
    country = Column(Text)


class Contact(Base):
    """Contact model."""
    __tablename__ = "contacts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    company_id = Column(Text)
    email = Column(Text)
    title = Column(Text)
    departments = Column(ARRAY(Text))
    mobile_phone = Column(Text)
    email_status = Column(Text)
    text_search = Column(Text)
    seniority = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ContactMetadata(Base):
    """Contact metadata model."""
    __tablename__ = "contacts_metadata"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Text)
    linkedin_url = Column(Text)
    linkedin_sales_url = Column(Text)
    facebook_url = Column(Text)
    twitter_url = Column(Text)
    website = Column(Text)
    work_direct_phone = Column(Text)
    home_phone = Column(Text)
    city = Column(Text)
    state = Column(Text)
    country = Column(Text)
    other_phone = Column(Text)
    stage = Column(Text)


class EmailPattern(Base):
    """Email pattern model."""
    __tablename__ = "email_patterns"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(Text)
    company_uuid = Column(Text)
    pattern_format = Column(Text)
    pattern_string = Column(Text)
    contact_count = Column(Integer)
    is_auto_extracted = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

