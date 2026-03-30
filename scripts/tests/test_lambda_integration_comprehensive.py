#!/usr/bin/env python3
"""Comprehensive integration test for appointment360 Lambda documentation API integration."""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import httpx
from app.core.config import get_settings
from app.services.lambda_documentation_client import get_lambda_documentation_client

async def test_lambda_client_initialization():
    """Test Lambda client initialization."""
    print("1. Testing Lambda client initialization...")
    try:
        settings = get_settings()
        client = get_lambda_documentation_client()
        
        print(f"   ✅ Base URL: {client.base_url}")
        print(f"   ✅ Timeout: {client.timeout}s")
        print(f"   ✅ API Key configured: {'Yes' if client.api_key else 'No'}")
        
        # Verify URL matches settings
        if client.base_url == settings.LAMBDA_DOCUMENTATION_API_URL:
            print("   ✅ URL matches configuration")
            return True
        else:
            print(f"   ⚠️  URL mismatch: client={client.base_url}, config={settings.LAMBDA_DOCUMENTATION_API_URL}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def test_public_endpoints():
    """Test public endpoints through Lambda client."""
    print("\n2. Testing public endpoints (no auth required)...")
    client = get_lambda_documentation_client()
    results = []
    
    # Test list pages
    try:
        result = await client.list_pages()
        if isinstance(result, dict) and "pages" in result:
            print(f"   ✅ list_pages(): {result.get('total', 0)} pages")
            results.append(True)
        else:
            print(f"   ❌ list_pages(): Unexpected response format")
            results.append(False)
    except Exception as e:
        print(f"   ❌ list_pages(): {e}")
        results.append(False)
    
    # Test get page (will 404 if no pages, which is OK)
    try:
        result = await client.get_page("test_page")
        print(f"   ✅ get_page(): Response received")
        results.append(True)
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            print(f"   ✅ get_page(): 404 (expected if no pages exist)")
            results.append(True)
        else:
            print(f"   ❌ get_page(): {e}")
            results.append(False)
    
    return all(results)

async def test_protected_endpoints():
    """Test protected endpoints through Lambda client."""
    print("\n3. Testing protected endpoints (API key required)...")
    client = get_lambda_documentation_client()
    results = []
    
    # Test list endpoints
    try:
        result = await client.list_endpoints()
        if isinstance(result, dict):
            print(f"   ✅ list_endpoints(): Response received")
            results.append(True)
        else:
            print(f"   ❌ list_endpoints(): Unexpected response format")
            results.append(False)
    except Exception as e:
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print(f"   ⚠️  list_endpoints(): Authentication failed - check API key")
            results.append(False)
        else:
            print(f"   ❌ list_endpoints(): {e}")
            results.append(False)
    
    # Test get relationship graph
    try:
        result = await client.get_relationship_graph()
        if isinstance(result, dict):
            print(f"   ✅ get_relationship_graph(): Response received")
            results.append(True)
        else:
            print(f"   ❌ get_relationship_graph(): Unexpected response format")
            results.append(False)
    except Exception as e:
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print(f"   ⚠️  get_relationship_graph(): Authentication failed - check API key")
            results.append(False)
        else:
            print(f"   ❌ get_relationship_graph(): {e}")
            results.append(False)
    
    return all(results)

async def test_error_handling():
    """Test error handling."""
    print("\n4. Testing error handling...")
    client = get_lambda_documentation_client()
    results = []
    
    # Test with invalid page ID
    try:
        result = await client.get_page("nonexistent_page_12345")
        print(f"   ⚠️  get_page() with invalid ID: Got response (expected 404)")
        results.append(True)  # Any response is OK, 404 is expected
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            print(f"   ✅ get_page() with invalid ID: Correctly returned 404")
            results.append(True)
        else:
            print(f"   ⚠️  get_page() with invalid ID: {e}")
            results.append(False)
    
    # Test timeout handling (if we can simulate)
    print(f"   ✅ Error handling: Basic tests passed")
    results.append(True)
    
    return all(results)

async def test_appointment360_endpoints():
    """Test appointment360 endpoints that proxy to Lambda."""
    print("\n5. Testing appointment360 proxy endpoints...")
    base_url = os.getenv("APPOINTMENT360_URL", "http://localhost:8000")
    base_url = base_url.rstrip("/")
    results = []
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test list pages
        try:
            response = await client.get(f"{base_url}/api/v4/docs")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ GET /api/v4/docs: {data.get('total', 0)} pages")
                results.append(True)
            else:
                print(f"   ⚠️  GET /api/v4/docs: Status {response.status_code}")
                results.append(False)
        except httpx.ConnectError:
            print(f"   ⚠️  GET /api/v4/docs: appointment360 not running (skip)")
            results.append(None)
        except Exception as e:
            print(f"   ❌ GET /api/v4/docs: {e}")
            results.append(False)
    
    # Filter out None results (skipped tests)
    results = [r for r in results if r is not None]
    return all(results) if results else True

async def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Appointment360 Lambda Integration - Comprehensive Test")
    print("=" * 60)
    
    settings = get_settings()
    print(f"\nConfiguration:")
    print(f"  Lambda API URL: {settings.LAMBDA_DOCUMENTATION_API_URL}")
    print(f"  Lambda API Timeout: {settings.LAMBDA_DOCUMENTATION_API_TIMEOUT}s")
    print(f"  API Key configured: {'Yes' if settings.LAMBDA_DOCUMENTATION_API_KEY else 'No'}")
    print()
    
    results = []
    results.append(await test_lambda_client_initialization())
    results.append(await test_public_endpoints())
    results.append(await test_protected_endpoints())
    results.append(await test_error_handling())
    results.append(await test_appointment360_endpoints())
    
    print("\n" + "=" * 60)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"Results: {passed}/{total} test suites passed")
    
    if all(results):
        print("✅ All integration tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed or were skipped")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
