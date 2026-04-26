"""
Vector Database Module for Job Storage and Retrieval
Handles ChromaDB operations for storing job embeddings and performing semantic search.
Enhanced with comprehensive logging, error handling, and advanced analytics.
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Any, Tuple
import json
import uuid
import logging
from datetime import datetime
import os
import hashlib
from dataclasses import dataclass
from enum import Enum

# Set up logging
logger = logging.getLogger(__name__)

class CollectionStatus(Enum):
    """Enum for collection status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

@dataclass
class DatabaseConfig:
    """Configuration for vector database"""
    persist_directory: str = "./chroma_db"
    collection_name: str = "job_postings"
    embedding_model: str = "all-MiniLM-L6-v2"
    max_results: int = 1000
    similarity_threshold: float = 0.7
    batch_size: int = 100

class VectorDatabase:
    """
    Vector database for storing and retrieving job embeddings using ChromaDB.
    Enhanced with comprehensive logging, error handling, and advanced analytics.
    """
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """
        Initialize ChromaDB client and collection.
        
        Args:
            config: DatabaseConfig object with database parameters
        """
        self.config = config or DatabaseConfig()
        logger.info(f"Initializing VectorDatabase with config: {self.config}")
        
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=self.config.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            logger.info(f"ChromaDB client initialized at {self.config.persist_directory}")
            
            # Initialize sentence transformer for embeddings
            logger.info(f"Loading embedding model: {self.config.embedding_model}")
            self.embedding_model = SentenceTransformer(self.config.embedding_model)
            logger.info("Embedding model loaded successfully")
            
            # Get or create collection
            self.collection = self._get_or_create_collection()
            
            # Initialize statistics
            self.stats = {
                'total_jobs': 0,
                'total_queries': 0,
                'successful_queries': 0,
                'failed_queries': 0,
                'embeddings_generated': 0,
                'last_updated': datetime.now().isoformat()
            }
            
            # Update statistics
            self._update_statistics()
            
            logger.info(f"VectorDatabase initialized successfully with {self.stats['total_jobs']} existing documents")
            
        except Exception as e:
            logger.error(f"Error initializing VectorDatabase: {str(e)}")
            raise
    
    def _get_or_create_collection(self):
        """Get or create the collection with proper metadata."""
        try:
            # Try to get existing collection
            collection = self.client.get_collection(name=self.config.collection_name)
            logger.info(f"Retrieved existing collection: {self.config.collection_name}")
            return collection
            
        except Exception:
            # Create new collection
            try:
                collection = self.client.create_collection(
                    name=self.config.collection_name,
                    metadata={
                        "description": "LinkedIn job postings collection",
                        "created_at": datetime.now().isoformat(),
                        "embedding_model": self.config.embedding_model,
                        "version": "1.0.0"
                    }
                )
                logger.info(f"Created new collection: {self.config.collection_name}")
                return collection
                
            except Exception as e:
                logger.error(f"Error creating collection: {str(e)}")
                raise
    
    def create_job_embedding(self, job_data: Dict[str, Any]) -> str:
        """
        Create embedding text from job data.
        
        Args:
            job_data: Job data dictionary
            
        Returns:
            Text string for embedding
        """
        try:
            # Combine relevant fields for embedding
            embedding_parts = []
            
            # Add title
            if job_data.get('title'):
                embedding_parts.append(f"Title: {job_data['title']}")
            
            # Add company
            if job_data.get('company'):
                embedding_parts.append(f"Company: {job_data['company']}")
            
            # Add location
            if job_data.get('location'):
                embedding_parts.append(f"Location: {job_data['location']}")
            
            # Add description (truncated for efficiency)
            if job_data.get('description'):
                description = job_data['description'][:1000]  # Limit description length
                embedding_parts.append(f"Description: {description}")
            
            # Add skills
            if job_data.get('skills'):
                skills_text = ', '.join(job_data['skills'][:10])  # Limit skills
                embedding_parts.append(f"Skills: {skills_text}")
            
            # Add job type and experience level
            if job_data.get('job_type'):
                embedding_parts.append(f"Job Type: {job_data['job_type']}")
            
            if job_data.get('experience_level'):
                embedding_parts.append(f"Experience: {job_data['experience_level']}")
            
            embedding_text = ' '.join(embedding_parts)
            
            logger.debug(f"Created embedding text of length: {len(embedding_text)}")
            return embedding_text
            
        except Exception as e:
            logger.error(f"Error creating job embedding: {str(e)}")
            return ""
    
    def store_job(self, job_data: Dict[str, Any]) -> Optional[str]:
        """
        Store a single job in the vector database.
        
        Args:
            job_data: Job data dictionary
            
        Returns:
            Job ID if successful, None otherwise
        """
        try:
            # Generate unique ID if not provided
            job_id = job_data.get('id', str(uuid.uuid4()))
            
            # Create embedding text
            embedding_text = self.create_job_embedding(job_data)
            if not embedding_text:
                logger.warning(f"No embedding text created for job: {job_id}")
                return None
            
            # Generate embedding
            logger.debug(f"Generating embedding for job: {job_id}")
            embedding = self.embedding_model.encode(embedding_text).tolist()
            self.stats['embeddings_generated'] += 1
            
            # Prepare metadata (ChromaDB requires string values for metadata)
            metadata = self._prepare_metadata(job_data)
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[embedding_text],
                metadatas=[metadata],
                ids=[job_id]
            )
            
            self.stats['total_jobs'] += 1
            logger.info(f"Stored job: {job_data.get('title', 'Unknown')} at {job_data.get('company', 'Unknown')}")
            return job_id
            
        except Exception as e:
            logger.error(f"Error storing job: {str(e)}")
            return None
    
    def store_jobs(self, jobs_data: List[Dict[str, Any]]) -> List[str]:
        """
        Store multiple jobs in batch.
        
        Args:
            jobs_data: List of job data dictionaries
            
        Returns:
            List of stored job IDs
        """
        stored_ids = []
        
        try:
            logger.info(f"Storing {len(jobs_data)} jobs in batch")
            
            # Process jobs in batches
            for i in range(0, len(jobs_data), self.config.batch_size):
                batch = jobs_data[i:i + self.config.batch_size]
                batch_ids = self._store_batch(batch)
                stored_ids.extend(batch_ids)
                
                logger.debug(f"Processed batch {i//self.config.batch_size + 1}/{(len(jobs_data)-1)//self.config.batch_size + 1}")
            
            self.stats['total_jobs'] += len(stored_ids)
            logger.info(f"Successfully stored {len(stored_ids)} jobs")
            
        except Exception as e:
            logger.error(f"Error storing jobs batch: {str(e)}")
            
        return stored_ids
    
    def _store_batch(self, batch_jobs: List[Dict[str, Any]]) -> List[str]:
        """Store a batch of jobs."""
        try:
            # Prepare batch data
            embeddings = []
            documents = []
            metadatas = []
            ids = []
            stored_ids = []
            
            for job_data in batch_jobs:
                # Generate unique ID if not provided
                job_id = job_data.get('id', str(uuid.uuid4()))
                
                # Create embedding text
                embedding_text = self.create_job_embedding(job_data)
                if not embedding_text:
                    logger.warning(f"Skipping job {job_id}: no embedding text")
                    continue
                
                # Generate embedding
                embedding = self.embedding_model.encode(embedding_text).tolist()
                self.stats['embeddings_generated'] += 1
                
                # Prepare metadata
                metadata = self._prepare_metadata(job_data)
                
                embeddings.append(embedding)
                documents.append(embedding_text)
                metadatas.append(metadata)
                ids.append(job_id)
                stored_ids.append(job_id)
            
            # Batch add to collection
            if embeddings:
                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.debug(f"Stored batch of {len(embeddings)} jobs")
            
            return stored_ids
            
        except Exception as e:
            logger.error(f"Error storing batch: {str(e)}")
            return []
    
    def _prepare_metadata(self, job_data: Dict[str, Any]) -> Dict[str, str]:
        """Prepare metadata for ChromaDB storage."""
        return {
            'title': str(job_data.get('title', '')),
            'company': str(job_data.get('company', '')),
            'location': str(job_data.get('location', '')),
            'job_type': str(job_data.get('job_type', '')),
            'experience_level': str(job_data.get('experience_level', '')),
            'date_posted': str(job_data.get('date_posted', '')),
            'salary': str(job_data.get('salary', '')),
            'url': str(job_data.get('url', '')),
            'scraped_date': str(job_data.get('scraped_date', datetime.now().isoformat())),
            'skills': json.dumps(job_data.get('skills', [])),
            'source': str(job_data.get('source', 'linkedin')),
            'job_hash': str(job_data.get('job_hash', ''))
        }
    
    def semantic_search(self, query: str, top_k: int = 10, 
                       filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Perform semantic search for jobs.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            filters: Optional filters to apply
            
        Returns:
            List of matching job dictionaries
        """
        try:
            self.stats['total_queries'] += 1
            logger.info(f"Performing semantic search: '{query}' (top_k={top_k})")
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Prepare where clause for filtering
            where_clause = self._build_where_clause(filters)
            
            # Query the collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, self.config.max_results),
                where=where_clause if where_clause else None
            )
            
            # Format results
            formatted_results = self._format_search_results(results)
            
            self.stats['successful_queries'] += 1
            logger.info(f"Found {len(formatted_results)} results for query: '{query}'")
            return formatted_results
            
        except Exception as e:
            self.stats['failed_queries'] += 1
            logger.error(f"Error in semantic search: {str(e)}")
            return []
    
    def _build_where_clause(self, filters: Optional[Dict]) -> Optional[Dict]:
        """Build where clause for filtering."""
        if not filters:
            return None
        
        where_clause = {}
        
        for key, value in filters.items():
            if value and value != "All" and value != "":
                where_clause[key] = value
        
        logger.debug(f"Built where clause: {where_clause}")
        return where_clause if where_clause else None
    
    def _format_search_results(self, results: Dict) -> List[Dict[str, Any]]:
        """Format search results into job dictionaries."""
        formatted_results = []
        
        try:
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
                        'similarity_score': 1 - results['distances'][0][i] if results['distances'][0] else 0,
                        'source': results['metadatas'][0][i].get('source', 'linkedin')
                    }
                    formatted_results.append(job_data)
            
        except Exception as e:
            logger.error(f"Error formatting search results: {str(e)}")
        
        return formatted_results
    
    def find_similar_jobs(self, job_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Find jobs similar to a given job ID.
        
        Args:
            job_id: ID of the job to find similar jobs for
            top_k: Number of similar jobs to return
            
        Returns:
            List of similar job dictionaries
        """
        try:
            logger.info(f"Finding similar jobs for job ID: {job_id}")
            
            # Get the job data first
            job_result = self.collection.get(ids=[job_id])
            
            if not job_result['documents']:
                logger.warning(f"Job with ID {job_id} not found")
                return []
            
            # Use the job's document as query
            job_document = job_result['documents'][0]
            
            # Perform similarity search
            similar_jobs = self.semantic_search(job_document, top_k + 1)
            
            # Remove the original job from results
            similar_jobs = [job for job in similar_jobs if job['id'] != job_id]
            
            logger.info(f"Found {len(similar_jobs)} similar jobs")
            return similar_jobs
            
        except Exception as e:
            logger.error(f"Error finding similar jobs: {str(e)}")
            return []
    
    def get_all_jobs(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all jobs from the database.
        
        Args:
            limit: Maximum number of jobs to retrieve
            
        Returns:
            List of all job dictionaries
        """
        try:
            logger.info(f"Retrieving all jobs (limit={limit})")
            
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
                        'scraped_date': results['metadatas'][i].get('scraped_date', ''),
                        'source': results['metadatas'][i].get('source', 'linkedin')
                    }
                    formatted_results.append(job_data)
            
            logger.info(f"Retrieved {len(formatted_results)} jobs")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error retrieving all jobs: {str(e)}")
            return []
    
    def filter_jobs(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter jobs based on metadata criteria.
        
        Args:
            filters: Dictionary of filter criteria
            
        Returns:
            List of filtered job dictionaries
        """
        try:
            logger.info(f"Filtering jobs with criteria: {filters}")
            
            # Build where clause
            where_clause = self._build_where_clause(filters)
            
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
                        'scraped_date': results['metadatas'][i].get('scraped_date', ''),
                        'source': results['metadatas'][i].get('source', 'linkedin')
                    }
                    formatted_results.append(job_data)
            
            logger.info(f"Found {len(formatted_results)} jobs matching filters")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error filtering jobs: {str(e)}")
            return []
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific job by ID.
        
        Args:
            job_id: ID of the job to retrieve
            
        Returns:
            Job dictionary or None if not found
        """
        try:
            logger.debug(f"Retrieving job by ID: {job_id}")
            
            results = self.collection.get(ids=[job_id])
            
            if not results['documents']:
                logger.warning(f"Job with ID {job_id} not found")
                return None
            
            # Format single result
            job_data = {
                'id': results['ids'][0],
                'title': results['metadatas'][0].get('title', ''),
                'company': results['metadatas'][0].get('company', ''),
                'location': results['metadatas'][0].get('location', ''),
                'description': results['documents'][0],
                'job_type': results['metadatas'][0].get('job_type', ''),
                'experience_level': results['metadatas'][0].get('experience_level', ''),
                'date_posted': results['metadatas'][0].get('date_posted', ''),
                'salary': results['metadatas'][0].get('salary', ''),
                'url': results['metadatas'][0].get('url', ''),
                'skills': json.loads(results['metadatas'][0].get('skills', '[]')),
                'scraped_date': results['metadatas'][0].get('scraped_date', ''),
                'source': results['metadatas'][0].get('source', 'linkedin')
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error retrieving job by ID: {str(e)}")
            return None
    
    def update_job(self, job_id: str, job_data: Dict[str, Any]) -> bool:
        """
        Update an existing job.
        
        Args:
            job_id: ID of the job to update
            job_data: Updated job data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Updating job: {job_id}")
            
            # Check if job exists
            existing = self.collection.get(ids=[job_id])
            if not existing['documents']:
                logger.warning(f"Job with ID {job_id} not found for update")
                return False
            
            # Delete existing job
            self.collection.delete(ids=[job_id])
            
            # Add updated job
            job_data['id'] = job_id
            updated_id = self.store_job(job_data)
            
            success = updated_id is not None
            if success:
                logger.info(f"Successfully updated job: {job_id}")
            else:
                logger.error(f"Failed to update job: {job_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating job: {str(e)}")
            return False
    
    def delete_job(self, job_id: str) -> bool:
        """
        Delete a job by ID.
        
        Args:
            job_id: ID of the job to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Deleting job: {job_id}")
            
            self.collection.delete(ids=[job_id])
            self.stats['total_jobs'] = max(0, self.stats['total_jobs'] - 1)
            
            logger.info(f"Successfully deleted job: {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting job: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary containing database statistics
        """
        try:
            self._update_statistics()
            
            # Get additional statistics
            all_jobs = self.get_all_jobs()
            
            stats = {
                **self.stats,
                'unique_companies': len(set(job.get('company', '') for job in all_jobs if job.get('company'))),
                'unique_locations': len(set(job.get('location', '') for job in all_jobs if job.get('location'))),
                'job_types': list(set(job.get('job_type', '') for job in all_jobs if job.get('job_type'))),
                'experience_levels': list(set(job.get('experience_level', '') for job in all_jobs if job.get('experience_level'))),
                'date_range': self._get_date_range(all_jobs),
                'collection_info': {
                    'name': self.config.collection_name,
                    'embedding_model': self.config.embedding_model,
                    'persist_directory': self.config.persist_directory
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return self.stats
    
    def _update_statistics(self):
        """Update internal statistics."""
        try:
            # Get actual count from collection
            actual_count = self.collection.count()
            self.stats['total_jobs'] = actual_count
            self.stats['last_updated'] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Error updating statistics: {str(e)}")
    
    def _get_date_range(self, jobs: List[Dict[str, Any]]) -> Dict[str, str]:
        """Get date range of jobs."""
        try:
            dates = [job.get('date_posted', '') for job in jobs if job.get('date_posted')]
            if dates:
                return {
                    'earliest': min(dates),
                    'latest': max(dates)
                }
            return {'earliest': '', 'latest': ''}
            
        except Exception as e:
            logger.error(f"Error getting date range: {str(e)}")
            return {'earliest': '', 'latest': ''}
    
    def clear_all(self) -> bool:
        """
        Clear all jobs from the database.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Clearing all jobs from database")
            
            # Delete the collection
            self.client.delete_collection(name=self.config.collection_name)
            
            # Recreate the collection
            self.collection = self._get_or_create_collection()
            
            # Reset statistics
            self.stats['total_jobs'] = 0
            self.stats['last_updated'] = datetime.now().isoformat()
            
            logger.info("Successfully cleared all jobs from database")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            return False
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """
        Export all jobs to a pandas DataFrame.
        
        Returns:
            DataFrame containing all jobs
        """
        try:
            logger.info("Exporting jobs to DataFrame")
            
            all_jobs = self.get_all_jobs()
            if all_jobs:
                df = pd.DataFrame(all_jobs)
                logger.info(f"Exported {len(df)} jobs to DataFrame")
                return df
            else:
                logger.info("No jobs to export")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error exporting to DataFrame: {str(e)}")
            return pd.DataFrame()
    
    def import_from_dataframe(self, df: pd.DataFrame) -> int:
        """
        Import jobs from a pandas DataFrame.
        
        Args:
            df: DataFrame containing job data
            
        Returns:
            Number of jobs imported
        """
        try:
            logger.info(f"Importing {len(df)} jobs from DataFrame")
            
            jobs_data = df.to_dict('records')
            stored_ids = self.store_jobs(jobs_data)
            
            logger.info(f"Successfully imported {len(stored_ids)} jobs")
            return len(stored_ids)
            
        except Exception as e:
            logger.error(f"Error importing from DataFrame: {str(e)}")
            return 0

# Advanced analytics class
class JobAnalytics:
    """
    Advanced analytics functions for job data.
    Enhanced with comprehensive logging and statistical analysis.
    """
    
    def __init__(self, vector_db: VectorDatabase):
        """
        Initialize analytics with vector database.
        
        Args:
            vector_db: VectorDatabase instance
        """
        self.vector_db = vector_db
        logger.info("Initialized JobAnalytics")
    
    def get_salary_insights(self) -> Dict[str, Any]:
        """
        Analyze salary data and provide insights.
        
        Returns:
            Dictionary containing salary insights
        """
        try:
            logger.info("Analyzing salary data")
            
            all_jobs = self.vector_db.get_all_jobs()
            salaries = []
            
            for job in all_jobs:
                salary_text = job.get('salary', '')
                if salary_text:
                    # Extract numeric values from salary strings
                    numbers = re.findall(r'\d+', salary_text.replace(',', ''))
                    if numbers:
                        # Take the first number (usually minimum salary)
                        salaries.append(int(numbers[0]))
            
            if salaries:
                insights = {
                    'average': sum(salaries) / len(salaries),
                    'median': sorted(salaries)[len(salaries) // 2],
                    'min': min(salaries),
                    'max': max(salaries),
                    'count': len(salaries),
                    'distribution': self._calculate_salary_distribution(salaries)
                }
                
                logger.info(f"Salary analysis complete: {len(salaries)} salaries analyzed")
                return insights
            
            logger.warning("No salary data found for analysis")
            return {}
            
        except Exception as e:
            logger.error(f"Error analyzing salary data: {str(e)}")
            return {}
    
    def _calculate_salary_distribution(self, salaries: List[int]) -> Dict[str, int]:
        """Calculate salary distribution by ranges."""
        ranges = {
            '0-50k': 0,
            '50k-75k': 0,
            '75k-100k': 0,
            '100k-125k': 0,
            '125k-150k': 0,
            '150k+': 0
        }
        
        for salary in salaries:
            if salary < 50000:
                ranges['0-50k'] += 1
            elif salary < 75000:
                ranges['50k-75k'] += 1
            elif salary < 100000:
                ranges['75k-100k'] += 1
            elif salary < 125000:
                ranges['100k-125k'] += 1
            elif salary < 150000:
                ranges['125k-150k'] += 1
            else:
                ranges['150k+'] += 1
        
        return ranges
    
    def get_trending_skills(self, top_n: int = 20) -> List[Dict[str, Any]]:
        """
        Get trending skills from job descriptions.
        
        Args:
            top_n: Number of top skills to return
            
        Returns:
            List of trending skills with counts
        """
        try:
            logger.info(f"Analyzing trending skills (top {top_n})")
            
            all_jobs = self.vector_db.get_all_jobs()
            skill_count = {}
            
            for job in all_jobs:
                skills = job.get('skills', [])
                for skill in skills:
                    skill_count[skill] = skill_count.get(skill, 0) + 1
            
            # Sort by frequency
            trending_skills = [
                {'skill': skill, 'count': count, 'percentage': (count / len(all_jobs)) * 100}
                for skill, count in sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
            ]
            
            logger.info(f"Found {len(trending_skills)} unique skills")
            return trending_skills[:top_n]
            
        except Exception as e:
            logger.error(f"Error analyzing trending skills: {str(e)}")
            return []
    
    def get_location_insights(self) -> Dict[str, Any]:
        """
        Analyze job distribution by location.
        
        Returns:
            Dictionary containing location insights
        """
        try:
            logger.info("Analyzing location distribution")
            
            all_jobs = self.vector_db.get_all_jobs()
            location_count = {}
            
            for job in all_jobs:
                location = job.get('location', '')
                if location:
                    location_count[location] = location_count.get(location, 0) + 1
            
            # Sort by count
            sorted_locations = dict(sorted(location_count.items(), key=lambda x: x[1], reverse=True))
            
            # Calculate percentages
            total_jobs = len(all_jobs)
            location_insights = {
                'distribution': sorted_locations,
                'top_10': dict(list(sorted_locations.items())[:10]),
                'remote_percentage': self._calculate_remote_percentage(all_jobs),
                'total_locations': len(sorted_locations)
            }
            
            logger.info(f"Location analysis complete: {len(sorted_locations)} unique locations")
            return location_insights
            
        except Exception as e:
            logger.error(f"Error analyzing location data: {str(e)}")
            return {}
    
    def _calculate_remote_percentage(self, jobs: List[Dict[str, Any]]) -> float:
        """Calculate percentage of remote jobs."""
        remote_keywords = ['remote', 'work from home', 'wfh', 'distributed', 'anywhere']
        remote_count = 0
        
        for job in jobs:
            location = job.get('location', '').lower()
            if any(keyword in location for keyword in remote_keywords):
                remote_count += 1
        
        return (remote_count / len(jobs)) * 100 if jobs else 0
    
    def get_company_insights(self) -> Dict[str, Any]:
        """
        Analyze hiring patterns by company.
        
        Returns:
            Dictionary containing company insights
        """
        try:
            logger.info("Analyzing company hiring patterns")
            
            all_jobs = self.vector_db.get_all_jobs()
            company_count = {}
            
            for job in all_jobs:
                company = job.get('company', '')
                if company:
                    company_count[company] = company_count.get(company, 0) + 1
            
            # Sort by count
            sorted_companies = dict(sorted(company_count.items(), key=lambda x: x[1], reverse=True))
            
            insights = {
                'distribution': sorted_companies,
                'top_10': dict(list(sorted_companies.items())[:10]),
                'total_companies': len(sorted_companies),
                'average_jobs_per_company': sum(sorted_companies.values()) / len(sorted_companies) if sorted_companies else 0
            }
            
            logger.info(f"Company analysis complete: {len(sorted_companies)} unique companies")
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing company data: {str(e)}")
            return {}
    
    def get_market_trends(self) -> Dict[str, Any]:
        """
        Analyze market trends over time.
        
        Returns:
            Dictionary containing market trend insights
        """
        try:
            logger.info("Analyzing market trends")
            
            all_jobs = self.vector_db.get_all_jobs()
            
            # Group jobs by date
            jobs_by_date = {}
            for job in all_jobs:
                date = job.get('date_posted', '')
                if date:
                    if date not in jobs_by_date:
                        jobs_by_date[date] = []
                    jobs_by_date[date].append(job)
            
            # Calculate trends
            trends = {
                'jobs_by_date': {date: len(jobs) for date, jobs in jobs_by_date.items()},
                'total_jobs': len(all_jobs),
                'date_range': {
                    'earliest': min(jobs_by_date.keys()) if jobs_by_date else '',
                    'latest': max(jobs_by_date.keys()) if jobs_by_date else ''
                },
                'average_jobs_per_day': len(all_jobs) / len(jobs_by_date) if jobs_by_date else 0
            }
            
            logger.info("Market trend analysis complete")
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {str(e)}")
            return {}

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    config = DatabaseConfig(
        persist_directory="./test_chroma_db",
        collection_name="test_jobs"
    )
    
    vector_db = VectorDatabase(config)
    
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
    print(f"Database statistics: {stats}")
    
    # Analytics
    analytics = JobAnalytics(vector_db)
    salary_insights = analytics.get_salary_insights()
    print(f"Salary insights: {salary_insights}")
