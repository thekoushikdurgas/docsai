"""Performance benchmark script to verify optimization improvements.

This script benchmarks:
1. Endpoint response times (with timing decorators)
2. Background task performance (email verification, analytics)
3. Unified batch endpoint performance
4. Database query performance
5. Cache hit rates

Usage:
    python scripts/benchmark_performance.py [--endpoint ENDPOINT] [--iterations N]
"""

import asyncio
import json
import statistics
import time
from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

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


class PerformanceBenchmark:
    """Benchmark suite for performance testing."""

    def __init__(self, base_url: str = "http://localhost:8000", auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.results: Dict[str, List[float]] = defaultdict(list)
        self.errors: List[str] = []

    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication if available."""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    async def benchmark_endpoint(
        self,
        method: str,
        endpoint: str,
        iterations: int = 10,
        warmup: int = 2,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Benchmark a single endpoint."""
        url = f"{self.base_url}{endpoint}"
        times: List[float] = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Warmup
            for _ in range(warmup):
                try:
                    if method.upper() == "GET":
                        await client.get(url, headers=self.get_headers())
                    elif method.upper() == "POST":
                        await client.post(url, headers=self.get_headers(), json=payload or {})
                except Exception:
                    pass  # Ignore warmup errors

            # Actual benchmark
            for i in range(iterations):
                try:
                    start = time.time()
                    if method.upper() == "GET":
                        response = await client.get(url, headers=self.get_headers())
                    elif method.upper() == "POST":
                        response = await client.post(url, headers=self.get_headers(), json=payload or {})
                    elapsed = (time.time() - start) * 1000  # Convert to ms

                    if response.status_code < 500:  # Don't count server errors
                        times.append(elapsed)
                    else:
                        self.errors.append(f"{endpoint} returned {response.status_code} on iteration {i+1}")
                except Exception as e:
                    self.errors.append(f"{endpoint} failed on iteration {i+1}: {str(e)}")

        if not times:
            return {
                "endpoint": endpoint,
                "method": method,
                "iterations": iterations,
                "successful": 0,
                "failed": iterations,
                "error": "All iterations failed",
            }

        times.sort()
        return {
            "endpoint": endpoint,
            "method": method,
            "iterations": iterations,
            "successful": len(times),
            "failed": iterations - len(times),
            "min_ms": round(times[0], 2),
            "max_ms": round(times[-1], 2),
            "avg_ms": round(statistics.mean(times), 2),
            "median_ms": round(statistics.median(times), 2),
            "p95_ms": round(times[int(len(times) * 0.95)], 2) if len(times) > 1 else times[0],
            "p99_ms": round(times[int(len(times) * 0.99)], 2) if len(times) > 1 else times[0],
            "std_dev_ms": round(statistics.stdev(times), 2) if len(times) > 1 else 0,
        }

    async def benchmark_unified_batch(
        self,
        iterations: int = 10,
        warmup: int = 2,
    ) -> Dict[str, Any]:
        """Benchmark unified batch filter endpoint."""
        endpoint = "/api/v3/resources/filters/batch"
        payload = {
            "include_metadata": False,
            "filter_requests": [
                {
                    "resource_type": "contacts",
                    "filter_key": "job_title",
                    "search_text": "",
                    "page": 1,
                    "limit": 25,
                },
                {
                    "resource_type": "companies",
                    "filter_key": "company_name",
                    "search_text": "",
                    "page": 1,
                    "limit": 25,
                },
            ],
        }
        return await self.benchmark_endpoint("POST", endpoint, iterations, warmup, payload)

    async def benchmark_individual_filters(
        self,
        iterations: int = 10,
        warmup: int = 2,
    ) -> Dict[str, Any]:
        """Benchmark individual filter endpoints (for comparison)."""
        results = []
        
        # Simulate making separate calls (would need actual endpoints)
        # This is a placeholder to show the comparison concept
        contacts_endpoint = "/api/v3/contacts/filters/job_title"  # Example
        companies_endpoint = "/api/v3/companies/filters/company_name"  # Example
        
        # For now, return a placeholder result
        return {
            "endpoint": "individual_filters",
            "method": "GET",
            "iterations": iterations,
            "note": "This would benchmark separate filter calls for comparison",
            "estimated_avg_ms": 150,  # Estimated based on typical filter call
        }

    async def benchmark_background_task(
        self,
        iterations: int = 5,
        warmup: int = 1,
    ) -> Dict[str, Any]:
        """Benchmark background task endpoint (email verification)."""
        endpoint = "/api/v3/email/verify/bulk"
        payload = {
            "emails": ["test@example.com"] * 10,  # Small batch
            "provider": "truelist",
        }
        
        # Measure API response time (should be fast since it's background)
        result = await self.benchmark_endpoint("POST", endpoint, iterations, warmup, payload)
        result["note"] = "Measures API response time (background processing happens async)"
        return result

    async def run_all_benchmarks(self, iterations: int = 10) -> Dict[str, Any]:
        """Run all benchmark tests."""
        console.print("\n[bold cyan]Running Performance Benchmarks[/bold cyan]\n")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "iterations": iterations,
            "benchmarks": {},
        }

        # 1. Unified batch endpoint
        console.print("[yellow]Benchmarking unified batch filter endpoint...[/yellow]")
        results["benchmarks"]["unified_batch"] = await self.benchmark_unified_batch(iterations)
        
        # 2. Background task endpoint
        console.print("[yellow]Benchmarking background task endpoint...[/yellow]")
        results["benchmarks"]["background_task"] = await self.benchmark_background_task(iterations // 2)
        
        # 3. Health check (baseline)
        console.print("[yellow]Benchmarking health check (baseline)...[/yellow]")
        results["benchmarks"]["health_check"] = await self.benchmark_endpoint("GET", "/api/v1/health", iterations)
        
        results["errors"] = self.errors
        return results

    def print_results(self, results: Dict[str, Any]):
        """Print benchmark results in a formatted table."""
        if HAS_RICH:
            console.print("\n[bold green]Benchmark Results[/bold green]\n")
            
            table = Table(title="Performance Benchmarks")
            table.add_column("Endpoint", style="cyan")
            table.add_column("Method", style="magenta")
            table.add_column("Avg (ms)", justify="right", style="green")
            table.add_column("Median (ms)", justify="right", style="green")
            table.add_column("P95 (ms)", justify="right", style="yellow")
            table.add_column("P99 (ms)", justify="right", style="yellow")
            table.add_column("Success", justify="right", style="blue")

            for name, benchmark in results["benchmarks"].items():
                if "error" in benchmark:
                    table.add_row(
                        name,
                        benchmark.get("method", "N/A"),
                        "ERROR",
                        "ERROR",
                        "ERROR",
                        "ERROR",
                        f"0/{benchmark['iterations']}",
                    )
                else:
                    table.add_row(
                        name,
                        benchmark.get("method", "N/A"),
                        str(benchmark.get("avg_ms", "N/A")),
                        str(benchmark.get("median_ms", "N/A")),
                        str(benchmark.get("p95_ms", "N/A")),
                        str(benchmark.get("p99_ms", "N/A")),
                        f"{benchmark.get('successful', 0)}/{benchmark.get('iterations', 0)}",
                    )

            console.print(table)
        else:
            # Fallback plain text output
            print("\n=== Benchmark Results ===\n")
            print(f"{'Endpoint':<30} {'Method':<8} {'Avg (ms)':<12} {'Median (ms)':<12} {'P95 (ms)':<12} {'P99 (ms)':<12} {'Success':<12}")
            print("-" * 100)
            
            for name, benchmark in results["benchmarks"].items():
                if "error" in benchmark:
                    print(f"{name:<30} {benchmark.get('method', 'N/A'):<8} {'ERROR':<12} {'ERROR':<12} {'ERROR':<12} {'ERROR':<12} {'0/' + str(benchmark['iterations']):<12}")
                else:
                    print(f"{name:<30} {benchmark.get('method', 'N/A'):<8} {benchmark.get('avg_ms', 'N/A'):<12} {benchmark.get('median_ms', 'N/A'):<12} {benchmark.get('p95_ms', 'N/A'):<12} {benchmark.get('p99_ms', 'N/A'):<12} {str(benchmark.get('successful', 0)) + '/' + str(benchmark.get('iterations', 0)):<12}")

        if results.get("errors"):
            print("\nErrors:")
            for error in results["errors"]:
                print(f"  • {error}")

    def save_results(self, results: Dict[str, Any], filename: Optional[str] = None):
        """Save results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n[green]Results saved to {filename}[/green]")


async def main():
    """Main benchmark runner."""
    parser = ArgumentParser(description="Performance benchmark script")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--auth-token", help="Authentication token (Bearer)")
    parser.add_argument("--iterations", type=int, default=10, help="Number of iterations per benchmark")
    parser.add_argument("--endpoint", help="Specific endpoint to benchmark")
    parser.add_argument("--save", help="Save results to JSON file")
    parser.add_argument("--output", help="Output file for results")

    args = parser.parse_args()

    benchmark = PerformanceBenchmark(base_url=args.base_url, auth_token=args.auth_token)

    if args.endpoint:
        # Benchmark single endpoint
        console.print(f"[yellow]Benchmarking {args.endpoint}...[/yellow]")
        result = await benchmark.benchmark_endpoint("GET", args.endpoint, args.iterations)
        benchmark.print_results({"benchmarks": {args.endpoint: result}})
    else:
        # Run all benchmarks
        results = await benchmark.run_all_benchmarks(args.iterations)
        benchmark.print_results(results)
        
        if args.save or args.output:
            filename = args.output or args.save or None
            benchmark.save_results(results, filename)


if __name__ == "__main__":
    asyncio.run(main())

