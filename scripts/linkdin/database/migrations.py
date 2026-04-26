"""
Database Migration Module
Handles database schema migrations and data transformations.
Enhanced with comprehensive logging and rollback capabilities.
"""

import logging
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
import json
import os
import shutil
from dataclasses import dataclass
from enum import Enum
import chromadb
from chromadb.config import Settings

# Set up logging
logger = logging.getLogger(__name__)

class MigrationStatus(Enum):
    """Enum for migration status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class Migration:
    """Migration definition"""
    version: str
    name: str
    description: str
    up_function: Callable
    down_function: Callable
    dependencies: List[str] = None
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.dependencies is None:
            self.dependencies = []

class DatabaseMigrator:
    """
    Database migration manager for ChromaDB collections.
    Enhanced with comprehensive logging and rollback capabilities.
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize the database migrator.
        
        Args:
            persist_directory: Directory where ChromaDB data is stored
        """
        self.persist_directory = persist_directory
        self.migrations_dir = os.path.join(persist_directory, "migrations")
        self.migrations_file = os.path.join(self.migrations_dir, "migrations.json")
        
        # Create migrations directory
        os.makedirs(self.migrations_dir, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Load migration history
        self.migration_history = self._load_migration_history()
        
        logger.info(f"DatabaseMigrator initialized for {persist_directory}")
    
    def _load_migration_history(self) -> Dict[str, Any]:
        """Load migration history from file."""
        try:
            if os.path.exists(self.migrations_file):
                with open(self.migrations_file, 'r') as f:
                    return json.load(f)
            else:
                return {
                    'migrations': [],
                    'last_migration': None,
                    'created_at': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error loading migration history: {str(e)}")
            return {
                'migrations': [],
                'last_migration': None,
                'created_at': datetime.now().isoformat()
            }
    
    def _save_migration_history(self):
        """Save migration history to file."""
        try:
            with open(self.migrations_file, 'w') as f:
                json.dump(self.migration_history, f, indent=2)
            logger.debug("Migration history saved")
        except Exception as e:
            logger.error(f"Error saving migration history: {str(e)}")
    
    def register_migration(self, migration: Migration):
        """
        Register a new migration.
        
        Args:
            migration: Migration object to register
        """
        try:
            # Check if migration already exists
            existing_migrations = [m['version'] for m in self.migration_history['migrations']]
            if migration.version in existing_migrations:
                logger.warning(f"Migration {migration.version} already exists")
                return
            
            # Add migration to history
            migration_data = {
                'version': migration.version,
                'name': migration.name,
                'description': migration.description,
                'dependencies': migration.dependencies,
                'created_at': migration.created_at,
                'status': MigrationStatus.PENDING.value,
                'applied_at': None,
                'rolled_back_at': None
            }
            
            self.migration_history['migrations'].append(migration_data)
            self._save_migration_history()
            
            logger.info(f"Registered migration: {migration.version} - {migration.name}")
            
        except Exception as e:
            logger.error(f"Error registering migration: {str(e)}")
            raise
    
    def run_migrations(self, target_version: Optional[str] = None) -> bool:
        """
        Run pending migrations.
        
        Args:
            target_version: Target migration version (None for latest)
            
        Returns:
            True if all migrations succeeded, False otherwise
        """
        try:
            logger.info("Starting migration process")
            
            # Get pending migrations
            pending_migrations = self._get_pending_migrations()
            
            if not pending_migrations:
                logger.info("No pending migrations")
                return True
            
            # Filter by target version if specified
            if target_version:
                pending_migrations = [m for m in pending_migrations if m['version'] <= target_version]
            
            # Sort by version
            pending_migrations.sort(key=lambda x: x['version'])
            
            logger.info(f"Running {len(pending_migrations)} migrations")
            
            # Run migrations
            for migration_data in pending_migrations:
                if not self._run_single_migration(migration_data):
                    logger.error(f"Migration {migration_data['version']} failed")
                    return False
            
            logger.info("All migrations completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error running migrations: {str(e)}")
            return False
    
    def _get_pending_migrations(self) -> List[Dict[str, Any]]:
        """Get list of pending migrations."""
        return [m for m in self.migration_history['migrations'] 
                if m['status'] == MigrationStatus.PENDING.value]
    
    def _run_single_migration(self, migration_data: Dict[str, Any]) -> bool:
        """
        Run a single migration.
        
        Args:
            migration_data: Migration data dictionary
            
        Returns:
            True if migration succeeded, False otherwise
        """
        try:
            version = migration_data['version']
            logger.info(f"Running migration: {version} - {migration_data['name']}")
            
            # Update status to running
            migration_data['status'] = MigrationStatus.RUNNING.value
            self._save_migration_history()
            
            # Get migration function (this would need to be implemented based on your migration system)
            migration_function = self._get_migration_function(version)
            
            if migration_function:
                # Run the migration
                migration_function()
                
                # Update status to completed
                migration_data['status'] = MigrationStatus.COMPLETED.value
                migration_data['applied_at'] = datetime.now().isoformat()
                self.migration_history['last_migration'] = version
                self._save_migration_history()
                
                logger.info(f"Migration {version} completed successfully")
                return True
            else:
                logger.error(f"Migration function not found for version {version}")
                migration_data['status'] = MigrationStatus.FAILED.value
                self._save_migration_history()
                return False
                
        except Exception as e:
            logger.error(f"Error running migration {migration_data['version']}: {str(e)}")
            migration_data['status'] = MigrationStatus.FAILED.value
            self._save_migration_history()
            return False
    
    def _get_migration_function(self, version: str) -> Optional[Callable]:
        """
        Get migration function for a specific version.
        This would need to be implemented based on your migration system.
        
        Args:
            version: Migration version
            
        Returns:
            Migration function or None
        """
        # This is a placeholder - you would implement this based on your needs
        # For example, you could have a registry of migration functions
        migration_functions = {
            "001": self._migration_001_add_job_hash,
            "002": self._migration_002_add_skills_field,
            "003": self._migration_003_add_contact_info,
        }
        
        return migration_functions.get(version)
    
    def rollback_migration(self, version: str) -> bool:
        """
        Rollback a specific migration.
        
        Args:
            version: Migration version to rollback
            
        Returns:
            True if rollback succeeded, False otherwise
        """
        try:
            logger.info(f"Rolling back migration: {version}")
            
            # Find migration
            migration_data = None
            for m in self.migration_history['migrations']:
                if m['version'] == version:
                    migration_data = m
                    break
            
            if not migration_data:
                logger.error(f"Migration {version} not found")
                return False
            
            if migration_data['status'] != MigrationStatus.COMPLETED.value:
                logger.error(f"Migration {version} is not in completed status")
                return False
            
            # Get rollback function
            rollback_function = self._get_rollback_function(version)
            
            if rollback_function:
                # Run rollback
                rollback_function()
                
                # Update status
                migration_data['status'] = MigrationStatus.ROLLED_BACK.value
                migration_data['rolled_back_at'] = datetime.now().isoformat()
                self._save_migration_history()
                
                logger.info(f"Migration {version} rolled back successfully")
                return True
            else:
                logger.error(f"Rollback function not found for version {version}")
                return False
                
        except Exception as e:
            logger.error(f"Error rolling back migration {version}: {str(e)}")
            return False
    
    def _get_rollback_function(self, version: str) -> Optional[Callable]:
        """Get rollback function for a specific version."""
        rollback_functions = {
            "001": self._rollback_001_remove_job_hash,
            "002": self._rollback_002_remove_skills_field,
            "003": self._rollback_003_remove_contact_info,
        }
        
        return rollback_functions.get(version)
    
    def get_migration_status(self) -> Dict[str, Any]:
        """
        Get current migration status.
        
        Returns:
            Dictionary containing migration status information
        """
        try:
            total_migrations = len(self.migration_history['migrations'])
            completed_migrations = len([m for m in self.migration_history['migrations'] 
                                      if m['status'] == MigrationStatus.COMPLETED.value])
            pending_migrations = len([m for m in self.migration_history['migrations'] 
                                    if m['status'] == MigrationStatus.PENDING.value])
            failed_migrations = len([m for m in self.migration_history['migrations'] 
                                   if m['status'] == MigrationStatus.FAILED.value])
            
            return {
                'total_migrations': total_migrations,
                'completed_migrations': completed_migrations,
                'pending_migrations': pending_migrations,
                'failed_migrations': failed_migrations,
                'last_migration': self.migration_history.get('last_migration'),
                'migrations': self.migration_history['migrations']
            }
            
        except Exception as e:
            logger.error(f"Error getting migration status: {str(e)}")
            return {}
    
    def create_backup(self, backup_name: Optional[str] = None) -> str:
        """
        Create a backup of the database.
        
        Args:
            backup_name: Name for the backup (None for auto-generated)
            
        Returns:
            Path to the backup directory
        """
        try:
            if not backup_name:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_dir = os.path.join(self.persist_directory, "backups", backup_name)
            os.makedirs(backup_dir, exist_ok=True)
            
            # Copy database files
            for item in os.listdir(self.persist_directory):
                if item not in ['migrations', 'backups']:
                    src = os.path.join(self.persist_directory, item)
                    dst = os.path.join(backup_dir, item)
                    
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
            
            logger.info(f"Database backup created: {backup_dir}")
            return backup_dir
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            raise
    
    def restore_backup(self, backup_path: str) -> bool:
        """
        Restore database from backup.
        
        Args:
            backup_path: Path to the backup directory
            
        Returns:
            True if restore succeeded, False otherwise
        """
        try:
            logger.info(f"Restoring database from backup: {backup_path}")
            
            if not os.path.exists(backup_path):
                logger.error(f"Backup path does not exist: {backup_path}")
                return False
            
            # Create backup of current state
            current_backup = self.create_backup("pre_restore")
            logger.info(f"Created pre-restore backup: {current_backup}")
            
            # Clear current database
            for item in os.listdir(self.persist_directory):
                if item not in ['migrations', 'backups']:
                    item_path = os.path.join(self.persist_directory, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
            
            # Restore from backup
            for item in os.listdir(backup_path):
                src = os.path.join(backup_path, item)
                dst = os.path.join(self.persist_directory, item)
                
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            
            logger.info("Database restored successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
            return False
    
    # Example migration functions
    def _migration_001_add_job_hash(self):
        """Migration 001: Add job_hash field to all documents."""
        logger.info("Running migration 001: Add job_hash field")
        
        try:
            # Get all collections
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                
                # Get all documents
                results = collection.get()
                
                if results['documents']:
                    # Update each document with job_hash
                    for i, doc_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i]
                        
                        # Generate job_hash if not present
                        if 'job_hash' not in metadata:
                            import hashlib
                            title = metadata.get('title', '')
                            company = metadata.get('company', '')
                            location = metadata.get('location', '')
                            
                            hash_string = f"{title}|{company}|{location}"
                            job_hash = hashlib.md5(hash_string.encode()).hexdigest()[:16]
                            
                            # Update metadata
                            metadata['job_hash'] = job_hash
                            
                            # Update document
                            collection.update(
                                ids=[doc_id],
                                metadatas=[metadata]
                            )
                    
                    logger.info(f"Updated {len(results['ids'])} documents in collection {collection_info.name}")
            
        except Exception as e:
            logger.error(f"Error in migration 001: {str(e)}")
            raise
    
    def _rollback_001_remove_job_hash(self):
        """Rollback migration 001: Remove job_hash field."""
        logger.info("Rolling back migration 001: Remove job_hash field")
        
        try:
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                results = collection.get()
                
                if results['documents']:
                    for i, doc_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i]
                        
                        if 'job_hash' in metadata:
                            del metadata['job_hash']
                            collection.update(
                                ids=[doc_id],
                                metadatas=[metadata]
                            )
                    
                    logger.info(f"Rolled back {len(results['ids'])} documents in collection {collection_info.name}")
            
        except Exception as e:
            logger.error(f"Error rolling back migration 001: {str(e)}")
            raise
    
    def _migration_002_add_skills_field(self):
        """Migration 002: Add skills field to all documents."""
        logger.info("Running migration 002: Add skills field")
        
        try:
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                results = collection.get()
                
                if results['documents']:
                    for i, doc_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i]
                        
                        if 'skills' not in metadata:
                            metadata['skills'] = '[]'  # Empty JSON array
                            collection.update(
                                ids=[doc_id],
                                metadatas=[metadata]
                            )
                    
                    logger.info(f"Updated {len(results['ids'])} documents in collection {collection_info.name}")
            
        except Exception as e:
            logger.error(f"Error in migration 002: {str(e)}")
            raise
    
    def _rollback_002_remove_skills_field(self):
        """Rollback migration 002: Remove skills field."""
        logger.info("Rolling back migration 002: Remove skills field")
        
        try:
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                results = collection.get()
                
                if results['documents']:
                    for i, doc_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i]
                        
                        if 'skills' in metadata:
                            del metadata['skills']
                            collection.update(
                                ids=[doc_id],
                                metadatas=[metadata]
                            )
                    
                    logger.info(f"Rolled back {len(results['ids'])} documents in collection {collection_info.name}")
            
        except Exception as e:
            logger.error(f"Error rolling back migration 002: {str(e)}")
            raise
    
    def _migration_003_add_contact_info(self):
        """Migration 003: Add contact_info field to all documents."""
        logger.info("Running migration 003: Add contact_info field")
        
        try:
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                results = collection.get()
                
                if results['documents']:
                    for i, doc_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i]
                        
                        if 'contact_info' not in metadata:
                            metadata['contact_info'] = '{}'  # Empty JSON object
                            collection.update(
                                ids=[doc_id],
                                metadatas=[metadata]
                            )
                    
                    logger.info(f"Updated {len(results['ids'])} documents in collection {collection_info.name}")
            
        except Exception as e:
            logger.error(f"Error in migration 003: {str(e)}")
            raise
    
    def _rollback_003_remove_contact_info(self):
        """Rollback migration 003: Remove contact_info field."""
        logger.info("Rolling back migration 003: Remove contact_info field")
        
        try:
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                results = collection.get()
                
                if results['documents']:
                    for i, doc_id in enumerate(results['ids']):
                        metadata = results['metadatas'][i]
                        
                        if 'contact_info' in metadata:
                            del metadata['contact_info']
                            collection.update(
                                ids=[doc_id],
                                metadatas=[metadata]
                            )
                    
                    logger.info(f"Rolled back {len(results['ids'])} documents in collection {collection_info.name}")
            
        except Exception as e:
            logger.error(f"Error rolling back migration 003: {str(e)}")
            raise

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    migrator = DatabaseMigrator("./test_chroma_db")
    
    # Register migrations
    migration_001 = Migration(
        version="001",
        name="Add job_hash field",
        description="Add job_hash field to all documents for duplicate detection",
        up_function=migrator._migration_001_add_job_hash,
        down_function=migrator._rollback_001_remove_job_hash
    )
    
    migration_002 = Migration(
        version="002",
        name="Add skills field",
        description="Add skills field to all documents",
        up_function=migrator._migration_002_add_skills_field,
        down_function=migrator._rollback_002_remove_skills_field,
        dependencies=["001"]
    )
    
    migrator.register_migration(migration_001)
    migrator.register_migration(migration_002)
    
    # Run migrations
    success = migrator.run_migrations()
    print(f"Migrations completed: {success}")
    
    # Get migration status
    status = migrator.get_migration_status()
    print(f"Migration status: {status}")
    
    # Create backup
    backup_path = migrator.create_backup()
    print(f"Backup created: {backup_path}")
