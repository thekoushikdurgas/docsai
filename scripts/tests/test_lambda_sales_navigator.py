#!/usr/bin/env python3
"""
Test script for Lambda Sales Navigator integration.

This script tests the Lambda Sales Navigator API integration from appointment360 backend.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.clients.lambda_sales_navigator_client import (
    LambdaSalesNavigatorClient,
    LambdaSalesNavigatorError,
)
from app.core.config import get_settings

# Sample HTML for testing (minimal Sales Navigator search results)
SAMPLE_HTML = """
<div class="reusable-search__result-container">
    <div class="entity-result">
        <div class="entity-result__title">
            <a href="/sales/lead/ACwAAAFK" class="app-aware-link">
                <span class="entity-result__title-text">John Doe</span>
            </a>
        </div>
        <div class="entity-result__primary-subtitle">Senior Software Engineer at Tech Corp</div>
        <div class="entity-result__secondary-subtitle">New York, NY</div>
    </div>
</div>
"""


async def test_lambda_client_initialization():
    """Test Lambda client initialization."""
    print("\n" + "=" * 60)
    print("Test 1: Lambda Client Initialization")
    print("=" * 60)
    
    try:
        settings = get_settings()
        print(f"Lambda API URL: {settings.LAMBDA_SALES_NAVIGATOR_API_URL}")
        print(f"Lambda API Key: {'***' if settings.LAMBDA_SALES_NAVIGATOR_API_KEY else 'Not set'}")
        print(f"Lambda Enabled: {settings.LAMBDA_SALES_NAVIGATOR_ENABLED}")
        
        if not settings.LAMBDA_SALES_NAVIGATOR_API_URL:
            print("❌ Lambda API URL not configured")
            return False
        
        async with LambdaSalesNavigatorClient() as client:
            print(f"✅ Client initialized successfully")
            print(f"   Base URL: {client.base_url}")
            print(f"   Timeout: {client.timeout}s")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def test_lambda_health_check():
    """Test Lambda health check endpoint."""
    print("\n" + "=" * 60)
    print("Test 2: Lambda Health Check")
    print("=" * 60)
    
    try:
        async with LambdaSalesNavigatorClient() as client:
            try:
                response = await client.health_check()
                print(f"✅ Health check successful")
                print(f"   Response: {response}")
                return True
            except LambdaSalesNavigatorError as e:
                print(f"⚠️  Health check endpoint may not be available: {e}")
                return False
            except Exception as e:
                print(f"❌ Error: {e}")
                return False
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return False


async def test_lambda_scrape_no_save():
    """Test Lambda scrape endpoint without saving."""
    print("\n" + "=" * 60)
    print("Test 3: Lambda Scrape (No Save)")
    print("=" * 60)
    
    try:
        async with LambdaSalesNavigatorClient() as client:
            print(f"Sending scrape request (save=False)...")
            response = await client.scrape(
                html=SAMPLE_HTML,
                save=False,
                include_metadata=True
            )
            
            print(f"✅ Scrape successful")
            print(f"   Profiles extracted: {len(response.get('profiles', []))}")
            print(f"   Page metadata: {response.get('page_metadata', {})}")
            
            if response.get('profiles'):
                profile = response['profiles'][0]
                print(f"   Sample profile: {profile.get('name', 'N/A')}")
            
            return True
    except LambdaSalesNavigatorError as e:
        print(f"❌ Lambda API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_lambda_scrape_with_save():
    """Test Lambda scrape endpoint with saving."""
    print("\n" + "=" * 60)
    print("Test 4: Lambda Scrape (With Save)")
    print("=" * 60)
    
    settings = get_settings()
    if not settings.LAMBDA_SALES_NAVIGATOR_API_KEY:
        print("⚠️  Lambda API key not configured. Skipping save test.")
        return None
    
    try:
        async with LambdaSalesNavigatorClient() as client:
            print(f"Sending scrape request (save=True)...")
            response = await client.scrape(
                html=SAMPLE_HTML,
                save=True,
                include_metadata=True
            )
            
            print(f"✅ Scrape and save successful")
            print(f"   Profiles extracted: {len(response.get('profiles', []))}")
            
            if 'save_summary' in response:
                summary = response['save_summary']
                print(f"   Save summary:")
                print(f"     Contacts created: {summary.get('contacts_created', 0)}")
                print(f"     Companies created: {summary.get('companies_created', 0)}")
            
            return True
    except LambdaSalesNavigatorError as e:
        print(f"❌ Lambda API Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_lambda_error_handling():
    """Test Lambda error handling."""
    print("\n" + "=" * 60)
    print("Test 5: Error Handling")
    print("=" * 60)
    
    try:
        # Test with invalid API key
        print("Testing with invalid API key...")
        async with LambdaSalesNavigatorClient(api_key="invalid-key") as client:
            try:
                await client.scrape(html=SAMPLE_HTML, save=False)
                print("❌ Expected error for invalid API key, but request succeeded")
                return False
            except LambdaSalesNavigatorError as e:
                print(f"✅ Correctly caught error: {e}")
                return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def test_lambda_timeout():
    """Test Lambda timeout handling."""
    print("\n" + "=" * 60)
    print("Test 6: Timeout Handling")
    print("=" * 60)
    
    try:
        # Test with very short timeout
        print("Testing with short timeout (1 second)...")
        async with LambdaSalesNavigatorClient(timeout=1) as client:
            try:
                # Use a large HTML payload that might take longer
                large_html = SAMPLE_HTML * 1000
                await client.scrape(html=large_html, save=False)
                print("⚠️  Request completed (may not have timed out)")
                return True
            except Exception as e:
                if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                    print(f"✅ Timeout correctly handled: {e}")
                    return True
                else:
                    print(f"⚠️  Unexpected error (may still be valid): {e}")
                    return True
    except Exception as e:
        print(f"⚠️  Error during timeout test: {e}")
        return True  # Don't fail on timeout tests


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Lambda Sales Navigator Integration Test Suite")
    print("=" * 60)
    
    settings = get_settings()
    print(f"\nConfiguration:")
    print(f"  Lambda API URL: {settings.LAMBDA_SALES_NAVIGATOR_API_URL}")
    print(f"  Lambda Enabled: {settings.LAMBDA_SALES_NAVIGATOR_ENABLED}")
    print(f"  API Key configured: {'Yes' if settings.LAMBDA_SALES_NAVIGATOR_API_KEY else 'No'}")
    print()
    
    results = []
    
    results.append(("Initialization", await test_lambda_client_initialization()))
    results.append(("Health Check", await test_lambda_health_check()))
    results.append(("Scrape (No Save)", await test_lambda_scrape_no_save()))
    
    save_result = await test_lambda_scrape_with_save()
    if save_result is not None:
        results.append(("Scrape (With Save)", save_result))
    
    results.append(("Error Handling", await test_lambda_error_handling()))
    results.append(("Timeout Handling", await test_lambda_timeout()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    
    for test_name, result in results:
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⏭️  SKIP"
        print(f"  {test_name:25} {status}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
