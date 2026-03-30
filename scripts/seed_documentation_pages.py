"""Seed script to populate S3 + MongoDB with documentation page content from markdown files."""

import asyncio
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.lambda_documentation_client import get_lambda_documentation_client
from app.core.config import get_settings
from app.utils.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)
lambda_client = get_lambda_documentation_client()

# Path to documentation pages directory
DOCS_DIR = Path(__file__).parent.parent.parent / "frontent" / "docs" / "pages"


def parse_markdown_file(file_path: Path) -> dict:
    """Parse markdown file and extract metadata (without content)."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise
    
    # Extract route (e.g., **Route:** `/about`)
    route_match = re.search(r'\*\*Route:\*\*\s*`?([^\n`]+)`?', content)
    route = route_match.group(1).strip() if route_match else "/"
    
    # Extract file path (e.g., **File:** `frontent/app/(marketing)/about/page.tsx`)
    file_match = re.search(r'\*\*File:\*\*\s*`?([^\n`]+)`?', content)
    file_path_str = file_match.group(1).strip() if file_match else ""
    
    # Extract authentication (e.g., **Authentication:** Not required (public marketing page))
    auth_match = re.search(r'\*\*Authentication:\*\*\s*([^\n]+)', content)
    authentication = auth_match.group(1).strip() if auth_match else "Not required"
    
    # Extract authorization (e.g., **Authorization:** Admin or Super Admin only)
    authz_match = re.search(r'\*\*Authorization:\*\*\s*([^\n]+)', content)
    authorization = authz_match.group(1).strip() if authz_match else None
    
    # Extract purpose (e.g., **Purpose:** Marketing page that tells the story...)
    purpose_match = re.search(r'\*\*Purpose:\*\*\s*([^\n]+)', content)
    purpose = purpose_match.group(1).strip() if purpose_match else ""
    
    # Generate page_id from filename (e.g., "about_page.md" -> "about_page")
    page_id = file_path.stem
    
    return {
        "page_id": page_id,
        "metadata": {
            "route": route,
            "file_path": file_path_str,
            "authentication": authentication,
            "authorization": authorization,
            "purpose": purpose,
            "last_updated": datetime.now(timezone.utc)
        },
        "created_at": datetime.now(timezone.utc)
    }


async def seed_documentation():
    """Seed all documentation pages to S3 + MongoDB via Lambda."""
    docs_prefix = settings.S3_DOCUMENTATION_PREFIX
    
    # Exclude tracking files
    exclude_patterns = [
        '_page_docs_template',
        'CSS_',
        'DOCUMENTATION_',
        'FINAL_',
        'IMPLEMENTATION_',
        'PROGRESS_',
        'page_docs_coverage',
        'sidebar_'
    ]
    
    markdown_files = [
        f for f in DOCS_DIR.glob("*.md")
        if not any(pattern in f.name for pattern in exclude_patterns)
    ]
    
    print(f"Found {len(markdown_files)} documentation files to seed\n")
    
    created_count = 0
    updated_count = 0
    error_count = 0
    
    for idx, file_path in enumerate(sorted(markdown_files), 1):
        try:
            # Parse markdown file (metadata only, content read separately)
            content = file_path.read_text(encoding='utf-8')
            data = parse_markdown_file(file_path)
            page_id = data["page_id"]
            
            # Generate S3 key
            s3_key = f"{docs_prefix}{page_id}.md"
            data["metadata"]["s3_key"] = s3_key
            
            # Check if page exists
            try:
                existing = await lambda_client.get_page(page_id)
                if existing:
                    print(f"[{idx}/{len(markdown_files)}] Updating via Lambda: {page_id}")
                    # Update via Lambda
                    update_data = {
                        "metadata": data["metadata"],
                        "content": content
                    }
                    await lambda_client.update_page(page_id, update_data)
                    updated_count += 1
                else:
                    raise Exception("Page not found")
            except Exception:
                # Page doesn't exist, create it
                print(f"[{idx}/{len(markdown_files)}] Creating via Lambda: {page_id}")
                page_data = {
                    "page_id": page_id,
                    "metadata": data["metadata"],
                    "content": content
                }
                await lambda_client.create_page(page_data)
                created_count += 1
                
        except Exception as e:
            error_count += 1
            logger.error(f"Error processing {file_path.name}: {e}")
            print(f"[{idx}/{len(markdown_files)}] ERROR: {file_path.name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Seeding complete!")
    print(f"  Created:  {created_count}")
    print(f"  Updated:  {updated_count}")
    print(f"  Errors:   {error_count}")
    print(f"  Total:    {len(markdown_files)}")
    print(f"  S3 Path:  s3://{settings.S3_BUCKET_NAME}/{docs_prefix}")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(seed_documentation())
