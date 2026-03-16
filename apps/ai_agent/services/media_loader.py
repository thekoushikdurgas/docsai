"""Media file loader service for loading documentation from S3 via documentation services."""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class MediaFileLoaderService:
    """Service for loading documentation from S3 (via documentation services)."""
    
    def __init__(self):
        """Initialize media file loader (S3-backed)."""
        logger.debug("MediaFileLoaderService initialized (S3)")
    
    def load_all_pages(self) -> List[Dict[str, Any]]:
        """Load all pages from S3 (via pages service)."""
        try:
            from apps.documentation.services import get_pages_service
            result = get_pages_service().list_pages(limit=None, offset=0)
            return result.get("pages", [])
        except Exception as e:
            logger.error(f"Error loading all pages: {e}")
            return []
    
    def load_all_endpoints(self) -> List[Dict[str, Any]]:
        """Load all endpoints from S3 (via endpoints service)."""
        try:
            from apps.documentation.services import get_endpoints_service
            result = get_endpoints_service().list_endpoints(limit=None, offset=0)
            return result.get("endpoints", [])
        except Exception as e:
            logger.error(f"Error loading all endpoints: {e}")
            return []
    
    def load_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Load a single page from S3."""
        try:
            from apps.documentation.services import get_pages_service
            return get_pages_service().get_page(page_id)
        except Exception as e:
            logger.error(f"Error loading page {page_id}: {e}")
            return None
    
    def load_endpoint(self, endpoint_id: str) -> Optional[Dict[str, Any]]:
        """Load a single endpoint from S3."""
        try:
            from apps.documentation.services import get_endpoints_service
            return get_endpoints_service().get_endpoint(endpoint_id)
        except Exception as e:
            logger.error(f"Error loading endpoint {endpoint_id}: {e}")
            return None
    
    def load_relationships_by_page(self, page_path: str) -> Optional[Dict[str, Any]]:
        """Load relationships for a page from S3."""
        try:
            from apps.documentation.services import get_shared_unified_storage
            return get_shared_unified_storage().get_relationships_by_page(page_path)
        except Exception as e:
            logger.error(f"Error loading relationships for page {page_path}: {e}")
            return None
    
    def load_relationships_by_endpoint(
        self,
        endpoint_path: str,
        method: str = "QUERY"
    ) -> Optional[Dict[str, Any]]:
        """Load relationships for an endpoint from S3."""
        try:
            from apps.documentation.services import get_shared_unified_storage
            return get_shared_unified_storage().get_relationships_by_endpoint(endpoint_path, method)
        except Exception as e:
            logger.error(f"Error loading relationships for endpoint {endpoint_path}: {e}")
            return None
    
    def load_postman_collections(self) -> List[Dict[str, Any]]:
        """Load Postman collections from S3 (list collection keys and read each)."""
        try:
            from apps.documentation.services import get_shared_s3_storage
            from django.conf import settings
            s3_storage = get_shared_s3_storage()
            prefix = f"{settings.S3_DATA_PREFIX}postman/collection/"
            keys = s3_storage.list_json_files(prefix, max_keys=500)
            collections = []
            for key in keys:
                data = s3_storage.read_json(key)
                if data:
                    collections.append(data)
            return collections
        except Exception as e:
            logger.error(f"Error loading Postman collections: {e}")
            return []
    
    def load_project_docs(self) -> List[Dict[str, Any]]:
        """Load project documentation files. Returns [] (project docs not in S3 in this setup)."""
        return []
    
    def get_index(self, resource_type: str) -> Dict[str, Any]:
        """Get index data for a resource type from S3 index manager (for semantic_search/ai_service)."""
        try:
            from apps.documentation.services import get_shared_s3_index_manager
            index_manager = get_shared_s3_index_manager()
            return index_manager.read_index(resource_type)
        except Exception as e:
            logger.error(f"Error loading index for {resource_type}: {e}")
            return {}
