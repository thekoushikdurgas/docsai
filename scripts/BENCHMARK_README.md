# Performance Benchmark Scripts

This directory contains scripts for benchmarking and comparing performance improvements.

## Scripts

### `benchmark_performance.py`

Comprehensive performance benchmark script that tests:
- Endpoint response times (with timing decorators)
- Unified batch filter endpoint performance
- Background task endpoint performance (email verification, analytics)
- Health check baseline

**Usage:**

```bash
# Run all benchmarks
python scripts/benchmark_performance.py --base-url http://localhost:8000 --iterations 10

# Benchmark specific endpoint
python scripts/benchmark_performance.py --endpoint /api/v1/health --iterations 20

# With authentication
python scripts/benchmark_performance.py --auth-token YOUR_TOKEN --iterations 10

# Save results to file
python scripts/benchmark_performance.py --iterations 10 --save results.json
```

**Output:**
- Console table with min, max, avg, median, P95, P99 response times
- JSON file with detailed results (if --save specified)

### `benchmark_comparison.py`

Compare performance before and after optimizations.

**Usage:**

```bash
# Compare two benchmark runs
python scripts/benchmark_comparison.py --before before_results.json --after after_results.json

# Save comparison to file
python scripts/benchmark_comparison.py --before before.json --after after.json --output comparison.json
```

**Output:**
- Console table showing improvement percentages and speedup
- Summary statistics (average improvement, speedup)
- JSON file with comparison data (if --output specified)

## Dependencies

Install required dependencies:

```bash
pip install httpx rich
```

Or add to `requirements.txt`:
```
httpx>=0.27.2
rich>=13.0.0
```

## Example Workflow

1. **Before optimizations:**
   ```bash
   python scripts/benchmark_performance.py --iterations 20 --save before_optimization.json
   ```

2. **After optimizations:**
   ```bash
   python scripts/benchmark_performance.py --iterations 20 --save after_optimization.json
   ```

3. **Compare results:**
   ```bash
   python scripts/benchmark_comparison.py --before before_optimization.json --after after_optimization.json
   ```

## Metrics Explained

- **Min/Max**: Fastest and slowest response times
- **Avg**: Average response time across all iterations
- **Median**: Middle value (50th percentile)
- **P95**: 95th percentile (95% of requests are faster)
- **P99**: 99th percentile (99% of requests are faster)
- **Std Dev**: Standard deviation (measure of variance)

## Performance Targets

Based on our optimizations, target metrics:

- **Health check**: < 10ms
- **Unified batch filters**: < 200ms (vs 300-500ms for individual calls)
- **Background task endpoints**: < 100ms (API response, processing happens async)
- **Regular endpoints**: < 500ms (with timing decorators)

## Notes

- Benchmarks include warmup iterations to account for cold starts
- Results may vary based on system load, network conditions, and database state
- For accurate comparisons, run benchmarks under similar conditions
- Background task benchmarks measure API response time, not processing time

