"""
Orchestrator for coordinating data generation and writing.

This module manages the producer-consumer architecture with multiprocessing
for data generation and threading for database writes.
"""

import multiprocessing
import threading
import queue
import signal
import sys
from typing import Optional

from .config import GeneratorConfig
from .generators import generate_batch
from .models import GeneratedBatch
from .statistics import GeneratorStatistics
from .writers.postgres_writer import PostgresWriter
from .writers.elasticsearch_writer import ElasticsearchWriter


class GeneratorOrchestrator:
    """Orchestrator for managing the data generation pipeline."""
    
    def __init__(self, config: GeneratorConfig):
        """
        Initialize the orchestrator.
        
        Args:
            config: Generator configuration
        """
        self.config = config
        self.stats = GeneratorStatistics()
        self.shutdown_event = threading.Event()
        
        # Queues for communication
        # Generator processes put batches here
        self.generated_queue: multiprocessing.Queue = multiprocessing.Queue(maxsize=config.queue_buffer_size)
        # Fanout thread distributes to these
        self.pg_queue: queue.Queue = queue.Queue(maxsize=config.queue_buffer_size)
        self.es_queue: queue.Queue = queue.Queue(maxsize=config.queue_buffer_size)
        
        # Writer instances (will be created per thread)
        self.es_writer = ElasticsearchWriter(
            host=config.es_host,
            port=config.es_port,
            username=config.es_username,
            password=config.es_password
        )
        self.es_writer.set_indices(config.es_companies_index, config.es_contacts_index)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\n\nShutdown signal received. Finishing current batches...")
        self.shutdown_event.set()
    
    @staticmethod
    def _generator_worker(
        start_batch: int,
        end_batch: int,
        worker_id: int,
        batch_size: int,
        contacts_per_company: int,
        generated_queue: multiprocessing.Queue
    ) -> None:
        """
        Worker process for generating batches.
        
        Args:
            start_batch: First batch number to generate
            end_batch: Last batch number (exclusive)
            worker_id: Worker identifier for logging
            batch_size: Number of companies per batch
            contacts_per_company: Number of contacts per company
            generated_queue: Queue to put generated batches
        """
        try:
            for batch_num in range(start_batch, end_batch):
                batch = generate_batch(
                    batch_num=batch_num,
                    batch_size=batch_size,
                    contacts_per_company=contacts_per_company
                )
                
                generated_queue.put(batch)
                
                if (batch_num + 1) % 100 == 0:
                    print(f"Generator {worker_id}: Generated {batch_num + 1} batches")
        
        except Exception as e:
            print(f"Generator {worker_id} error: {e}")
        finally:
            print(f"Generator {worker_id}: Finished")
    
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
                
                # Increment batch counter (only once per batch, use ES as the counter)
                self.stats.increment_batches()
                
                print(f"ES Writer {worker_id}: Batch {batch.batch_num + 1} - "
                      f"Companies: {company_success}, Contacts: {contact_success}")
        
        except Exception as e:
            print(f"ES Writer {worker_id} error: {e}")
    
    def _fanout_worker(self) -> None:
        """Fanout worker that distributes batches to PG and ES queues."""
        try:
            while not self.shutdown_event.is_set() or not self.generated_queue.empty():
                try:
                    batch: GeneratedBatch = self.generated_queue.get(timeout=1)
                    # Send to both queues
                    self.pg_queue.put(batch)
                    self.es_queue.put(batch)
                except queue.Empty:
                    continue
        except Exception as e:
            print(f"Fanout worker error: {e}")
    
    def _progress_reporter(self) -> None:
        """Background thread for reporting progress."""
        while not self.shutdown_event.is_set():
            self.shutdown_event.wait(10)  # Wait 10 seconds or until shutdown
            if not self.shutdown_event.is_set():
                self.stats.print_progress()
    
    def run(self) -> None:
        """Run the data generation pipeline."""
        print("\n==============================================")
        print("     Data Generator - Companies & Contacts    ")
        print("==============================================")
        print(f"Total Companies: {self.config.total_companies:,}")
        print(f"Contacts per Company: {self.config.contacts_per_company}")
        print(f"Total Contacts: {self.config.total_contacts:,}")
        print(f"Batch Size (Companies): {self.config.batch_size}")
        print(f"Total Batches: {self.config.total_batches}")
        print(f"Generator Processes: {self.config.num_generator_processes}")
        print(f"PostgreSQL Threads: {self.config.num_pg_threads}")
        print(f"Elasticsearch Threads: {self.config.num_es_threads}\n")
        
        # Initialize statistics
        self.stats.start(self.config.total_batches)
        
        # Create Elasticsearch indices
        print("Creating Elasticsearch indices...")
        try:
            self.es_writer.create_indices()
            print("Elasticsearch indices created successfully!")
        except Exception as e:
            print(f"Warning: Could not create Elasticsearch indices: {e}")
            print("Continuing anyway...")
        
        # Calculate batches per generator process
        batches_per_process = self.config.total_batches // self.config.num_generator_processes
        
        # Start generator processes
        print("\nStarting generator processes...")
        generator_processes = []
        for i in range(self.config.num_generator_processes):
            start_batch = i * batches_per_process
            end_batch = start_batch + batches_per_process
            if i == self.config.num_generator_processes - 1:
                end_batch = self.config.total_batches  # Last process handles remaining batches
            
            process = multiprocessing.Process(
                target=self._generator_worker,
                args=(
                    start_batch,
                    end_batch,
                    i + 1,
                    self.config.batch_size,
                    self.config.contacts_per_company,
                    self.generated_queue
                )
            )
            process.start()
            generator_processes.append(process)
        
        # Start fanout worker (distributes batches to PG and ES queues)
        print("Starting fanout worker...")
        fanout_thread = threading.Thread(target=self._fanout_worker)
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
        
        # Wait for all generator processes to finish
        print("\nWaiting for generators to complete...")
        for process in generator_processes:
            process.join()
        
        print("All generators finished. Waiting for writers to complete...")
        
        # Wait for fanout to finish
        fanout_thread.join()
        
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

