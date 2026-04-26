"""
Embedding Generation Module
Handles text embedding generation using various models for semantic search.
Enhanced with comprehensive logging and model management.
"""

import logging
from typing import List, Dict, Optional, Any, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
from enum import Enum
import pickle
import os
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

class EmbeddingModel(Enum):
    """Enum for available embedding models"""
    ALL_MINI_LM_L6_V2 = "all-MiniLM-L6-v2"
    ALL_MPNET_BASE_V2 = "all-mpnet-base-v2"
    PARAPHRASE_MULTILINGUAL_MPNET_BASE_V2 = "paraphrase-multilingual-mpnet-base-v2"
    DISTILBERT_BASE_NLI_MEAN_TOKENS = "distilbert-base-nli-mean-tokens"

@dataclass
class EmbeddingConfig:
    """Configuration for embedding generation"""
    model_name: str = "all-MiniLM-L6-v2"
    max_seq_length: int = 512
    batch_size: int = 32
    normalize_embeddings: bool = True
    cache_embeddings: bool = True
    cache_directory: str = "./embedding_cache"

class EmbeddingGenerator:
    """
    Text embedding generator using various models.
    Enhanced with comprehensive logging and caching.
    """
    
    def __init__(self, config: Optional[EmbeddingConfig] = None):
        """
        Initialize the embedding generator.
        
        Args:
            config: EmbeddingConfig object with embedding parameters
        """
        self.config = config or EmbeddingConfig()
        logger.info(f"Initializing EmbeddingGenerator with model: {self.config.model_name}")
        
        try:
            # Load the model
            self.model = SentenceTransformer(self.config.model_name)
            
            # Set model parameters
            self.model.max_seq_length = self.config.max_seq_length
            
            # Create cache directory if needed
            if self.config.cache_embeddings:
                os.makedirs(self.config.cache_directory, exist_ok=True)
            
            # Initialize statistics
            self.stats = {
                'embeddings_generated': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'total_texts_processed': 0,
                'model_load_time': datetime.now().isoformat()
            }
            
            logger.info(f"EmbeddingGenerator initialized successfully with model: {self.config.model_name}")
            
        except Exception as e:
            logger.error(f"Error initializing EmbeddingGenerator: {str(e)}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            Numpy array containing the embedding
        """
        try:
            logger.debug(f"Generating embedding for text of length: {len(text)}")
            
            # Check cache first
            if self.config.cache_embeddings:
                cached_embedding = self._get_cached_embedding(text)
                if cached_embedding is not None:
                    self.stats['cache_hits'] += 1
                    logger.debug("Using cached embedding")
                    return cached_embedding
                else:
                    self.stats['cache_misses'] += 1
            
            # Generate embedding
            embedding = self.model.encode(
                text,
                normalize_embeddings=self.config.normalize_embeddings,
                show_progress_bar=False
            )
            
            # Cache the embedding
            if self.config.cache_embeddings:
                self._cache_embedding(text, embedding)
            
            self.stats['embeddings_generated'] += 1
            self.stats['total_texts_processed'] += 1
            
            logger.debug(f"Generated embedding with shape: {embedding.shape}")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts in batch.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List of numpy arrays containing the embeddings
        """
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts in batch")
            
            # Check cache for all texts
            cached_embeddings = []
            uncached_texts = []
            uncached_indices = []
            
            if self.config.cache_embeddings:
                for i, text in enumerate(texts):
                    cached_embedding = self._get_cached_embedding(text)
                    if cached_embedding is not None:
                        cached_embeddings.append((i, cached_embedding))
                        self.stats['cache_hits'] += 1
                    else:
                        uncached_texts.append(text)
                        uncached_indices.append(i)
                        self.stats['cache_misses'] += 1
            else:
                uncached_texts = texts
                uncached_indices = list(range(len(texts)))
            
            # Generate embeddings for uncached texts
            if uncached_texts:
                logger.debug(f"Generating {len(uncached_texts)} new embeddings")
                
                new_embeddings = self.model.encode(
                    uncached_texts,
                    batch_size=self.config.batch_size,
                    normalize_embeddings=self.config.normalize_embeddings,
                    show_progress_bar=True
                )
                
                # Cache new embeddings
                if self.config.cache_embeddings:
                    for text, embedding in zip(uncached_texts, new_embeddings):
                        self._cache_embedding(text, embedding)
                
                self.stats['embeddings_generated'] += len(uncached_texts)
            
            # Combine cached and new embeddings
            all_embeddings = [None] * len(texts)
            
            # Add cached embeddings
            for i, embedding in cached_embeddings:
                all_embeddings[i] = embedding
            
            # Add new embeddings
            for i, embedding in zip(uncached_indices, new_embeddings):
                all_embeddings[i] = embedding
            
            self.stats['total_texts_processed'] += len(texts)
            
            logger.info(f"Successfully generated {len(all_embeddings)} embeddings")
            return all_embeddings
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise
    
    def _get_cached_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get cached embedding for text."""
        try:
            cache_file = self._get_cache_file_path(text)
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    embedding = pickle.load(f)
                logger.debug("Retrieved embedding from cache")
                return embedding
        except Exception as e:
            logger.warning(f"Error reading cached embedding: {str(e)}")
        
        return None
    
    def _cache_embedding(self, text: str, embedding: np.ndarray):
        """Cache embedding for text."""
        try:
            cache_file = self._get_cache_file_path(text)
            with open(cache_file, 'wb') as f:
                pickle.dump(embedding, f)
            logger.debug("Cached embedding")
        except Exception as e:
            logger.warning(f"Error caching embedding: {str(e)}")
    
    def _get_cache_file_path(self, text: str) -> str:
        """Get cache file path for text."""
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return os.path.join(self.config.cache_directory, f"{text_hash}.pkl")
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score between -1 and 1
        """
        try:
            # Ensure embeddings are normalized
            if self.config.normalize_embeddings:
                similarity = np.dot(embedding1, embedding2)
            else:
                # Calculate cosine similarity manually
                norm1 = np.linalg.norm(embedding1)
                norm2 = np.linalg.norm(embedding2)
                if norm1 == 0 or norm2 == 0:
                    return 0.0
                similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
            
            logger.debug(f"Calculated similarity: {similarity:.4f}")
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def find_most_similar(self, query_embedding: np.ndarray, 
                         candidate_embeddings: List[np.ndarray], 
                         top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Find most similar embeddings to query.
        
        Args:
            query_embedding: Query embedding
            candidate_embeddings: List of candidate embeddings
            top_k: Number of top similar embeddings to return
            
        Returns:
            List of dictionaries with similarity scores and indices
        """
        try:
            logger.info(f"Finding {top_k} most similar embeddings from {len(candidate_embeddings)} candidates")
            
            similarities = []
            for i, candidate in enumerate(candidate_embeddings):
                similarity = self.calculate_similarity(query_embedding, candidate)
                similarities.append({
                    'index': i,
                    'similarity': similarity
                })
            
            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Return top k
            top_similarities = similarities[:top_k]
            
            logger.info(f"Found {len(top_similarities)} similar embeddings")
            return top_similarities
            
        except Exception as e:
            logger.error(f"Error finding similar embeddings: {str(e)}")
            return []
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings generated by this model."""
        try:
            # Generate a test embedding to get dimension
            test_embedding = self.generate_embedding("test")
            return test_embedding.shape[0]
        except Exception as e:
            logger.error(f"Error getting embedding dimension: {str(e)}")
            return 384  # Default for all-MiniLM-L6-v2
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        return {
            'model_name': self.config.model_name,
            'max_seq_length': self.config.max_seq_length,
            'embedding_dimension': self.get_embedding_dimension(),
            'normalize_embeddings': self.config.normalize_embeddings,
            'batch_size': self.config.batch_size,
            'cache_enabled': self.config.cache_embeddings,
            'cache_directory': self.config.cache_directory
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get embedding generation statistics."""
        return {
            **self.stats,
            'cache_hit_rate': self.stats['cache_hits'] / max(self.stats['cache_hits'] + self.stats['cache_misses'], 1),
            'model_info': self.get_model_info()
        }
    
    def clear_cache(self):
        """Clear the embedding cache."""
        try:
            if os.path.exists(self.config.cache_directory):
                import shutil
                shutil.rmtree(self.config.cache_directory)
                os.makedirs(self.config.cache_directory, exist_ok=True)
                logger.info("Embedding cache cleared")
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
    
    def update_config(self, new_config: EmbeddingConfig):
        """
        Update embedding configuration.
        
        Args:
            new_config: New embedding configuration
        """
        try:
            self.config = new_config
            
            # Reload model if model name changed
            if new_config.model_name != self.model.get_sentence_embedding_dimension():
                self.model = SentenceTransformer(new_config.model_name)
                self.model.max_seq_length = new_config.max_seq_length
            
            # Update cache directory
            if new_config.cache_embeddings:
                os.makedirs(new_config.cache_directory, exist_ok=True)
            
            logger.info(f"Updated embedding configuration: {new_config}")
            
        except Exception as e:
            logger.error(f"Error updating configuration: {str(e)}")
            raise

class MultiModelEmbeddingGenerator:
    """
    Multi-model embedding generator for comparing different models.
    """
    
    def __init__(self, model_configs: List[EmbeddingConfig]):
        """
        Initialize with multiple model configurations.
        
        Args:
            model_configs: List of EmbeddingConfig objects
        """
        self.generators = {}
        
        for config in model_configs:
            try:
                generator = EmbeddingGenerator(config)
                self.generators[config.model_name] = generator
                logger.info(f"Loaded model: {config.model_name}")
            except Exception as e:
                logger.error(f"Failed to load model {config.model_name}: {str(e)}")
    
    def generate_embeddings_multi_model(self, text: str, 
                                      model_names: Optional[List[str]] = None) -> Dict[str, np.ndarray]:
        """
        Generate embeddings using multiple models.
        
        Args:
            text: Text to generate embeddings for
            model_names: List of model names to use (None for all)
            
        Returns:
            Dictionary mapping model names to embeddings
        """
        if model_names is None:
            model_names = list(self.generators.keys())
        
        embeddings = {}
        for model_name in model_names:
            if model_name in self.generators:
                try:
                    embedding = self.generators[model_name].generate_embedding(text)
                    embeddings[model_name] = embedding
                except Exception as e:
                    logger.error(f"Error generating embedding with {model_name}: {str(e)}")
        
        return embeddings
    
    def compare_models(self, text1: str, text2: str, 
                      model_names: Optional[List[str]] = None) -> Dict[str, float]:
        """
        Compare similarity between two texts using multiple models.
        
        Args:
            text1: First text
            text2: Second text
            model_names: List of model names to use
            
        Returns:
            Dictionary mapping model names to similarity scores
        """
        if model_names is None:
            model_names = list(self.generators.keys())
        
        similarities = {}
        for model_name in model_names:
            if model_name in self.generators:
                try:
                    generator = self.generators[model_name]
                    emb1 = generator.generate_embedding(text1)
                    emb2 = generator.generate_embedding(text2)
                    similarity = generator.calculate_similarity(emb1, emb2)
                    similarities[model_name] = similarity
                except Exception as e:
                    logger.error(f"Error comparing with {model_name}: {str(e)}")
        
        return similarities

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    config = EmbeddingConfig(
        model_name="all-MiniLM-L6-v2",
        cache_embeddings=True,
        batch_size=16
    )
    
    generator = EmbeddingGenerator(config)
    
    # Generate single embedding
    text = "Senior Data Scientist with Python and machine learning experience"
    embedding = generator.generate_embedding(text)
    print(f"Generated embedding with shape: {embedding.shape}")
    
    # Generate batch embeddings
    texts = [
        "Python developer with Django experience",
        "Machine learning engineer with TensorFlow",
        "Data scientist with SQL and statistics background"
    ]
    
    embeddings = generator.generate_embeddings_batch(texts)
    print(f"Generated {len(embeddings)} embeddings")
    
    # Calculate similarity
    if len(embeddings) >= 2:
        similarity = generator.calculate_similarity(embeddings[0], embeddings[1])
        print(f"Similarity between first two texts: {similarity:.4f}")
    
    # Get statistics
    stats = generator.get_statistics()
    print(f"Generator statistics: {stats}")
    
    # Multi-model comparison
    configs = [
        EmbeddingConfig(model_name="all-MiniLM-L6-v2"),
        EmbeddingConfig(model_name="all-mpnet-base-v2")
    ]
    
    multi_generator = MultiModelEmbeddingGenerator(configs)
    similarities = multi_generator.compare_models(
        "Python developer",
        "Software engineer with Python"
    )
    print(f"Multi-model similarities: {similarities}")
