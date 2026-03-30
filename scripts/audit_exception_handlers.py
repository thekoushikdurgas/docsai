"""Audit empty exception handlers in the codebase.

Categorizes empty exception handlers by:
1. Acceptable (intentional fallback, non-critical)
2. Problematic (swallowing errors silently)
3. Needs review (context-dependent)
"""

import re
import os
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict

def find_empty_exception_handlers(root_dir: str = "app") -> List[Tuple[str, int, str, str]]:
    """Find all empty exception handlers."""
    results = []
    
    for root, dirs, files in os.walk(root_dir):
        # Skip __pycache__ and other non-code directories
        dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith(".")]
        
        for file in files:
            if not file.endswith(".py"):
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    
                for i, line in enumerate(lines):
                    # Check for "except ...: pass" on same line
                    if re.search(r'except\s+.*:\s*pass\s*$', line):
                        results.append((filepath, i + 1, line.strip(), "same_line"))
                    
                    # Check for "except ...:" followed by "pass" on next line
                    elif re.search(r'except\s+.*:\s*$', line) and i + 1 < len(lines):
                        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                        if next_line == "pass":
                            # Get context (2 lines before and after)
                            context_start = max(0, i - 2)
                            context_end = min(len(lines), i + 4)
                            context = "".join(lines[context_start:context_end])
                            results.append((filepath, i + 1, line.strip(), context))
                            
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    
    return results

def categorize_handler(filepath: str, line_num: int, line: str, context: str) -> str:
    """Categorize exception handler as acceptable, problematic, or needs review."""
    line_lower = line.lower()
    context_lower = context.lower()
    
    # Acceptable patterns
    acceptable_patterns = [
        "jsondecodeerror",  # JSON parsing fallbacks
        "modulenotfounderror",  # Optional imports
        "importerror",  # Optional imports
        "keyerror",  # Dictionary access fallbacks
        "typeerror",  # Type conversion fallbacks
        "valueerror",  # Value parsing fallbacks (sometimes)
    ]
    
    # Problematic patterns
    problematic_patterns = [
        "exception:",  # Too broad, swallows all errors
        "except:",  # Bare except
    ]
    
    # Check for acceptable
    for pattern in acceptable_patterns:
        if pattern in line_lower:
            # Additional check: should have specific exception type
            if "exception" not in line_lower or pattern in line_lower:
                return "acceptable"
    
    # Check for problematic
    for pattern in problematic_patterns:
        if pattern in line_lower:
            return "problematic"
    
    # Check context for clues
    if "fallback" in context_lower or "optional" in context_lower:
        return "acceptable"
    
    if "log" in context_lower or "logger" in context_lower:
        return "needs_review"  # Might be logging elsewhere
    
    return "needs_review"

def main():
    """Main analysis function."""
    print("=" * 80)
    print("Empty Exception Handler Audit")
    print("=" * 80)
    print()
    
    handlers = find_empty_exception_handlers()
    
    print(f"Total empty exception handlers found: {len(handlers)}")
    print()
    
    # Categorize
    categories = defaultdict(list)
    for filepath, line_num, line, context in handlers:
        category = categorize_handler(filepath, line_num, line, context)
        categories[category].append((filepath, line_num, line, context))
    
    # Report by category
    print("=" * 80)
    print("CATEGORIZATION")
    print("=" * 80)
    print(f"Acceptable (intentional fallback): {len(categories['acceptable'])}")
    print(f"Problematic (swallows errors): {len(categories['problematic'])}")
    print(f"Needs Review (context-dependent): {len(categories['needs_review'])}")
    print()
    
    # Detailed report
    if categories['problematic']:
        print("=" * 80)
        print("PROBLEMATIC HANDLERS (Should be fixed)")
        print("=" * 80)
        for filepath, line_num, line, context in categories['problematic']:
            print(f"\n{filepath}:{line_num}")
            print(f"  {line}")
            print(f"  Context: {context[:200]}...")
    
    if categories['needs_review']:
        print("\n" + "=" * 80)
        print("NEEDS REVIEW (Context-dependent)")
        print("=" * 80)
        for filepath, line_num, line, context in categories['needs_review'][:10]:  # First 10
            print(f"\n{filepath}:{line_num}")
            print(f"  {line}")
            print(f"  Context: {context[:200]}...")
    
    # Save detailed report
    report_file = Path("cleanup_diffs/exception_handlers_audit.txt")
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("Empty Exception Handler Audit Report\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Total: {len(handlers)}\n")
        f.write(f"Acceptable: {len(categories['acceptable'])}\n")
        f.write(f"Problematic: {len(categories['problematic'])}\n")
        f.write(f"Needs Review: {len(categories['needs_review'])}\n\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("PROBLEMATIC HANDLERS\n")
        f.write("=" * 80 + "\n\n")
        for filepath, line_num, line, context in categories['problematic']:
            f.write(f"{filepath}:{line_num}\n")
            f.write(f"  {line}\n")
            f.write(f"  Context:\n{context}\n\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("NEEDS REVIEW\n")
        f.write("=" * 80 + "\n\n")
        for filepath, line_num, line, context in categories['needs_review']:
            f.write(f"{filepath}:{line_num}\n")
            f.write(f"  {line}\n")
            f.write(f"  Context:\n{context}\n\n")
    
    print(f"\nDetailed report saved to: {report_file}")

if __name__ == "__main__":
    main()
