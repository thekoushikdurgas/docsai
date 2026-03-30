"""Script for debugging unused file detection logic."""
import sys
from pathlib import Path

# Add the parent directory to Python path if needed
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from scripts.unused import find_unused_files
    print("Successfully imported find_unused_files")
    files = find_unused_files()
    print(f"Found {len(files)} unused files")
except Exception as e:  # pylint: disable=broad-exception-caught
    print(f"Error: {e}")
