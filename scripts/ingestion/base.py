"""
Base ingestion class with shared batch processing and thread pool logic.

This module provides the BaseIngester abstract class that handles common
ingestion patterns like batch processing, thread pool management, and
error handling.
"""

import csv
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Iterator, Optional
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED

from ..config import get_default
from ..utils import log_error


class BaseIngester(ABC):
    """
    Abstract base class for data ingestion.
    
    Handles common batch processing, thread pool management, and error handling.
    Subclasses must implement insert_data() and provide_data_source() methods.
    """
    
    def __init__(self, batch_size: Optional[int] = None, max_threads: Optional[int] = None):
        """
        Initialize the ingester.
        
        Args:
            batch_size: Number of rows to process per batch (defaults to config)
            max_threads: Maximum number of concurrent threads (defaults to config)
        """
        self.batch_size = batch_size or get_default("batch_size", 1000)
        self.max_threads = max_threads or get_default("max_threads", 3)
    
    @abstractmethod
    def insert_data(self, data_list: List[Dict]) -> None:
        """
        Insert a batch of data into the database.
        
        This method must be implemented by subclasses to handle the specific
        data transformation and insertion logic.
        
        Args:
            data_list: List of dictionaries representing rows to insert
        """
        pass
    
    @abstractmethod
    def get_data_source_description(self) -> str:
        """
        Get a description of the data source for logging.
        
        Returns:
            String description of the data source (e.g., filename, S3 key)
        """
        pass
    
    def _get_csv_reader(self) -> Iterator[Dict]:
        """
        Get a CSV reader iterator for the data source.
        
        This method must be implemented by subclasses to provide the appropriate
        CSV reader (from file or S3).
        
        Returns:
            Iterator of dictionaries representing CSV rows
        """
        raise NotImplementedError("Subclasses must implement _get_csv_reader()")
    
    def ingest(self) -> None:
        """
        Main ingestion method that processes data in batches using thread pools.
        
        This method handles:
        - Reading data from the source
        - Batching data
        - Managing thread pool for concurrent processing
        - Error handling and logging
        """
        source_desc = self.get_data_source_description()
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = set()
            
            def submit_batch(batch: List[Dict]) -> None:
                """Submit a batch for processing."""
                future = executor.submit(self.insert_data, batch)
                futures.add(future)
            
            def wait_for_slot() -> None:
                """Wait for a thread slot to become available."""
                if len(futures) < self.max_threads:
                    return
                wait_for_completion(return_when=FIRST_COMPLETED)
            
            def wait_for_completion(return_when=None) -> None:
                """Wait for futures to complete and handle results.

                Any exceptions raised during batch processing are caught and
                recorded via the centralized error logger so that the overall
                ingestion job can continue where possible.
                """
                done, _ = wait(futures, return_when=return_when if return_when is not None else ALL_COMPLETED)
                for future in done:
                    futures.discard(future)
                    try:
                        future.result()  # Raise any exceptions that occurred
                    except Exception as e:
                        # Log a high-level batch error; individual rows should already
                        # be logged by insert_data implementations when possible.
                        log_error(
                            {
                                "source": source_desc,
                                "message": "Batch processing failure",
                            },
                            error_reason=str(e),
                            error_type="batch",
                        )
                        print(f"Error processing batch from {source_desc}: {e}")
            
            # Read and process data in batches
            data_lst = []
            reader = self._get_csv_reader()
            
            for row in reader:
                data_lst.append(row)
                
                if len(data_lst) >= self.batch_size:
                    batch = data_lst[:]
                    data_lst.clear()
                    print(f"Inserting {len(batch)} rows from {source_desc}")
                    submit_batch(batch)
                    wait_for_slot()
            
            # Process remaining data
            if data_lst:
                batch = data_lst[:]
                data_lst.clear()
                print(f"Inserting {len(batch)} rows from {source_desc}")
                submit_batch(batch)
            
            # Wait for all remaining futures to complete
            while futures:
                wait_for_completion()
        
        print(f"Data inserted successfully from {source_desc}")


class LocalFileIngester(BaseIngester):
    """
    Base class for ingesting data from local CSV files.
    
    Subclasses must implement insert_data() method.
    """
    
    def __init__(self, file_path: str, batch_size: Optional[int] = None, max_threads: Optional[int] = None):
        """
        Initialize local file ingester.
        
        Args:
            file_path: Path to the CSV file to ingest
            batch_size: Number of rows to process per batch
            max_threads: Maximum number of concurrent threads
        """
        super().__init__(batch_size, max_threads)
        self.file_path = file_path
        self._file_handle = None
    
    def get_data_source_description(self) -> str:
        """Get description of the data source."""
        return os.path.basename(self.file_path)
    
    def _get_csv_reader(self) -> Iterator[Dict]:
        """Get CSV reader for local file."""
        self._file_handle = open(self.file_path, 'r', encoding='utf-8', newline='')
        return csv.DictReader(self._file_handle)
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close file handle."""
        if self._file_handle:
            self._file_handle.close()
        return False


class S3Ingester(BaseIngester):
    """
    Base class for ingesting data from S3 CSV objects.
    
    Subclasses must implement insert_data() method.
    """
    
    def __init__(
        self,
        s3_client,
        bucket_name: str,
        object_key: str,
        batch_size: Optional[int] = None,
        max_threads: Optional[int] = None
    ):
        """
        Initialize S3 ingester.
        
        Args:
            s3_client: Boto3 S3 client
            bucket_name: S3 bucket name
            object_key: S3 object key (path to CSV file)
            batch_size: Number of rows to process per batch
            max_threads: Maximum number of concurrent threads
        """
        super().__init__(batch_size, max_threads)
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.object_key = object_key
    
    def get_data_source_description(self) -> str:
        """Get description of the data source."""
        return self.object_key
    
    def _get_csv_reader(self) -> Iterator[Dict]:
        """Get CSV reader for S3 object."""
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.object_key)
        body = response['Body']
        lines = (line.decode('utf-8') for line in body.iter_lines(chunk_size=4 * 1024 * 1024))
        print(f"Reading started for S3 object: {self.object_key} ....")
        return csv.DictReader(lines)

