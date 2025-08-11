#!/usr/bin/env python3
"""
Test script for the Document Q&A API
"""

import asyncio
import json
from document_processor import DocumentQAProcessor


async def test_local_processing():
    """Test the document processor locally"""
    
    print("Testing DocumentQAProcessor...")
    processor = DocumentQAProcessor()
    
    # Test questions similar to the API example
    questions = [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?",
        "Does this policy cover maternity expenses?",
        "What is the waiting period for cataract surgery?",
        "Are medical expenses for organ donors covered?",
        "What is the No Claim Discount offered?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a Hospital?",
        "What is the coverage for AYUSH treatments?",
        "Are there sub-limits on room rent and ICU charges?"
    ]
    
    try:
        answers = await processor.process_document_and_answer("policy.pdf", questions)
        
        print("\n" + "="*80)
        print("DOCUMENT Q&A RESULTS")
        print("="*80)
        
        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            print(f"\n{i}. Q: {question}")
            print(f"   A: {answer}")
        
        print("\n" + "="*80)
        print(f"Successfully processed {len(questions)} questions")
        
        # Format as API response
        api_response = {
            "answers": answers
        }
        
        print("\nAPI Response format:")
        print(json.dumps(api_response, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")


def test_api_format():
    """Test API request/response format"""
    
    sample_request = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?"
        ]
    }
    
    print("Sample API Request:")
    print(json.dumps(sample_request, indent=2))
    
    sample_response = {
        "answers": [
            "A grace period of thirty days is provided for premium payment after the due date.",
            "There is a waiting period of thirty-six (36) months for pre-existing diseases.",
            "Yes, the policy covers maternity expenses with a 24-month waiting period."
        ]
    }
    
    print("\nSample API Response:")
    print(json.dumps(sample_response, indent=2))


if __name__ == "__main__":
    print("Document Q&A API Testing")
    print("=" * 40)
    
    # Test API format
    test_api_format()
    
    print("\n" + "=" * 40)
    print("Testing local processing...")
    
    # Test local processing
    asyncio.run(test_local_processing())
