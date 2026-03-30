"""
PostgreSQL writer for bulk inserting generated data.

This module provides functionality to bulk insert companies and contacts
into PostgreSQL with proper error handling and conflict resolution.
"""

from typing import List, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..models import CompanyData, ContactData
from ...models.database import SessionLocal, engine

# Note: Using connection.execute() with a list of dicts performs executemany automatically


class PostgresWriter:
    """Writer for bulk inserting data into PostgreSQL."""
    
    def __init__(self):
        """Initialize the PostgreSQL writer."""
        self.session: Session = SessionLocal()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close session."""
        self.close()
    
    def close(self) -> None:
        """Close the database session."""
        if self.session:
            self.session.close()
    
    def bulk_insert_companies(self, companies: List[CompanyData]) -> Tuple[int, int]:
        """
        Bulk insert companies into PostgreSQL.
        
        Returns:
            Tuple of (success_count, failed_count)
        """
        if not companies:
            return 0, 0
        
        success_count = 0
        failed_count = 0
        
        try:
            # Insert into companies table
            companies_values = []
            for company in companies:
                companies_values.append({
                    'uuid': company.uuid,
                    'name': company.name,
                    'employees_count': company.employees_count,
                    'industries': company.industries,
                    'keywords': company.keywords,
                    'address': company.address,
                    'annual_revenue': company.annual_revenue,
                    'total_funding': company.total_funding,
                    'technologies': company.technologies,
                    'text_search': None,  # Can be computed later
                    'created_at': company.created_at,
                    'updated_at': company.updated_at,
                })
            
            # Insert into companies_metadata table
            metadata_values = []
            for company in companies:
                metadata_values.append({
                    'uuid': company.uuid,
                    'linkedin_url': company.linkedin_url,
                    'linkedin_sales_url': None,
                    'facebook_url': company.facebook_url,
                    'twitter_url': company.twitter_url,
                    'website': company.website,
                    'company_name_for_emails': company.company_name_for_emails,
                    'phone_number': company.phone_number,
                    'latest_funding': company.latest_funding,
                    'latest_funding_amount': company.latest_funding_amount,
                    'last_raised_at': company.last_raised_at,
                    'city': company.city,
                    'state': company.state,
                    'country': company.country,
                })
            
            # Bulk insert companies using executemany
            if companies_values:
                stmt = text("""
                    INSERT INTO companies (
                        uuid, name, employees_count, industries, keywords, address,
                        annual_revenue, total_funding, technologies, text_search,
                        created_at, updated_at
                    )
                    VALUES (
                        :uuid, :name, :employees_count, :industries, :keywords, :address,
                        :annual_revenue, :total_funding, :technologies, :text_search,
                        :created_at, :updated_at
                    )
                    ON CONFLICT (uuid) DO NOTHING
                """)
                
                # Use connection directly for executemany
                conn = self.session.connection()
                conn.execute(stmt, companies_values)
            
            # Bulk insert metadata using executemany
            if metadata_values:
                stmt = text("""
                    INSERT INTO companies_metadata (
                        uuid, linkedin_url, linkedin_sales_url, facebook_url, twitter_url,
                        website, company_name_for_emails, phone_number, latest_funding,
                        latest_funding_amount, last_raised_at, city, state, country
                    )
                    VALUES (
                        :uuid, :linkedin_url, :linkedin_sales_url, :facebook_url, :twitter_url,
                        :website, :company_name_for_emails, :phone_number, :latest_funding,
                        :latest_funding_amount, :last_raised_at, :city, :state, :country
                    )
                    ON CONFLICT (uuid) DO NOTHING
                """)
                
                # Use connection directly for executemany
                conn = self.session.connection()
                conn.execute(stmt, metadata_values)
            
            self.session.commit()
            success_count = len(companies)
            
        except Exception as e:
            self.session.rollback()
            failed_count = len(companies)
            # Log error but continue
            print(f"Error inserting companies: {e}")
        
        return success_count, failed_count
    
    def bulk_insert_contacts(self, contacts: List[ContactData]) -> Tuple[int, int]:
        """
        Bulk insert contacts into PostgreSQL.
        
        Returns:
            Tuple of (success_count, failed_count)
        """
        if not contacts:
            return 0, 0
        
        success_count = 0
        failed_count = 0
        
        try:
            # Insert into contacts table
            contacts_values = []
            for contact in contacts:
                contacts_values.append({
                    'uuid': contact.uuid,
                    'first_name': contact.first_name,
                    'last_name': contact.last_name,
                    'company_id': contact.company_id,
                    'email': contact.email,
                    'title': contact.title,
                    'departments': contact.departments,
                    'mobile_phone': contact.mobile_phone,
                    'email_status': contact.email_status,
                    'text_search': None,  # Can be computed later
                    'seniority': contact.seniority,
                    'created_at': contact.created_at,
                    'updated_at': contact.updated_at,
                })
            
            # Insert into contacts_metadata table
            metadata_values = []
            for contact in contacts:
                metadata_values.append({
                    'uuid': contact.uuid,
                    'linkedin_url': contact.linkedin_url,
                    'linkedin_sales_url': None,
                    'facebook_url': contact.facebook_url,
                    'twitter_url': contact.twitter_url,
                    'website': contact.website,
                    'work_direct_phone': contact.work_direct_phone,
                    'home_phone': contact.home_phone,
                    'city': contact.city,
                    'state': contact.state,
                    'country': contact.country,
                    'other_phone': contact.other_phone,
                    'stage': contact.stage,
                })
            
            # Bulk insert contacts using executemany
            if contacts_values:
                stmt = text("""
                    INSERT INTO contacts (
                        uuid, first_name, last_name, company_id, email, title,
                        departments, mobile_phone, email_status, text_search,
                        seniority, created_at, updated_at
                    )
                    VALUES (
                        :uuid, :first_name, :last_name, :company_id, :email, :title,
                        :departments, :mobile_phone, :email_status, :text_search,
                        :seniority, :created_at, :updated_at
                    )
                    ON CONFLICT (uuid) DO NOTHING
                """)
                
                # Use connection directly for executemany
                conn = self.session.connection()
                conn.execute(stmt, contacts_values)
            
            # Bulk insert metadata using executemany
            if metadata_values:
                stmt = text("""
                    INSERT INTO contacts_metadata (
                        uuid, linkedin_url, linkedin_sales_url, facebook_url, twitter_url,
                        website, work_direct_phone, home_phone, city, state, country,
                        other_phone, stage
                    )
                    VALUES (
                        :uuid, :linkedin_url, :linkedin_sales_url, :facebook_url, :twitter_url,
                        :website, :work_direct_phone, :home_phone, :city, :state, :country,
                        :other_phone, :stage
                    )
                    ON CONFLICT (uuid) DO NOTHING
                """)
                
                # Use connection directly for executemany
                conn = self.session.connection()
                conn.execute(stmt, metadata_values)
            
            self.session.commit()
            success_count = len(contacts)
            
        except Exception as e:
            self.session.rollback()
            failed_count = len(contacts)
            # Log error but continue
            print(f"Error inserting contacts: {e}")
        
        return success_count, failed_count

