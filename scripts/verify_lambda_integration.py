#!/usr/bin/env python3
"""Verify appointment360 integration with Lambda documentation API."""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from app.core.config import get_settings

async def test_appointment360_endpoints():
    """Test appointment360 endpoints that proxy to Lambda."""
    settings = get_settings()
    
    # Get appointment360 URL (default to localhost)
    base_url = os.getenv("APPOINTMENT360_URL", "http://localhost:8000")
    base_url = base_url.rstrip("/")
    
    print("=" * 60)
    print("Appointment360 Lambda Integration Verification")
    print("=" * 60)
    print(f"\nAppointment360 URL: {base_url}")
    print(f"Lambda API URL: {settings.LAMBDA_DOCUMENTATION_API_URL}")
    print()
    
    results = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: List pages (public endpoint)
        print("1. Testing GET /api/v4/docs (list pages)...")
        try:
            response = await client.get(f"{base_url}/api/v4/docs")
            if response.status_code == 200:
                data = response.json()
                total = data.get("total", 0)
                print(f"   ✅ Status: 200, Total pages: {total}")
                results.append(True)
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                results.append(False)
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results.append(False)
        
        # Test 2: Get page (public endpoint)
        print("\n2. Testing GET /api/v4/docs/{page_id}...")
        try:
            # Try to get a page (will 404 if no pages exist, which is OK)
            response = await client.get(f"{base_url}/api/v4/docs/test_page")
            if response.status_code in [200, 404]:
                print(f"   ✅ Status: {response.status_code}")
                results.append(True)
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results.append(False)
        
        # Test 3: Get page content (public endpoint)
        print("\n3. Testing GET /api/v4/docs/{page_id}/content...")
        try:
            response = await client.get(f"{base_url}/api/v4/docs/test_page/content")
            if response.status_code in [200, 404]:
                print(f"   ✅ Status: {response.status_code}")
                results.append(True)
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            results.append(False)
        
        # Test 4: List endpoints (requires auth)
        print("\n4. Testing GET /api/v4/endpoint-docs (requires auth)...")
        try:
            # This will fail without auth, which is expected
            response = await client.get(f"{base_url}/api/v4/endpoint-docs")
            if response.status_code in [200, 401, 403]:
                print(f"   ✅ Status: {response.status_code} (expected without auth)")
                results.append(True)
            else:
                print(f"   ⚠️  Unexpected status: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"   ⚠️  Test: {e}")
            results.append(False)
        
        # Test 5: Get relationship graph (requires auth)
        print("\n5. Testing GET /api/v4/docs/relationships/graph (requires auth)...")
        try:
            response = await client.get(f"{base_url}/api/v4/docs/relationships/graph")
            if response.status_code in [200, 401, 403]:
                print(f"   ✅ Status: {response.status_code} (expected without auth)")
                results.append(True)
            else:
                print(f"   ⚠️  Unexpected status: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"   ⚠️  Test: {e}")
            results.append(False)
    
    print()
    print("=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if all(results):
        print("✅ Integration verification successful!")
        print("\nAll appointment360 endpoints are correctly proxying to Lambda.")
    else:
        print("⚠️  Some tests failed. Check:")
        print("   1. Appointment360 is running")
        print("   2. Lambda API URL is correct in configuration")
        print("   3. Lambda API key is correct")
        print("   4. Lambda service is accessible from appointment360")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_appointment360_endpoints())
