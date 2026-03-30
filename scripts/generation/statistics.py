"""
Thread-safe statistics tracking for data generation.

This module provides a statistics tracker that can be safely used across
multiple threads and processes.
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GeneratorStatistics:
    """Thread-safe statistics tracker for data generation."""
    
    # Counters (protected by lock)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _pg_companies_indexed: int = 0
    _pg_companies_failed: int = 0
    _pg_contacts_indexed: int = 0
    _pg_contacts_failed: int = 0
    _es_companies_indexed: int = 0
    _es_companies_failed: int = 0
    _es_contacts_indexed: int = 0
    _es_contacts_failed: int = 0
    _batches_completed: int = 0
    
    # Timing
    start_time: Optional[float] = None
    total_batches: int = 0
    
    def start(self, total_batches: int) -> None:
        """Start timing and initialize total batches."""
        with self._lock:
            self.start_time = time.time()
            self.total_batches = total_batches
    
    def add_pg_companies(self, success: int, failed: int) -> None:
        """Add PostgreSQL company statistics."""
        with self._lock:
            self._pg_companies_indexed += success
            self._pg_companies_failed += failed
    
    def add_pg_contacts(self, success: int, failed: int) -> None:
        """Add PostgreSQL contact statistics."""
        with self._lock:
            self._pg_contacts_indexed += success
            self._pg_contacts_failed += failed
    
    def add_es_companies(self, success: int, failed: int) -> None:
        """Add Elasticsearch company statistics."""
        with self._lock:
            self._es_companies_indexed += success
            self._es_companies_failed += failed
    
    def add_es_contacts(self, success: int, failed: int) -> None:
        """Add Elasticsearch contact statistics."""
        with self._lock:
            self._es_contacts_indexed += success
            self._es_contacts_failed += failed
    
    def increment_batches(self) -> None:
        """Increment completed batches counter."""
        with self._lock:
            self._batches_completed += 1
    
    def get_stats(self) -> dict:
        """Get current statistics as a dictionary."""
        with self._lock:
            elapsed = time.time() - self.start_time if self.start_time else 0
            total_records = (
                self._pg_companies_indexed + self._pg_contacts_indexed +
                self._es_companies_indexed + self._es_contacts_indexed
            )
            records_per_sec = total_records / elapsed if elapsed > 0 else 0
            
            return {
                "batches_completed": self._batches_completed,
                "total_batches": self.total_batches,
                "pg_companies_indexed": self._pg_companies_indexed,
                "pg_companies_failed": self._pg_companies_failed,
                "pg_contacts_indexed": self._pg_contacts_indexed,
                "pg_contacts_failed": self._pg_contacts_failed,
                "es_companies_indexed": self._es_companies_indexed,
                "es_companies_failed": self._es_companies_failed,
                "es_contacts_indexed": self._es_contacts_indexed,
                "es_contacts_failed": self._es_contacts_failed,
                "elapsed_seconds": elapsed,
                "records_per_second": records_per_sec,
            }
    
    def print_progress(self) -> None:
        """Print current progress statistics."""
        stats = self.get_stats()
        
        print("\n========== Current Stats ==========")
        print(f"Batches: {stats['batches_completed']}/{stats['total_batches']}")
        print(f"PG Companies - Success: {stats['pg_companies_indexed']:,}, Failed: {stats['pg_companies_failed']:,}")
        print(f"PG Contacts  - Success: {stats['pg_contacts_indexed']:,}, Failed: {stats['pg_contacts_failed']:,}")
        print(f"ES Companies - Success: {stats['es_companies_indexed']:,}, Failed: {stats['es_companies_failed']:,}")
        print(f"ES Contacts  - Success: {stats['es_contacts_indexed']:,}, Failed: {stats['es_contacts_failed']:,}")
        
        if stats['elapsed_seconds'] > 0:
            elapsed_str = f"{stats['elapsed_seconds']:.1f}s"
            rate = f"{stats['records_per_second']:.2f}"
            print(f"Time Elapsed: {elapsed_str}, Rate: {rate} records/sec")
        
        print("====================================\n")
    
    def print_final(self) -> None:
        """Print final statistics report."""
        stats = self.get_stats()
        
        print("\n==============================================")
        print("              FINAL RESULTS                   ")
        print("==============================================")
        
        elapsed = stats['elapsed_seconds']
        if elapsed > 0:
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            if hours > 0:
                elapsed_str = f"{hours}h {minutes}m {seconds}s"
            elif minutes > 0:
                elapsed_str = f"{minutes}m {seconds}s"
            else:
                elapsed_str = f"{seconds}s"
            
            print(f"Time Elapsed: {elapsed_str}")
            print(f"Records per second: {stats['records_per_second']:.2f}")
        
        print(f"\nBatches: {stats['batches_completed']}/{stats['total_batches']}")
        print(f"\nPostgreSQL:")
        print(f"  Companies - Success: {stats['pg_companies_indexed']:,}, Failed: {stats['pg_companies_failed']:,}")
        print(f"  Contacts  - Success: {stats['pg_contacts_indexed']:,}, Failed: {stats['pg_contacts_failed']:,}")
        print(f"\nElasticsearch:")
        print(f"  Companies - Success: {stats['es_companies_indexed']:,}, Failed: {stats['es_companies_failed']:,}")
        print(f"  Contacts  - Success: {stats['es_contacts_indexed']:,}, Failed: {stats['es_contacts_failed']:,}")
        
        total_success = (
            stats['pg_companies_indexed'] + stats['pg_contacts_indexed'] +
            stats['es_companies_indexed'] + stats['es_contacts_indexed']
        )
        total_failed = (
            stats['pg_companies_failed'] + stats['pg_contacts_failed'] +
            stats['es_companies_failed'] + stats['es_contacts_failed']
        )
        total = total_success + total_failed
        success_rate = (total_success / total * 100) if total > 0 else 0
        
        print(f"\nTotal Records: {total:,}")
        print(f"Success Rate: {success_rate:.2f}%")
        print("==============================================")
        print("              COMPLETED!                      ")
        print("==============================================\n")

