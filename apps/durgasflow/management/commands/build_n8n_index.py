"""Django management command to build n8n workflow index."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.durgasflow.services.n8n_library_service import N8nWorkflowLibraryService
from apps.durgasflow.services.n8n_parser import N8nParser

logger = logging.getLogger(__name__)

# Non-workflow JSON files to exclude from scanning
EXCLUDE_FILENAMES = frozenset({
    'package.json', 'tsconfig.json', 'package-lock.json',
    'composer.json', 'bower.json', '.eslintrc.json',
    'index.json',  # Don't include the index itself
})


def _load_n8n_json(file_path: Path) -> dict | None:
    """Load n8n workflow JSON; return None on failure."""
    try:
        content = file_path.read_text(encoding='utf-8').strip()
    except (OSError, FileNotFoundError):
        return None
    if not content:
        return None
    try:
        data = json.loads(content)
        if isinstance(data, dict) and 'nodes' in data and isinstance(data.get('nodes'), list):
            return data
    except json.JSONDecodeError:
        try:
            decoder = json.JSONDecoder()
            obj, _ = decoder.raw_decode(content)
            if isinstance(obj, dict) and 'nodes' in obj and isinstance(obj.get('nodes'), list):
                return obj
        except json.JSONDecodeError:
            pass
    return None


class Command(BaseCommand):
    """Build index.json for n8n workflows in media/n8n directory."""

    help = 'Scan media/n8n for workflow JSON files and build index.json for fast listing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Rebuild index even if it appears up to date',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help='Limit number of workflows to index (0 = no limit)',
        )

    def handle(self, *args, **options):
        n8n_dir = N8nWorkflowLibraryService.get_n8n_dir()
        base_dir = Path(settings.BASE_DIR)
        index_path = n8n_dir / 'index.json'

        if not n8n_dir.exists():
            self.stdout.write(self.style.WARNING(f'n8n directory does not exist: {n8n_dir}'))
            return

        workflows = []
        categories_count = {}

        for file_path in sorted(n8n_dir.rglob('*.json')):
            if file_path.name in EXCLUDE_FILENAMES:
                continue

            n8n_data = _load_n8n_json(file_path)
            if n8n_data is None:
                continue

            try:
                stats = N8nParser.get_mapping_stats(n8n_data)
                relative_to_n8n = file_path.relative_to(n8n_dir)
                workflow_id = str(relative_to_n8n.with_suffix('')).replace('\\', '/')
                n8n_path_str = str(relative_to_n8n).replace('\\', '/')

                meta = n8n_data.get('meta')
                description = (meta.get('description', '') if isinstance(meta, dict) else '') or ''

                category = str(relative_to_n8n.parts[0]) if len(relative_to_n8n.parts) > 1 else file_path.parent.name
                categories_count[category] = categories_count.get(category, 0) + 1

                workflow_info = {
                    'id': workflow_id,
                    'name': n8n_data.get('name', file_path.stem),
                    'description': description[:500] if description else '',
                    'category': category,
                    'n8n_path': n8n_path_str,
                    'node_count': len(n8n_data.get('nodes') or []),
                    'conversion_stats': stats,
                    'is_supported': stats.get('conversion_confidence', 0) > 0.8,
                    'size': file_path.stat().st_size,
                    'last_modified': int(file_path.stat().st_mtime),
                }
                workflows.append(workflow_info)

                if options['limit'] and len(workflows) >= options['limit']:
                    break

            except Exception as e:
                logger.warning("Failed to index %s: %s", file_path, e)
                continue

        workflows.sort(key=lambda x: (x['category'], x['name']))
        now = datetime.now(timezone.utc).isoformat()

        index_data = {
            'version': '2.0',
            'last_updated': now,
            'total': len(workflows),
            'workflows': workflows,
            'categories': categories_count,
        }

        index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

        self.stdout.write(
            self.style.SUCCESS(
                f'Built n8n index: {len(workflows)} workflows, '
                f'{len(categories_count)} categories -> {index_path}'
            )
        )
