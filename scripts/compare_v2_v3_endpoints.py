"""Compare v2 and v3 endpoint files to identify differences.

This script compares duplicate endpoint files between v2 and v3 to identify
exact differences and help decide which version to keep.
"""

import difflib
import sys
from pathlib import Path

# Files to compare
COMPARISONS = [
    ("app/api/v2/endpoints/contacts.py", "app/api/v3/endpoints/contacts.py"),
    ("app/api/v2/endpoints/email.py", "app/api/v3/endpoints/email.py"),
    ("app/api/v2/endpoints/exports.py", "app/api/v3/endpoints/exports.py"),
    ("app/api/v2/endpoints/activities.py", "app/api/v3/endpoints/activities.py"),
    ("app/api/v2/endpoints/linkedin.py", "app/api/v3/endpoints/linkedin.py"),
    ("app/api/v2/endpoints/sales_navigator.py", "app/api/v3/endpoints/sales_navigator.py"),
]

# Check if unified exists in both
if Path("app/api/v2/endpoints/unified.py").exists() and Path("app/api/v3/endpoints/unified.py").exists():
    COMPARISONS.append(("app/api/v2/endpoints/unified.py", "app/api/v3/endpoints/unified.py"))


def compare_files(file1_path: str, file2_path: str) -> dict:
    """Compare two files and return statistics."""
    try:
        with open(file1_path, "r", encoding="utf-8") as f1:
            lines1 = f1.readlines()
        with open(file2_path, "r", encoding="utf-8") as f2:
            lines2 = f2.readlines()
    except FileNotFoundError as e:
        return {"error": str(e)}

    # Generate diff
    diff = list(
        difflib.unified_diff(
            lines1, lines2, fromfile=file1_path, tofile=file2_path, n=3
        )
    )

    # Count differences
    additions = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    context_lines = sum(1 for line in diff if line.startswith(" "))

    # Check if files are identical
    is_identical = additions == 0 and deletions == 0

    return {
        "file1": file1_path,
        "file2": file2_path,
        "file1_lines": len(lines1),
        "file2_lines": len(lines2),
        "additions": additions,
        "deletions": deletions,
        "is_identical": is_identical,
        "diff": diff[:100] if not is_identical else [],  # First 100 lines of diff
    }


def main():
    """Main comparison function."""
    print("=" * 80)
    print("v2 vs v3 Endpoint File Comparison")
    print("=" * 80)
    print()

    results = []
    for file1, file2 in COMPARISONS:
        print(f"Comparing: {Path(file1).name} vs {Path(file2).name}")
        result = compare_files(file1, file2)

        if "error" in result:
            print(f"  ❌ Error: {result['error']}")
            continue

        results.append(result)

        if result["is_identical"]:
            print(f"  ✅ IDENTICAL ({result['file1_lines']} lines)")
        else:
            print(f"  ⚠️  DIFFERENT")
            print(f"     v2: {result['file1_lines']} lines")
            print(f"     v3: {result['file2_lines']} lines")
            print(f"     +{result['additions']} additions, -{result['deletions']} deletions")

        print()

    # Summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    identical_count = sum(1 for r in results if r.get("is_identical", False))
    different_count = len(results) - identical_count

    print(f"Total files compared: {len(results)}")
    print(f"Identical: {identical_count}")
    print(f"Different: {different_count}")

    # Save detailed diff to file
    output_file = Path("cleanup_diffs/comparison_summary.txt")
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("v2 vs v3 Endpoint Comparison Summary\n")
        f.write("=" * 80 + "\n\n")

        for result in results:
            if "error" in result:
                continue

            f.write(f"\n{result['file1']} vs {result['file2']}\n")
            f.write("-" * 80 + "\n")
            if result["is_identical"]:
                f.write("STATUS: IDENTICAL\n")
            else:
                f.write(f"STATUS: DIFFERENT\n")
                f.write(f"v2 lines: {result['file1_lines']}\n")
                f.write(f"v3 lines: {result['file2_lines']}\n")
                f.write(f"Additions: {result['additions']}\n")
                f.write(f"Deletions: {result['deletions']}\n")
                f.write("\nFirst 100 lines of diff:\n")
                f.write("".join(result["diff"]))

    print(f"\nDetailed comparison saved to: {output_file}")

    # Generate individual diff files
    print("\nGenerating individual diff files...")
    diff_dir = Path("cleanup_diffs")
    diff_dir.mkdir(exist_ok=True)

    for file1, file2 in COMPARISONS:
        try:
            with open(file1, "r", encoding="utf-8") as f1:
                lines1 = f1.readlines()
            with open(file2, "r", encoding="utf-8") as f2:
                lines2 = f2.readlines()

            diff = list(
                difflib.unified_diff(
                    lines1, lines2, fromfile=file1, tofile=file2, n=3
                )
            )

            filename = Path(file1).stem
            diff_file = diff_dir / f"{filename}.diff"
            with open(diff_file, "w", encoding="utf-8") as f:
                f.writelines(diff)

            print(f"  ✅ {diff_file.name}")
        except FileNotFoundError:
            print(f"  ⚠️  Skipped {Path(file1).name} (file not found)")


if __name__ == "__main__":
    main()
