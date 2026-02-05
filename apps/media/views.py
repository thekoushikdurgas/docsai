"""Media views."""
import json
import logging

from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator

from apps.core.decorators.auth import require_super_admin

logger = logging.getLogger(__name__)


@require_super_admin
def list_media_view(request):
    """List all media files."""
    from apps.core.services.s3_service import S3Service

    tab = request.GET.get('tab', 'files')

    try:
        if tab == 'n8n':
            # List n8n workflows from local filesystem
            return list_n8n_workflows_view(request)
        else:
            # List regular media files from S3
            s3_service = S3Service()

            # List media files from S3
            media_prefix = getattr(settings, 'S3_MEDIA_PREFIX', f"{settings.S3_DATA_PREFIX}media/")
            files = s3_service.list_files(prefix=media_prefix, max_keys=500)

            # Format file data
            media_files = []
            for file_info in files:
                file_key = file_info.get('key', '')
                if file_key and not file_key.endswith('/'):
                    media_files.append({
                        'name': file_key.split('/')[-1],
                        'key': file_key,
                        'size': file_info.get('size', 0),
                        'last_modified': file_info.get('last_modified'),
                        'url': s3_service.get_presigned_url(file_key) if hasattr(s3_service, 'get_presigned_url') else None
                    })

            # Pagination
            page_number = request.GET.get('page', 1)
            try:
                page_number = int(page_number)
                if page_number < 1:
                    page_number = 1
            except (ValueError, TypeError):
                page_number = 1

            paginator = Paginator(media_files, 20)
            page_obj = paginator.get_page(page_number)

            context = {
                'files': page_obj,
                'total': paginator.count,
                'current_tab': 'files',
            }
            return render(request, 'media/list.html', context)

    except Exception as e:
        logger.error(f"Error listing media files: {e}", exc_info=True)
        messages.error(request, 'An error occurred while loading media files.')
        context = {
            'files': [],
            'total': 0,
            'page_obj': None,
            'current_tab': tab,
        }
        return render(request, 'media/list.html', context)


@require_super_admin
def list_n8n_workflows_view(request):
    """List n8n workflows from local filesystem."""
    import os
    import json
    from pathlib import Path
    from apps.durgasflow.services.n8n_parser import N8nParser

    try:
        # Get n8n directory path
        base_dir = Path(settings.BASE_DIR)
        n8n_dir = base_dir / 'media' / 'n8n'

        workflows = []

        if n8n_dir.exists():
            # Walk through all subdirectories
            for root, dirs, files in os.walk(n8n_dir):
                for file in files:
                    if file.endswith('.json'):
                        file_path = Path(root) / file
                        if not file_path.exists():
                            continue
                        try:
                            if file_path.stat().st_size == 0:
                                continue
                            # Read and parse n8n workflow (some files have multiple JSON objects / Extra data)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            try:
                                n8n_data = json.loads(content)
                            except json.JSONDecodeError as e:
                                if 'Extra data' in str(e):
                                    # Parse only the first JSON object (e.g. JSONL or concatenated JSON)
                                    decoder = json.JSONDecoder()
                                    n8n_data, _ = decoder.raw_decode(content)
                                else:
                                    raise
                            if not isinstance(n8n_data, dict):
                                continue

                            # Get conversion stats
                            stats = N8nParser.get_mapping_stats(n8n_data)

                            # Create workflow entry - id is path from n8n_dir (without .json)
                            relative_to_n8n = file_path.relative_to(n8n_dir)
                            workflow_id = str(relative_to_n8n.with_suffix(''))
                            workflow_info = {
                                'id': workflow_id,
                                'name': n8n_data.get('name', file_path.stem),
                                'description': (n8n_data.get('meta') or {}).get('description', ''),
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

        # Sort by category and name
        workflows.sort(key=lambda x: (x['category'], x['name']))

        # Group by category
        categories = {}
        for workflow in workflows:
            category = workflow['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(workflow)

        context = {
            'workflows': workflows,
            'categories': categories,
            'total': len(workflows),
            'current_tab': 'n8n',
        }
        return render(request, 'media/n8n_list.html', context)

    except Exception as e:
        logger.error(f"Error listing n8n workflows: {e}", exc_info=True)
        messages.error(request, 'An error occurred while loading n8n workflows.')
        context = {
            'workflows': [],
            'categories': {},
            'total': 0,
            'current_tab': 'n8n',
        }
        return render(request, 'media/n8n_list.html', context)
