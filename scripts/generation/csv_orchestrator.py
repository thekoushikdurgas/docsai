"""
CSV orchestrator for processing CSV files through dual-write flow.

This module orchestrates the processing of CSV files, writing to both
PostgreSQL and Elasticsearch using the same writers as the generator.
"""

import threading
import queue
import signal
from typing import List, Generator

from .config import GeneratorConfig
from .models import GeneratedBatch
from .statistics import GeneratorStatistics
from .writers.postgres_writer import PostgresWriter
from .writers.elasticsearch_writer import ElasticsearchWriter
from .csv_processor import process_csv_file
from .csv_streaming_processor import process_csv_streaming


class CSVOrchestrator:
    """Orchestrator for processing CSV files through dual-write flow."""
    
    def __init__(self, config: GeneratorConfig):
        """
        Initialize the CSV orchestrator.
        
        Args:
            config: Generator configuration (for ES settings and thread counts)
        """
        self.config = config
        self.stats = GeneratorStatistics()
        self.shutdown_event = threading.Event()
        
        # Queues for communication
        self.pg_queue: queue.Queue = queue.Queue(maxsize=config.queue_buffer_size)
        self.es_queue: queue.Queue = queue.Queue(maxsize=config.queue_buffer_size)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\n\nShutdown signal received. Finishing current batches...")
        self.shutdown_event.set()
    
    def _fanout_worker(self, batch_generator: Generator[GeneratedBatch, None, None]) -> None:
        """Fanout worker that distributes batches to PG and ES queues."""
        try:
            for batch in batch_generator:
                if self.shutdown_event.is_set():
                    break
                # Send to both queues
                self.pg_queue.put(batch)
                self.es_queue.put(batch)
        except Exception as e:
            print(f"Fanout worker error: {e}")
    
    def _pg_writer_worker(self, worker_id: int) -> None:
        """
        Worker thread for writing to PostgreSQL.
        
        Args:
            worker_id: Worker identifier for logging
        """
        writer = PostgresWriter()
        
        try:
            while not self.shutdown_event.is_set() or not self.pg_queue.empty():
                try:
                    batch: GeneratedBatch = self.pg_queue.get(timeout=1)
                except queue.Empty:
                    continue
                
                # Insert companies
                company_success, company_failed = writer.bulk_insert_companies(batch.companies)
                self.stats.add_pg_companies(company_success, company_failed)
                
                # Insert contacts
                contact_success, contact_failed = writer.bulk_insert_contacts(batch.contacts)
                self.stats.add_pg_contacts(contact_success, contact_failed)
                
                print(f"PG Writer {worker_id}: Batch {batch.batch_num + 1} - "
                      f"Companies: {company_success}, Contacts: {contact_success}")
        
        except Exception as e:
            print(f"PG Writer {worker_id} error: {e}")
        finally:
            writer.close()
            print(f"PG Writer {worker_id}: Finished")
    
    def _es_writer_worker(self, worker_id: int) -> None:
        """
        Worker thread for writing to Elasticsearch.
        
        Args:
            worker_id: Worker identifier for logging
        """
        writer = ElasticsearchWriter(
            host=self.config.es_host,
            port=self.config.es_port,
            username=self.config.es_username,
            password=self.config.es_password
        )
        writer.set_indices(self.config.es_companies_index, self.config.es_contacts_index)
        
        try:
            while not self.shutdown_event.is_set() or not self.es_queue.empty():
                try:
                    batch: GeneratedBatch = self.es_queue.get(timeout=1)
                except queue.Empty:
                    continue
                
                # Index companies
                company_success, company_failed = writer.bulk_index_companies(batch.elastic_companies)
                self.stats.add_es_companies(company_success, company_failed)
                
                # Index contacts
                contact_success, contact_failed = writer.bulk_index_contacts(batch.elastic_contacts)
                self.stats.add_es_contacts(contact_success, contact_failed)
                
                # Increment batch counter
                self.stats.increment_batches()
                
                print(f"ES Writer {worker_id}: Batch {batch.batch_num + 1} - "
                      f"Companies: {company_success}, Contacts: {contact_success}")
        
        except Exception as e:
            print(f"ES Writer {worker_id} error: {e}")
    
    def _progress_reporter(self) -> None:
        """Background thread for reporting progress."""
        while not self.shutdown_event.is_set():
            self.shutdown_event.wait(10)  # Wait 10 seconds or until shutdown
            if not self.shutdown_event.is_set():
                self.stats.print_progress()
    
    def run(self, csv_path: str, use_streaming: bool = True) -> None:
        """
        Run the CSV processing pipeline.
        
        Args:
            csv_path: Path to the CSV file
            use_streaming: If True, use streaming mode for large files (default: True)
        """
        import os
        
        print("\n==============================================")
        print("     CSV Processor - Companies & Contacts    ")
        print("==============================================")
        print(f"CSV File: {csv_path}")
        
        # Check file size to determine if streaming is needed
        file_size = os.path.getsize(csv_path)
        file_size_mb = file_size / (1024 * 1024)
        file_size_gb = file_size / (1024 * 1024 * 1024)
        
        if file_size_gb >= 1:
            print(f"File Size: {file_size_gb:.2f} GB")
        else:
            print(f"File Size: {file_size_mb:.2f} MB")
        
        # Auto-enable streaming for files > 100MB
        if file_size > 100 * 1024 * 1024:  # 100MB
            use_streaming = True
            print("Large file detected - using streaming mode")
        else:
            use_streaming = False
            print("Using standard mode")
        
        print(f"PostgreSQL Threads: {self.config.num_pg_threads}")
        print(f"Elasticsearch Threads: {self.config.num_es_threads}")
        print(f"Batch Size: {self.config.batch_size}")
        print(f"Target: PostgreSQL + Elasticsearch\n")
        
        # Create Elasticsearch indices first
        print("Creating Elasticsearch indices...")
        try:
            es_writer = ElasticsearchWriter(
                host=self.config.es_host,
                port=self.config.es_port,
                username=self.config.es_username,
                password=self.config.es_password
            )
            es_writer.set_indices(self.config.es_companies_index, self.config.es_contacts_index)
            es_writer.create_indices()
            print("Elasticsearch indices created successfully!")
        except Exception as e:
            print(f"Warning: Could not create Elasticsearch indices: {e}")
            print("Continuing anyway...")
        
        # Process CSV file
        if use_streaming:
            # Streaming mode: process and write incrementally
            print("\nStarting streaming CSV processing...")
            batch_generator = process_csv_streaming(
                csv_path,
                batch_size=self.config.batch_size,
                progress_callback=lambda r, c, cont: None  # Progress shown in processor
            )
            
            # Initialize statistics (we don't know total batches yet)
            self.stats.start(0)  # Will be updated as batches are processed
            
            # Start fanout worker (distributes batches to PG and ES queues)
            print("Starting fanout worker...")
            fanout_thread = threading.Thread(target=self._fanout_worker, args=(batch_generator,))
            fanout_thread.daemon = True
            fanout_thread.start()
        else:
            # Standard mode: load all batches first (for small files)
            print("\nProcessing CSV file...")
            batches = process_csv_file(csv_path, batch_size=self.config.batch_size)
            
            if not batches:
                print("No data found in CSV file.")
                return
            
            total_companies = sum(len(batch.companies) for batch in batches)
            total_contacts = sum(len(batch.contacts) for batch in batches)
            
            print(f"\nTotal Companies: {total_companies:,}")
            print(f"Total Contacts: {total_contacts:,}")
            print(f"Total Batches: {len(batches)}\n")
            
            # Initialize statistics
            self.stats.start(len(batches))
            
            # Start fanout worker (distributes batches to PG and ES queues)
            print("Starting fanout worker...")
            fanout_thread = threading.Thread(target=self._fanout_worker, args=(iter(batches),))
            fanout_thread.daemon = True
            fanout_thread.start()
        
        # Start PostgreSQL writer threads
        print("Starting PostgreSQL writer threads...")
        pg_threads = []
        for i in range(self.config.num_pg_threads):
            thread = threading.Thread(target=self._pg_writer_worker, args=(i + 1,))
            thread.daemon = True
            thread.start()
            pg_threads.append(thread)
        
        # Start Elasticsearch writer threads
        print("Starting Elasticsearch writer threads...")
        es_threads = []
        for i in range(self.config.num_es_threads):
            thread = threading.Thread(target=self._es_writer_worker, args=(i + 1,))
            thread.daemon = True
            thread.start()
            es_threads.append(thread)
        
        # Start progress reporter
        progress_thread = threading.Thread(target=self._progress_reporter)
        progress_thread.daemon = True
        progress_thread.start()
        
        # Wait for fanout to finish
        fanout_thread.join()
        
        print("All batches distributed. Waiting for writers to complete...")
        
        # Wait for all writer threads to finish
        for thread in pg_threads:
            thread.join()
        
        for thread in es_threads:
            thread.join()
        
        # Signal shutdown to progress reporter
        self.shutdown_event.set()
        progress_thread.join(timeout=1)
        
        # Print final statistics
        self.stats.print_final()

