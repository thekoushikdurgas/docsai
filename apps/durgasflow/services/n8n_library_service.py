"""N8n Workflow Library Service - discovers and lists n8n workflows from media directory."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from django.conf import settings

from .n8n_parser import N8nParser
from .n8n_models import parse_index, parse_workflow

logger = logging.getLogger(__name__)


def _try_deduplicated_path(file_path: Path) -> Optional[Path]:
    """
    If the filename looks like 'NameName.json' (duplicated), try 'Name.json' in the same directory.
    Returns a path that exists, or None.
    """
    stem = file_path.stem
    if len(stem) < 2:
        return None
    half = len(stem) // 2
    if stem[:half] == stem[half:]:
        candidate = file_path.parent / (stem[:half] + file_path.suffix)
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def _load_n8n_json(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load n8n workflow JSON from file, handling malformed files gracefully.
    Handles: Extra data (multiple JSON objects), Expecting value (empty), FileNotFoundError.
    When the filename appears duplicated (e.g. NameName.json), tries Name.json in the same dir.
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except (OSError, FileNotFoundError):
        fallback = _try_deduplicated_path(file_path)
        if fallback is not None:
            try:
                content = fallback.read_text(encoding='utf-8')
            except (OSError, FileNotFoundError) as e:
                logger.warning("Failed to read n8n workflow %s: %s", file_path, e)
                return None
        else:
            logger.warning("Failed to read n8n workflow %s: No such file or directory", file_path)
            return None

    content = content.strip()
    if not content:
        logger.debug(f"Skipping empty file: {file_path}")
        return None

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        if "Expecting value" in str(e):
            logger.debug(f"Skipping non-JSON file: {file_path}")
            return None
        if "Extra data" in str(e):
            # File contains multiple JSON objects - extract first valid workflow
            try:
                decoder = json.JSONDecoder()
                obj, _ = decoder.raw_decode(content)
                if isinstance(obj, dict) and 'nodes' in obj:
                    return obj
            except json.JSONDecodeError:
                pass
        logger.warning(f"Failed to parse JSON in {file_path}: {e}")
        return None


class N8nWorkflowLibraryService:
    """Service for discovering and listing n8n workflows from media/n8n directory."""

    _INDEX_PATH = 'index.json'

    @classmethod
    def _get_index_path(cls) -> Path:
        """Path to index.json in n8n directory."""
        return cls.get_n8n_dir() / cls._INDEX_PATH

    @classmethod
    def _load_from_index(cls) -> Optional[List[Dict[str, Any]]]:
        """
        Load workflows from pre-built index.json if it exists and has content.
        Uses n8n_models.parse_index for validation. Returns None if missing or invalid.
        """
        index_path = cls._get_index_path()
        if not index_path.exists() or not index_path.is_file():
            return None
        try:
            raw = json.loads(index_path.read_text(encoding='utf-8'))
            data = parse_index(raw)
            if data is None:
                return None
            workflows = data.get('workflows', [])
            n8n_dir = cls.get_n8n_dir()
            for w in workflows:
                n8n_path = (w.get('n8n_path') or w.get('id', '') + '.json').replace('\\', '/')
                w['file_path'] = str(n8n_dir / n8n_path)
                w['relative_path'] = f"media/n8n/{n8n_path}"
            return workflows
        except Exception as e:
            logger.debug("Failed to load n8n index: %s", e)
            return None

    @classmethod
    def load_workflow_file(cls, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load n8n workflow from file. Handles malformed JSON gracefully.
        Returns normalized workflow dict (via n8n_models.parse_workflow) or None on failure.
        """
        raw = _load_n8n_json(file_path)
        return parse_workflow(raw) if raw else None

    @classmethod
    def get_n8n_dir(cls) -> Path:
        """Get the n8n workflows directory path."""
        return Path(settings.BASE_DIR) / 'media' / 'n8n'

    @classmethod
    def resolve_workflow_path(cls, file_path: Path) -> Optional[Path]:
        """
        Return a path that exists for the given workflow file path.
        If the path does not exist but a deduplicated filename does (e.g. NameName.json -> Name.json), return that.
        """
        if file_path.exists() and file_path.is_file():
            return file_path
        fallback = _try_deduplicated_path(file_path)
        return fallback if (fallback and fallback.exists() and fallback.is_file()) else None

    @classmethod
    def list_workflows(cls, use_index: bool = True) -> List[Dict[str, Any]]:
        """
        Discover and list all n8n workflows from media/n8n directory.
        When use_index is True, reads from index.json if available and non-empty.
        Otherwise scans the directory (slower with many files).

        Returns:
            List of workflow dicts with id, name, description, category, etc.
        """
        if use_index:
            from_index = cls._load_from_index()
            if from_index is not None:
                return from_index

        n8n_dir = cls.get_n8n_dir()
        base_dir = Path(settings.BASE_DIR)
        workflows = []

        if not n8n_dir.exists():
            return workflows

        for file_path in n8n_dir.rglob('*.json'):
            try:
                n8n_data = _load_n8n_json(file_path)
                if n8n_data is None:
                    continue

                stats = N8nParser.get_mapping_stats(n8n_data)
                relative_to_n8n = file_path.relative_to(n8n_dir)
                workflow_id = str(relative_to_n8n.with_suffix(''))

                # Handle meta being None (n8nworkflows.xyz format has "meta": null)
                meta = n8n_data.get('meta')
                description = (meta.get('description', '') if isinstance(meta, dict) else '') or ''

                workflow_info = {
                    'id': workflow_id,
                    'name': n8n_data.get('name', file_path.stem),
                    'description': description,
                    'file_path': str(file_path),
                    'relative_path': str(file_path.relative_to(base_dir)),
                    'n8n_path': str(relative_to_n8n),
                    'size': file_path.stat().st_size,
                    'last_modified': file_path.stat().st_mtime,
                    'category': str(relative_to_n8n.parts[0]) if len(relative_to_n8n.parts) > 1 else file_path.parent.name,
                    'node_count': len(n8n_data.get('nodes') or []),
                    'conversion_stats': stats,
                    'is_supported': stats['conversion_confidence'] > 0.8,
                }
                workflows.append(workflow_info)

            except Exception as e:
                logger.warning(f"Failed to parse n8n workflow {file_path}: {e}")
                continue

        workflows.sort(key=lambda x: (x['category'], x['name']))
        return workflows

    @classmethod
    def get_categories(cls, workflows: Optional[List[Dict]] = None) -> Dict[str, List[Dict]]:
        """Group workflows by category."""
        if workflows is None:
            workflows = cls.list_workflows()
        categories = {}
        for workflow in workflows:
            category = workflow['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(workflow)
        return categories

    @classmethod
    def get_featured(cls, limit: int = 4) -> List[Dict[str, Any]]:
        """Get featured workflows (high conversion confidence)."""
        workflows = cls.list_workflows()
        featured = [w for w in workflows if w.get('is_supported')][:limit]
        return featured
