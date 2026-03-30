"""
Elasticsearch index mappings for companies and contacts.

This module defines the field mappings for Elasticsearch indices.
"""

COMPANIES_INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "employees_count": {"type": "long"},
            "industries": {"type": "keyword"},
            "keywords": {"type": "keyword"},
            "address": {"type": "text"},
            "annual_revenue": {"type": "long"},
            "total_funding": {"type": "long"},
            "technologies": {"type": "keyword"},
            "city": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "state": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "country": {"type": "keyword"},
            "linkedin_url": {"type": "keyword"},
            "website": {"type": "keyword"},
            "normalized_domain": {"type": "keyword"},
            "created_at": {"type": "date"},
        }
    }
}

CONTACTS_INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "first_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "last_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "company_id": {"type": "keyword"},
            "email": {"type": "keyword"},
            "title": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "departments": {"type": "keyword"},
            "mobile_phone": {"type": "keyword"},
            "email_status": {"type": "keyword"},
            "seniority": {"type": "keyword"},
            "city": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "state": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "country": {"type": "keyword"},
            "linkedin_url": {"type": "keyword"},
            "created_at": {"type": "date"},
            # Denormalized company fields
            "company_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "company_employees_count": {"type": "long"},
            "company_industries": {"type": "keyword"},
            "company_keywords": {"type": "keyword"},
            "company_address": {"type": "text"},
            "company_annual_revenue": {"type": "long"},
            "company_total_funding": {"type": "long"},
            "company_technologies": {"type": "keyword"},
            "company_city": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "company_state": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "company_country": {"type": "keyword"},
            "company_linkedin_url": {"type": "keyword"},
            "company_website": {"type": "keyword"},
            "company_normalized_domain": {"type": "keyword"},
        }
    }
}

