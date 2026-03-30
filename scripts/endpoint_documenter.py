"""Main script to discover, test, and document all API endpoints."""

import csv
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from endpoint_discovery import discover_endpoints, EndpointInfo
from endpoint_test_config import (
    OUTPUT_DIR,
    OUTPUT_CSV_PREFIX,
    OUTPUT_ERROR_LOG,
    OUTPUT_SUMMARY_JSON,
)
from endpoint_tester import (
    EndpointTester,
    TestResult,
    authenticate_admin,
    authenticate_user,
)


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(OUTPUT_ERROR_LOG),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


class EndpointDocumenter:
    """Main class to orchestrate endpoint discovery, testing, and documentation."""
    
    def __init__(self):
        self.endpoints: List[EndpointInfo] = []
        self.test_results: List[TestResult] = []
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self):
        """Run the complete documentation process."""
        logger.info("Starting API endpoint documentation process...")
        
        # Step 1: Discover endpoints
        logger.info("Step 1: Discovering endpoints...")
        self.endpoints = discover_endpoints()
        logger.info(f"Discovered {len(self.endpoints)} endpoints")
        
        # Step 2: Authenticate
        logger.info("Step 2: Authenticating...")
        user_token = authenticate_user()
        admin_token = authenticate_admin()
        
        if not user_token:
            logger.warning("Could not authenticate user. Some endpoints may fail.")
        else:
            logger.info("User authentication successful")
        
        if admin_token:
            logger.info("Admin authentication successful")
        
        # Step 3: Test endpoints
        logger.info("Step 3: Testing endpoints...")
        tester = EndpointTester(access_token=user_token, admin_token=admin_token)
        
        total = len(self.endpoints)
        for i, endpoint in enumerate(self.endpoints, 1):
            logger.info(f"Testing [{i}/{total}]: {endpoint.method} {endpoint.full_path}")
            result = tester.test_endpoint(endpoint)
            self.test_results.append(result)
            
            if result.success:
                logger.debug(f"  ✓ Success ({result.response_time_ms:.2f}ms)")
            else:
                logger.debug(f"  ✗ Failed: {result.error_message}")
        
        # Step 4: Generate CSV
        logger.info("Step 4: Generating CSV report...")
        csv_path = self._generate_csv()
        logger.info(f"CSV report saved to: {csv_path}")
        
        # Step 5: Generate summary
        logger.info("Step 5: Generating summary...")
        summary_path = self._generate_summary()
        logger.info(f"Summary saved to: {summary_path}")
        
        logger.info("Documentation process completed!")
    
    def _generate_csv(self) -> Path:
        """Generate CSV report from test results."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_filename = f"{OUTPUT_CSV_PREFIX}_{timestamp}.csv"
        csv_path = self.output_dir / csv_filename
        
        # CSV columns
        fieldnames = [
            "api_version",
            "category",
            "method",
            "endpoint",
            "description",
            "requires_auth",
            "requires_admin",
            "status_code",
            "response_time_ms",
            "success",
            "error_message",
            "test_timestamp",
        ]
        
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.test_results:
                row = {
                    "api_version": result.endpoint.api_version,
                    "category": result.endpoint.category,
                    "method": result.endpoint.method,
                    "endpoint": result.endpoint.full_path,
                    "description": result.endpoint.description,
                    "requires_auth": str(result.requires_auth).lower(),
                    "requires_admin": str(result.requires_admin).lower(),
                    "status_code": result.status_code if result.status_code else "",
                    "response_time_ms": f"{result.response_time_ms:.2f}" if result.response_time_ms else "",
                    "success": str(result.success).lower(),
                    "error_message": result.error_message or "",
                    "test_timestamp": result.test_timestamp,
                }
                writer.writerow(row)
        
        return csv_path
    
    def _generate_summary(self) -> Path:
        """Generate JSON summary with statistics."""
        summary_path = self.output_dir / OUTPUT_SUMMARY_JSON
        
        # Calculate statistics
        total = len(self.test_results)
        successful = sum(1 for r in self.test_results if r.success)
        failed = total - successful
        requires_auth = sum(1 for r in self.test_results if r.requires_auth)
        requires_admin = sum(1 for r in self.test_results if r.requires_admin)
        
        # Response time statistics
        response_times = [r.response_time_ms for r in self.test_results if r.response_time_ms > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        # Group by API version
        by_version: Dict[str, int] = {}
        for result in self.test_results:
            version = result.endpoint.api_version
            by_version[version] = by_version.get(version, 0) + 1
        
        # Group by method
        by_method: Dict[str, int] = {}
        for result in self.test_results:
            method = result.endpoint.method
            by_method[method] = by_method.get(method, 0) + 1
        
        # Group by category
        by_category: Dict[str, int] = {}
        for result in self.test_results:
            category = result.endpoint.category
            by_category[category] = by_category.get(category, 0) + 1
        
        # Status code distribution
        by_status: Dict[int, int] = {}
        for result in self.test_results:
            if result.status_code:
                by_status[result.status_code] = by_status.get(result.status_code, 0) + 1
        
        summary = {
            "generated_at": datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "total_endpoints": total,
            "successful_tests": successful,
            "failed_tests": failed,
            "success_rate": f"{(successful / total * 100):.2f}%" if total > 0 else "0%",
            "requires_authentication": requires_auth,
            "requires_admin": requires_admin,
            "response_time_stats": {
                "average_ms": round(avg_response_time, 2),
                "min_ms": round(min_response_time, 2),
                "max_ms": round(max_response_time, 2),
            },
            "by_api_version": by_version,
            "by_method": by_method,
            "by_category": by_category,
            "by_status_code": by_status,
        }
        
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        
        return summary_path


def main():
    """Main entry point."""
    try:
        documenter = EndpointDocumenter()
        documenter.run()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
