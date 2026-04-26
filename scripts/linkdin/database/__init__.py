"""
Vector Database Package
Contains modules for vector database operations using ChromaDB.
"""

__version__ = "1.0.0"

from .vector_db import VectorDatabase, JobAnalytics
from .schemas import JobSchema, SearchSchema
from .embeddings import EmbeddingGenerator
from .migrations import DatabaseMigrator

__all__ = [
    'VectorDatabase',
    'JobAnalytics',
    'JobSchema',
    'SearchSchema',
    'EmbeddingGenerator',
    'DatabaseMigrator'
]
