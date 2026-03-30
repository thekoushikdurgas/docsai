"""Script to automatically add @timed_endpoint decorator to all endpoint functions.

This script scans all endpoint files and adds the @timed_endpoint() decorator
before each @router decorator if it's not already present.

Usage:
    python scripts/add_timing_to_endpoints.py
"""

import re
from pathlib import Path


def add_timing_decorator_to_file(file_path: Path) -> bool:
    """
    Add @timed_endpoint decorator to all endpoints in a file.
    
    Returns:
        True if file was modified, False otherwise
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Check if timed_endpoint is already imported
        has_import = 'from app.utils.endpoint_timing import timed_endpoint' in content
        has_import_alt = 'from app.utils.endpoint_timing import' in content
        
        # Check if file already has decorators
        has_decorator = '@timed_endpoint()' in content
        
        # Find all @router decorators
        router_pattern = r'(@router\.(?:get|post|put|delete|patch|head|options)\s*\([^)]*\))'
        
        # Find all endpoint function definitions
        endpoint_pattern = r'(@router\.(?:get|post|put|delete|patch|head|options)\s*\([^)]*\))\s*\n(async def|def)\s+(\w+)\s*\('
        
        matches = list(re.finditer(endpoint_pattern, content, re.MULTILINE))
        
        if not matches:
            return False
        
        # Add import if needed
        if not has_import and not has_import_alt:
            # Find the last import statement
            import_pattern = r'(from app\.utils\.logger import.*)'
            import_match = re.search(import_pattern, content)
            if import_match:
                # Add import after logger import
                import_line = import_match.group(0)
                new_import = import_line + '\nfrom app.utils.endpoint_timing import timed_endpoint'
                content = content.replace(import_line, new_import)
            else:
                # Try to find any from app.utils import
                utils_import_pattern = r'(from app\.utils\.[^\s]+ import[^\n]*)'
                utils_match = re.search(utils_import_pattern, content)
                if utils_match:
                    import_line = utils_match.group(0)
                    new_import = import_line + '\nfrom app.utils.endpoint_timing import timed_endpoint'
                    content = content.replace(import_line, new_import)
                else:
                    # Add at the top after other imports
                    lines = content.split('\n')
                    last_import_idx = 0
                    for i, line in enumerate(lines):
                        if line.startswith('from ') or line.startswith('import '):
                            last_import_idx = i
                    lines.insert(last_import_idx + 1, 'from app.utils.endpoint_timing import timed_endpoint')
                    content = '\n'.join(lines)
        
        # Add decorators before each @router decorator
        # Process in reverse to maintain positions
        for match in reversed(matches):
            router_decorator = match.group(1)
            func_def = match.group(2) + ' ' + match.group(3)
            
            # Check if decorator already exists
            start_pos = match.start()
            # Look backwards for @timed_endpoint
            before_text = content[:start_pos]
            if '@timed_endpoint()' in before_text[-200:]:  # Check last 200 chars before this match
                continue
            
            # Add decorator
            replacement = f'{router_decorator}\n@timed_endpoint()\n{func_def}'
            content = content[:match.start()] + replacement + content[match.end():]
        
        # Only write if content changed
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all endpoint files."""
    base_path = Path('appointment360/app/api')
    
    # Find all endpoint files
    endpoint_files = []
    for version_dir in ['v1', 'v2', 'v3', 'v4']:
        endpoints_dir = base_path / version_dir / 'endpoints'
        if endpoints_dir.exists():
            endpoint_files.extend(endpoints_dir.glob('*.py'))
    
    # Filter out __init__.py
    endpoint_files = [f for f in endpoint_files if f.name != '__init__.py']
    
    print(f"Found {len(endpoint_files)} endpoint files")
    
    modified_count = 0
    for file_path in sorted(endpoint_files):
        if add_timing_decorator_to_file(file_path):
            print(f"Modified: {file_path}")
            modified_count += 1
        else:
            print(f"Skipped (already has decorators or no endpoints): {file_path}")
    
    print(f"\nModified {modified_count} files")


if __name__ == '__main__':
    main()

