"""
Vector Database Module for Job Storage and Retrieval
Handles ChromaDB operations for storing job embeddings and performing semantic search.
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Any
import json
import uuid
import logging
from datetime import datetime
import os

class VectorDatabase:
    """Vector database for storing and retrieving job embeddings using ChromaDB"""
    
    def __init__(self, persist_directory="./chroma_db", collection_name="job_postings"):
        """Initialize ChromaDB client and collection"""
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize sentence transformer for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "LinkedIn job postings collection"}
        )
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Initialized ChromaDB with {self.collection.count()} existing documents")
    
    def create_job_embedding(self, job_data: Dict) -> str:
        """Create embedding text from job data"""
        # Combine relevant fields for embedding
        embedding_text = f"""
        {job_data.get('title', '')} 
        {job_data.get('company', '')} 
        {job_data.get('location', '')}
        {job_data.get('description', '')}
        {' '.join(job_data.get('skills', []))}
        """.strip()
        
        return embedding_text
    
    def store_job(self, job_data: Dict) -> str:
        """Store a single job in the vector database"""
        try:
            # Generate unique ID if not provided
            job_id = job_data.get('id', str(uuid.uuid4()))
            
            # Create embedding text
            embedding_text = self.create_job_embedding(job_data)
            
            # Generate embedding
            embedding = self.embedding_model.encode(embedding_text).tolist()
            
            # Prepare metadata (ChromaDB requires string values for metadata)
            metadata = {
                'title': str(job_data.get('title', '')),
                'company': str(job_data.get('company', '')),
                'location': str(job_data.get('location', '')),
                'job_type': str(job_data.get('job_type', '')),
                'experience_level': str(job_data.get('experience_level', '')),
                'date_posted': str(job_data.get('date_posted', '')),
                'salary': str(job_data.get('salary', '')),
                'url': str(job_data.get('url', '')),
                'scraped_date': str(job_data.get('scraped_date', datetime.now().isoformat())),
                'skills': json.dumps(job_data.get('skills', []))
            }
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[embedding_text],
                metadatas=[metadata],
                ids=[job_id]
            )
            
            self.logger.info(f"Stored job: {job_data.get('title')} at {job_data.get('company')}")
            return job_id
            
        except Exception as e:
            self.logger.error(f"Error storing job: {str(e)}")
            return None
    
    def store_jobs(self, jobs_data: List[Dict]) -> List[str]:
        """Store multiple jobs in batch"""
        stored_ids = []
        
        try:
            # Prepare batch data
            embeddings = []
            documents = []
            metadatas = []
            ids = []
            
            for job_data in jobs_data:
                # Generate unique ID if not provided
                job_id = job_data.get('id', str(uuid.uuid4()))
                
                # Create embedding text
                embedding_text = self.create_job_embedding(job_data)
                
                # Generate embedding
                embedding = self.embedding_model.encode(embedding_text).tolist()
                
                # Prepare metadata
                metadata = {
                    'title': str(job_data.get('title', '')),
                    'company': str(job_data.get('company', '')),
                    'location': str(job_data.get('location', '')),
                    'job_type': str(job_data.get('job_type', '')),
                    'experience_level': str(job_data.get('experience_level', '')),
                    'date_posted': str(job_data.get('date_posted', '')),
                    'salary': str(job_data.get('salary', '')),
                    'url': str(job_data.get('url', '')),
                    'scraped_date': str(job_data.get('scraped_date', datetime.now().isoformat())),
                    'skills': json.dumps(job_data.get('skills', []))
                }
                
                embeddings.append(embedding)
                documents.append(embedding_text)
                metadatas.append(metadata)
                ids.append(job_id)
                stored_ids.append(job_id)
            
            # Batch add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"Stored {len(jobs_data)} jobs in batch")
            
        except Exception as e:
            self.logger.error(f"Error storing jobs batch: {str(e)}")
            
        return stored_ids
    
    def semantic_search(self, query: str, top_k: int = 10, filters: Dict = None) -> List[Dict]:
        """Perform semantic search for jobs"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Prepare where clause for filtering
            where_clause = {}
            if filters:
                for key, value in filters.items():
                    if value and value != "All":
                        where_clause[key] = value
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where_clause if where_clause else None
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    job_data = {
                        'id': results['ids'][0][i],
                        'title': results['metadatas'][0][i].get('title', ''),
                        'company': results['metadatas'][0][i].get('company', ''),
                        'location': results['metadatas'][0][i].get('location', ''),
                        'description': results['documents'][0][i],
                        'job_type': results['metadatas'][0][i].get('job_type', ''),
                        'experience_level': results['metadatas'][0][i].get('experience_level', ''),
                        'date_posted': results['metadatas'][0][i].get('date_posted', ''),
                        'salary': results['metadatas'][0][i].get('salary', ''),
                        'url': results['metadatas'][0][i].get('url', ''),
                        'skills': json.loads(results['metadatas'][0][i].get('skills', '[]')),
                        'similarity_score': 1 - results['distances'][0][i] if results['distances'][0] else 0
                    }
                    formatted_results.append(job_data)
            
            self.logger.info(f"Found {len(formatted_results)} results for query: '{query}'")
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error in semantic search: {str(e)}")
            return []
    
    def find_similar_jobs(self, job_id: str, top_k: int = 10) -> List[Dict]:
        """Find jobs similar to a given job ID"""
        try:
            # Get the job data first
            job_result = self.collection.get(ids=[job_id])
            
            if not job_result['documents']:
                self.logger.warning(f"Job with ID {job_id} not found")
                return []
            
            # Use the job's document as query
            job_document = job_result['documents'][0]
            
            # Perform similarity search
            return self.semantic_search(job_document, top_k + 1)  # +1 to exclude the original job
            
        except Exception as e:
            self.logger.error(f"Error finding similar jobs: {str(e)}")
            return []
    
    def get_all_jobs(self, limit: int = None) -> List[Dict]:
        """Retrieve all jobs from the database"""
        try:
            # Get all documents
            results = self.collection.get(limit=limit)
            
            # Format results
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'])):
                    job_data = {
                        'id': results['ids'][i],
                        'title': results['metadatas'][i].get('title', ''),
                        'company': results['metadatas'][i].get('company', ''),
                        'location': results['metadatas'][i].get('location', ''),
                        'description': results['documents'][i],
                        'job_type': results['metadatas'][i].get('job_type', ''),
                        'experience_level': results['metadatas'][i].get('experience_level', ''),
                        'date_posted': results['metadatas'][i].get('date_posted', ''),
                        'salary': results['metadatas'][i].get('salary', ''),
                        'url': results['metadatas'][i].get('url', ''),
                        'skills': json.loads(results['metadatas'][i].get('skills', '[]')),
                        'scraped_date': results['metadatas'][i].get('scraped_date', '')
                    }
                    formatted_results.append(job_data)
            
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error retrieving all jobs: {str(e)}")
            return []
    
    def filter_jobs(self, filters: Dict) -> List[Dict]:
        """Filter jobs based on metadata criteria"""
        try:
            # Build where clause
            where_clause = {}
            for key, value in filters.items():
                if value and value != "All":
                    where_clause[key] = value
            
            # Query with filters only (no embedding search)
            results = self.collection.get(where=where_clause)
            
            # Format results
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'])):
                    job_data = {
                        'id': results['ids'][i],
                        'title': results['metadatas'][i].get('title', ''),
                        'company': results['metadatas'][i].get('company', ''),
                        'location': results['metadatas'][i].get('location', ''),
                        'description': results['documents'][i],
                        'job_type': results['metadatas'][i].get('job_type', ''),
                        'experience_level': results['metadatas'][i].get('experience_level', ''),
                        'date_posted': results['metadatas'][i].get('date_posted', ''),
                        'salary': results['metadatas'][i].get('salary', ''),
                        'url': results['metadatas'][i].get('url', ''),
                        'skills': json.loads(results['metadatas'][i].get('skills', '[]')),
                        'scraped_date': results['metadatas'][i].get('scraped_date', '')
                    }
                    formatted_results.append(job_data)
            
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error filtering jobs: {str(e)}")
            return []
    
    def update_job(self, job_id: str, job_data: Dict) -> bool:
        """Update an existing job"""
        try:
            # Check if job exists
            existing = self.collection.get(ids=[job_id])
            if not existing['documents']:
                self.logger.warning(f"Job with ID {job_id} not found for update")
                return False
            
            # Delete existing job
            self.collection.delete(ids=[job_id])
            
            # Add updated job
            job_data['id'] = job_id
            updated_id = self.store_job(job_data)
            
            return updated_id is not None
            
        except Exception as e:
            self.logger.error(f"Error updating job: {str(e)}")
            return False
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job by ID"""
        try:
            self.collection.delete(ids=[job_id])
            self.logger.info(f"Deleted job with ID: {job_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting job: {str(e)}")
            return False
    
    def get_job_count(self) -> int:
        """Get total number of jobs in the database"""
        try:
            return self.collection.count()
        except Exception as e:
            self.logger.error(f"Error getting job count: {str(e)}")
            return 0
    
    def get_unique_values(self, field: str) -> List[str]:
        """Get unique values for a specific field"""
        try:
            all_jobs = self.get_all_jobs()
            unique_values = list(set(job.get(field, '') for job in all_jobs if job.get(field)))
            return sorted(unique_values)
            
        except Exception as e:
            self.logger.error(f"Error getting unique values for {field}: {str(e)}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        try:
            stats = {
                'total_jobs': self.get_job_count(),
                'unique_companies': len(self.get_unique_values('company')),
                'unique_locations': len(self.get_unique_values('location')),
                'job_types': self.get_unique_values('job_type'),
                'experience_levels': self.get_unique_values('experience_level')
            }
            
            # Get date range
            all_jobs = self.get_all_jobs()
            if all_jobs:
                dates = [job.get('date_posted', '') for job in all_jobs if job.get('date_posted')]
                if dates:
                    stats['date_range'] = {
                        'earliest': min(dates),
                        'latest': max(dates)
                    }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {str(e)}")
            return {}
    
    def clear_all(self) -> bool:
        """Clear all jobs from the database"""
        try:
            # Delete the collection
            self.client.delete_collection(name=self.collection_name)
            
            # Recreate the collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "LinkedIn job postings collection"}
            )
            
            self.logger.info("Cleared all jobs from the database")
            return True
            
        except Exception as e:
            self.logger.error(f"Error clearing database: {str(e)}")
            return False
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """Export all jobs to a pandas DataFrame"""
        try:
            all_jobs = self.get_all_jobs()
            if all_jobs:
                df = pd.DataFrame(all_jobs)
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"Error exporting to DataFrame: {str(e)}")
            return pd.DataFrame()
    
    def import_from_dataframe(self, df: pd.DataFrame) -> int:
        """Import jobs from a pandas DataFrame"""
        try:
            jobs_data = df.to_dict('records')
            stored_ids = self.store_jobs(jobs_data)
            return len(stored_ids)
            
        except Exception as e:
            self.logger.error(f"Error importing from DataFrame: {str(e)}")
            return 0

# Advanced search and analytics functions
class JobAnalytics:
    """Advanced analytics functions for job data"""
    
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db
    
    def get_salary_insights(self) -> Dict:
        """Analyze salary data"""
        all_jobs = self.vector_db.get_all_jobs()
        
        salaries = []
        for job in all_jobs:
            salary_text = job.get('salary', '')
            if salary_text:
                # Extract numeric values from salary strings
                import re
                numbers = re.findall(r'\\d+', salary_text.replace(',', ''))
                if numbers:
                    salaries.append(int(numbers[0]))
        
        if salaries:
            return {
                'average': sum(salaries) / len(salaries),
                'median': sorted(salaries)[len(salaries) // 2],
                'min': min(salaries),
                'max': max(salaries),
                'count': len(salaries)
            }
        
        return {}
    
    def get_trending_skills(self) -> List[Dict]:
        """Get trending skills from job descriptions"""
        all_jobs = self.vector_db.get_all_jobs()
        
        skill_count = {}
        for job in all_jobs:
            skills = job.get('skills', [])
            for skill in skills:
                skill_count[skill] = skill_count.get(skill, 0) + 1
        
        # Sort by frequency
        trending_skills = [
            {'skill': skill, 'count': count}
            for skill, count in sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
        ]
        
        return trending_skills[:20]  # Top 20 skills
    
    def get_location_insights(self) -> Dict:
        """Analyze job distribution by location"""
        all_jobs = self.vector_db.get_all_jobs()
        
        location_count = {}
        for job in all_jobs:
            location = job.get('location', '')
            if location:
                location_count[location] = location_count.get(location, 0) + 1
        
        return dict(sorted(location_count.items(), key=lambda x: x[1], reverse=True))
    
    def get_company_insights(self) -> Dict:
        """Analyze hiring patterns by company"""
        all_jobs = self.vector_db.get_all_jobs()
        
        company_count = {}
        for job in all_jobs:
            company = job.get('company', '')
            if company:
                company_count[company] = company_count.get(company, 0) + 1
        
        return dict(sorted(company_count.items(), key=lambda x: x[1], reverse=True))

# Usage example
if __name__ == "__main__":
    # Initialize vector database
    vector_db = VectorDatabase()
    
    # Example job data
    sample_job = {
        'id': 'job_001',
        'title': 'Senior Data Scientist',
        'company': 'TechCorp',
        'location': 'San Francisco, CA',
        'description': 'Looking for an experienced data scientist with Python and machine learning skills...',
        'skills': ['python', 'machine learning', 'tensorflow', 'sql'],
        'job_type': 'Full-time',
        'experience_level': 'Mid-Senior level',
        'date_posted': '2024-01-15',
        'salary': '$120,000 - $150,000'
    }
    
    # Store job
    job_id = vector_db.store_job(sample_job)
    print(f"Stored job with ID: {job_id}")
    
    # Semantic search
    results = vector_db.semantic_search("python machine learning remote", top_k=5)
    print(f"Found {len(results)} similar jobs")
    
    # Get statistics
    stats = vector_db.get_statistics()
    print(f"Database contains {stats.get('total_jobs', 0)} jobs")