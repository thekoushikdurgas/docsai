"""Compare performance before and after optimizations.

This script helps verify that optimizations improved performance by:
1. Comparing endpoint response times
2. Comparing batch vs individual API calls
3. Comparing background task response times
4. Analyzing cache hit rates

Usage:
    python scripts/benchmark_comparison.py --before before_results.json --after after_results.json
"""

import json
from argparse import ArgumentParser
from typing import Dict, List

try:
    from rich.console import Console
    from rich.table import Table
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    # Fallback console
    class SimpleConsole:
        def print(self, *args, **kwargs):
            print(*args)
    console = SimpleConsole()


def load_results(filename: str) -> Dict:
    """Load benchmark results from JSON file."""
    with open(filename, "r") as f:
        return json.load(f)


def calculate_improvement(before: float, after: float) -> Dict[str, any]:
    """Calculate performance improvement metrics."""
    if before == 0:
        return {"improvement_pct": 0, "speedup": 1.0, "status": "no_change"}
    
    improvement_pct = ((before - after) / before) * 100
    speedup = before / after if after > 0 else float('inf')
    
    if improvement_pct > 10:
        status = "excellent"
    elif improvement_pct > 5:
        status = "good"
    elif improvement_pct > 0:
        status = "improved"
    elif improvement_pct > -5:
        status = "acceptable"
    else:
        status = "regression"
    
    return {
        "improvement_pct": round(improvement_pct, 2),
        "speedup": round(speedup, 2),
        "status": status,
    }


def compare_benchmarks(before_results: Dict, after_results: Dict) -> List[Dict]:
    """Compare before and after benchmark results."""
    comparisons = []
    
    before_benchmarks = before_results.get("benchmarks", {})
    after_benchmarks = after_results.get("benchmarks", {})
    
    # Compare common benchmarks
    common_keys = set(before_benchmarks.keys()) & set(after_benchmarks.keys())
    
    for key in common_keys:
        before = before_benchmarks[key]
        after = after_benchmarks[key]
        
        if "avg_ms" in before and "avg_ms" in after:
            improvement = calculate_improvement(before["avg_ms"], after["avg_ms"])
            comparisons.append({
                "benchmark": key,
                "before_avg_ms": before["avg_ms"],
                "after_avg_ms": after["avg_ms"],
                **improvement,
            })
    
    return comparisons


def print_comparison(comparisons: List[Dict]):
    """Print comparison results in a formatted table."""
    if HAS_RICH:
        console.print("\n[bold green]Performance Comparison[/bold green]\n")
        
        table = Table(title="Before vs After Optimization")
        table.add_column("Benchmark", style="cyan")
        table.add_column("Before (ms)", justify="right", style="red")
        table.add_column("After (ms)", justify="right", style="green")
        table.add_column("Improvement", justify="right", style="yellow")
        table.add_column("Speedup", justify="right", style="blue")
        table.add_column("Status", style="magenta")

        for comp in comparisons:
            status_emoji = {
                "excellent": "✅",
                "good": "✓",
                "improved": "→",
                "acceptable": "⚠",
                "regression": "❌",
            }.get(comp["status"], "?")
            
            table.add_row(
                comp["benchmark"],
                str(comp["before_avg_ms"]),
                str(comp["after_avg_ms"]),
                f"{comp['improvement_pct']}%",
                f"{comp['speedup']}x",
                f"{status_emoji} {comp['status']}",
            )

        console.print(table)
    else:
        # Fallback plain text output
        print("\n=== Performance Comparison ===\n")
        print(f"{'Benchmark':<30} {'Before (ms)':<15} {'After (ms)':<15} {'Improvement':<15} {'Speedup':<10} {'Status':<15}")
        print("-" * 100)
        
        for comp in comparisons:
            status_emoji = {
                "excellent": "[EXCELLENT]",
                "good": "[GOOD]",
                "improved": "[IMPROVED]",
                "acceptable": "[OK]",
                "regression": "[REGRESSION]",
            }.get(comp["status"], "[?]")
            
            print(f"{comp['benchmark']:<30} {comp['before_avg_ms']:<15} {comp['after_avg_ms']:<15} {comp['improvement_pct']}%{'':<10} {comp['speedup']}x{'':<6} {status_emoji}")
    
    # Summary statistics
    if comparisons:
        avg_improvement = sum(c["improvement_pct"] for c in comparisons) / len(comparisons)
        avg_speedup = sum(c["speedup"] for c in comparisons) / len(comparisons)
        
        print(f"\nSummary:")
        print(f"  Average Improvement: {avg_improvement:.2f}%")
        print(f"  Average Speedup: {avg_speedup:.2f}x")
        
        excellent_count = sum(1 for c in comparisons if c["status"] == "excellent")
        good_count = sum(1 for c in comparisons if c["status"] == "good")
        regression_count = sum(1 for c in comparisons if c["status"] == "regression")
        
        print(f"  Excellent improvements: {excellent_count}")
        print(f"  Good improvements: {good_count}")
        if regression_count > 0:
            print(f"  Regressions: {regression_count}")


def main():
    """Main comparison runner."""
    parser = ArgumentParser(description="Compare performance benchmarks")
    parser.add_argument("--before", required=True, help="Before optimization results JSON file")
    parser.add_argument("--after", required=True, help="After optimization results JSON file")
    parser.add_argument("--output", help="Save comparison to JSON file")

    args = parser.parse_args()

    console.print("[yellow]Loading benchmark results...[/yellow]")
    before_results = load_results(args.before)
    after_results = load_results(args.after)

    console.print("[yellow]Comparing benchmarks...[/yellow]")
    comparisons = compare_benchmarks(before_results, after_results)

    print_comparison(comparisons)

    if args.output:
        with open(args.output, "w") as f:
            json.dump({
                "before_file": args.before,
                "after_file": args.after,
                "comparisons": comparisons,
            }, f, indent=2)
        console.print(f"\n[green]Comparison saved to {args.output}[/green]")


if __name__ == "__main__":
    main()

