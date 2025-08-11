#!/usr/bin/env python3
"""
Vercel Deployment Test Script
Tests the deployed API on Vercel platform
"""

import asyncio
import httpx
import json
import time


async def test_vercel_deployment(base_url: str):
    """Test the Vercel-deployed API"""
    
    print(f"Testing Vercel deployment at: {base_url}")
    print("=" * 60)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5"
    }
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        try:
            # Test 1: Root endpoint
            print("1. Testing root endpoint...")
            response = await client.get(f"{base_url}/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test 2: Health check
            print("\n2. Testing health endpoint...")
            response = await client.get(f"{base_url}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            # Test 3: Main API endpoint
            print("\n3. Testing main API endpoint...")
            test_request = {
                "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
                "questions": [
                    "What is the grace period for premium payment?",
                    "What is the waiting period for pre-existing diseases?"
                ]
            }
            
            print("   Request payload:")
            print(f"   {json.dumps(test_request, indent=2)}")
            
            start_time = time.time()
            response = await client.post(
                f"{base_url}/hackrx/run",
                json=test_request,
                headers=headers
            )
            duration = time.time() - start_time
            
            print(f"\n   Status: {response.status_code}")
            print(f"   Duration: {duration:.2f} seconds")
            
            if response.status_code == 200:
                result = response.json()
                print("   Response:")
                print(f"   {json.dumps(result, indent=2)}")
                
                print(f"\n   ✅ Successfully processed {len(result['answers'])} questions")
                for i, answer in enumerate(result['answers'], 1):
                    print(f"   {i}. {answer}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Test failed: {e}")


def test_local_api():
    """Test local API before deployment"""
    print("Testing local API...")
    return asyncio.run(test_vercel_deployment("http://localhost:8000"))


def test_vercel_api(url: str):
    """Test deployed Vercel API"""
    print("Testing Vercel deployment...")
    return asyncio.run(test_vercel_deployment(url))


if __name__ == "__main__":
    print("Vercel Deployment Test")
    print("=" * 30)
    
    # Test options
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"Testing deployment at: {url}")
        asyncio.run(test_vercel_deployment(url))
    else:
        print("Usage:")
        print("  python test_vercel.py <vercel-url>")
        print("  python test_vercel.py https://your-app.vercel.app")
        print("\nOr test local API:")
        print("  python test_vercel.py http://localhost:8000")
