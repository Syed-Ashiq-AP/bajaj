#!/usr/bin/env python3
"""
API Client Test Script
"""

import httpx
import json
import asyncio


async def test_api_client():
    """Test the API with a real request"""
    
    # API endpoint
    base_url = "http://localhost:8000"
    
    # Test request
    request_data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment?",
            "What is the waiting period for pre-existing diseases?",
            "Does this policy cover maternity expenses?"
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5"
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            # Test health check first
            print("Testing health check...")
            health_response = await client.get(f"{base_url}/health")
            print(f"Health check: {health_response.status_code} - {health_response.json()}")
            
            # Test main endpoint
            print("\nTesting main endpoint...")
            print("Request:")
            print(json.dumps(request_data, indent=2))
            
            response = await client.post(
                f"{base_url}/hackrx/run",
                json=request_data,
                headers=headers
            )
            
            print(f"\nResponse Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("\nResponse:")
                print(json.dumps(result, indent=2))
                
                print("\nFormatted Answers:")
                for i, answer in enumerate(result["answers"], 1):
                    print(f"{i}. {answer}")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Error testing API: {e}")


if __name__ == "__main__":
    print("Testing Document Q&A API Client")
    print("=" * 40)
    print("Make sure the API is running on localhost:8000")
    print("Start it with: python start_api.py")
    print("=" * 40)
    
    asyncio.run(test_api_client())
