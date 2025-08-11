#!/usr/bin/env python3
"""
AI Answer Generator - A4F API Integration Module

This module provides AI-powered answer generation using the A4F API service.
It implements intelligent load balancing across multiple API keys and robust
error handling with exponential backoff retry logic.

Features:
- Multiple API key support for high availability
- Round-robin load balancing for optimal performance  
- Automatic retry with exponential backoff
- Configurable timeout and retry limits
- Support for various A4F model providers

The generator is specifically tuned for generating concise, accurate answers
from document context, making it ideal for question-answering applications.

Author: AI Assistant
Date: August 11, 2025
Version: 1.0.0
"""

import time
import requests
from typing import List, Optional


class AIAnswerGenerator:
    """
    AI Answer Generator using A4F API with intelligent key rotation
    
    This class manages multiple A4F API keys to ensure high availability and
    distributes load across keys using round-robin scheduling. It provides
    robust error handling and retry logic for production use.
    
    Attributes:
        api_keys: List of A4F API keys for load balancing
        model: A4F model identifier (must include provider prefix)
        current_key_index: Current position in key rotation
        base_url: A4F API base URL
        max_retries: Maximum retry attempts per request
        timeout: Request timeout in seconds
    """
    
    def __init__(self, api_keys: List[str], model: str = "provider-2/gpt-4o-mini"):
        """
        Initialize the AI Answer Generator
        
        Args:
            api_keys: List of A4F API keys for load balancing
            model: A4F model name with provider prefix (e.g., "provider-2/gpt-4o-mini")
            
        Raises:
            ValueError: If no API keys are provided
        """
        self.api_keys = api_keys
        self.model = model
        self.current_key_index = 0
        self.base_url = "https://api.a4f.co/v1"
        self.max_retries = 3
        self.timeout = 30
        
        if not self.api_keys:
            raise ValueError("At least one API key must be provided")
            
        print(f"🤖 AI Generator initialized with {len(self.api_keys)} keys, model: {self.model}")
    
    def get_next_api_key(self) -> str:
        """
        Get the next API key using round-robin load balancing
        
        Returns:
            str: Next API key in rotation
        """
        key = self.api_keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return key
    
    def generate_answer(self, question: str, context: str, max_tokens: int = 150) -> Optional[str]:
        """Generate a concise answer using A4F API"""
        
        prompt = f"""Based on the following context from a policy document, provide a clear and concise answer to the question in exactly ONE sentence.

Context: {context}

Question: {question}

Answer (one sentence only):"""

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides clear, concise answers based on policy documents. Always respond in exactly one sentence."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
            "top_p": 0.9
        }
        
        for attempt in range(self.max_retries):
            try:
                api_key = self.get_next_api_key()
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"].strip()
                    return answer
                else:
                    print(f"API request failed (attempt {attempt + 1}): {response.status_code}")
                    if response.status_code in [429, 500, 502, 503]:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        continue
                        
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt + 1}): {e}")
                time.sleep(1)
            except Exception as e:
                print(f"Unexpected error (attempt {attempt + 1}): {e}")
                time.sleep(1)
        
        print("Failed to generate answer after all retry attempts")
        return None


# Test function
if __name__ == "__main__":
    api_keys = [
        "ddc-a4f-b09618069a99435482ddb643588c748a",
        "ddc-a4f-b3c73ba57e1e454982d716b2d1eab0e0"
    ]
    
    generator = AIAnswerGenerator(api_keys)
    
    test_context = "This health insurance policy covers medical expenses, hospitalization costs, and emergency treatments. The waiting period is 30 days for most conditions."
    test_question = "What is the waiting period?"
    
    answer = generator.generate_answer(test_question, test_context)
    print(f"Question: {test_question}")
    print(f"Answer: {answer}")
