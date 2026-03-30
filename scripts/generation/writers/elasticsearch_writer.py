"""
Elasticsearch writer for bulk indexing generated data.

This module provides functionality to bulk index companies and contacts
into Elasticsearch with proper error handling.
"""

import json
from typing import List, Tuple
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from ..models import ElasticCompanyData, ElasticContactData
from .elasticsearch_mappings import COMPANIES_INDEX_MAPPING, CONTACTS_INDEX_MAPPING


class ElasticsearchWriter:
    """Writer for bulk indexing data into Elasticsearch."""
    
    def __init__(self, host: str, port: int, username: str = "", password: str = ""):
        """
        Initialize the Elasticsearch writer.
        
        Args:
            host: Elasticsearch host
            port: Elasticsearch port
            username: Optional username for authentication
            password: Optional password for authentication
        """
        config = {
            'hosts': [f"{host}:{port}"],
        }
        
        if username and password:
            config['basic_auth'] = (username, password)
        
        self.client = Elasticsearch(**config)
        self.companies_index = None
        self.contacts_index = None
    
    def set_indices(self, companies_index: str, contacts_index: str) -> None:
        """Set the index names."""
        self.companies_index = companies_index
        self.contacts_index = contacts_index
    
    def create_indices(self) -> None:
        """Create Elasticsearch indices if they don't exist."""
        if not self.companies_index or not self.contacts_index:
            raise ValueError("Indices must be set before creating them")
        
        # Create companies index
        if not self.client.indices.exists(index=self.companies_index):
            self.client.indices.create(
                index=self.companies_index,
                body=COMPANIES_INDEX_MAPPING
            )
        
        # Create contacts index
        if not self.client.indices.exists(index=self.contacts_index):
            self.client.indices.create(
                index=self.contacts_index,
                body=CONTACTS_INDEX_MAPPING
            )
    
    def bulk_index_companies(self, companies: List[ElasticCompanyData]) -> Tuple[int, int]:
        """
        Bulk index companies into Elasticsearch.
        
        Returns:
            Tuple of (success_count, failed_count)
        """
        if not companies or not self.companies_index:
            return 0, 0
        
        success_count = 0
        failed_count = 0
        
        try:
            def gen_actions():
                for company in companies:
                    doc = {
                        'id': company.id,
                        'name': company.name,
                        'employees_count': company.employees_count,
                        'industries': company.industries,
                        'keywords': company.keywords,
                        'address': company.address,
                        'annual_revenue': company.annual_revenue,
                        'total_funding': company.total_funding,
                        'technologies': company.technologies,
                        'city': company.city,
                        'state': company.state,
                        'country': company.country,
                        'linkedin_url': company.linkedin_url,
                        'website': company.website,
                        'normalized_domain': company.normalized_domain,
                        'created_at': company.created_at.isoformat() if company.created_at else None,
                    }
                    yield {
                        '_index': self.companies_index,
                        '_id': company.id,
                        '_source': doc,
                    }
            
            # Use bulk helper for efficient indexing
            success, failed = bulk(
                self.client,
                gen_actions(),
                raise_on_error=False,
                refresh=False
            )
            
            success_count = success
            failed_count = len(failed) if failed else 0
            
        except Exception as e:
            failed_count = len(companies)
            print(f"Error indexing companies: {e}")
        
        return success_count, failed_count
    
    def bulk_index_contacts(self, contacts: List[ElasticContactData]) -> Tuple[int, int]:
        """
        Bulk index contacts into Elasticsearch.
        
        Returns:
            Tuple of (success_count, failed_count)
        """
        if not contacts or not self.contacts_index:
            return 0, 0
        
        success_count = 0
        failed_count = 0
        
        try:
            def gen_actions():
                for contact in contacts:
                    doc = {
                        'id': contact.id,
                        'first_name': contact.first_name,
                        'last_name': contact.last_name,
                        'company_id': contact.company_id,
                        'email': contact.email,
                        'title': contact.title,
                        'departments': contact.departments,
                        'mobile_phone': contact.mobile_phone,
                        'email_status': contact.email_status,
                        'seniority': contact.seniority,
                        'city': contact.city,
                        'state': contact.state,
                        'country': contact.country,
                        'linkedin_url': contact.linkedin_url,
                        'created_at': contact.created_at.isoformat() if contact.created_at else None,
                        # Denormalized company fields
                        'company_name': contact.company_name,
                        'company_employees_count': contact.company_employees_count,
                        'company_industries': contact.company_industries,
                        'company_keywords': contact.company_keywords,
                        'company_address': contact.company_address,
                        'company_annual_revenue': contact.company_annual_revenue,
                        'company_total_funding': contact.company_total_funding,
                        'company_technologies': contact.company_technologies,
                        'company_city': contact.company_city,
                        'company_state': contact.company_state,
                        'company_country': contact.company_country,
                        'company_linkedin_url': contact.company_linkedin_url,
                        'company_website': contact.company_website,
                        'company_normalized_domain': contact.company_normalized_domain,
                    }
                    yield {
                        '_index': self.contacts_index,
                        '_id': contact.id,
                        '_source': doc,
                    }
            
            # Use bulk helper for efficient indexing
            success, failed = bulk(
                self.client,
                gen_actions(),
                raise_on_error=False,
                refresh=False
            )
            
            success_count = success
            failed_count = len(failed) if failed else 0
            
        except Exception as e:
            failed_count = len(contacts)
            print(f"Error indexing contacts: {e}")
        
        return success_count, failed_count

