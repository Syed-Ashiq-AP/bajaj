#!/usr/bin/env python3
"""
Vercel Serverless API Entry Point
FastAPI application adapted for Vercel's serverless architecture
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path to import our modules
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, HttpUrl
from typing import List
import httpx
import tempfile
import asyncio
from contextlib import asynccontextmanager

from .document_processor_simple import SimpleDocumentQAProcessor

# API Models
class QuestionRequest(BaseModel):
    documents: HttpUrl
    questions: List[str]

class QuestionResponse(BaseModel):
    answers: List[str]

# Security
security = HTTPBearer()
VALID_TOKEN = "e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5"

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials.credentials

# Global processor instance (will be initialized per request in serverless)
processor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Initialize processor
    global processor
    try:
        processor = SimpleDocumentQAProcessor()
        print("SimpleDocumentQAProcessor initialized successfully")
    except Exception as e:
        print(f"Failed to initialize processor: {e}")
        processor = None
    yield
    # Shutdown
    processor = None

# FastAPI app
app = FastAPI(
    title="Document Q&A API",
    description="AI-powered document question answering using semantic search (Vercel Deployment)",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "message": "Document Q&A API is running on Vercel",
        "status": "healthy",
        "platform": "vercel-serverless"
    }

@app.get("/health")
async def health_check():
    global processor
    if processor is None:
        # Initialize processor if not already done (cold start)
        try:
            processor = SimpleDocumentQAProcessor()
        except Exception as e:
            return {
                "status": "unhealthy", 
                "error": str(e),
                "ai_enabled": False
            }
    
    return {
        "status": "healthy", 
        "ai_enabled": processor.ai_enabled if processor else False,
        "platform": "vercel-serverless"
    }

@app.post("/hackrx/run", response_model=QuestionResponse)
async def process_questions(
    request: QuestionRequest,
    token: str = Depends(verify_token)
):
    """
    Process PDF document and answer questions using AI-powered semantic search
    Optimized for Vercel serverless deployment
    """
    global processor
    
    # Initialize processor if not already done (cold start handling)
    if processor is None:
        try:
            processor = SimpleDocumentQAProcessor()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize processor: {str(e)}")
    
    try:
        # Download PDF from URL with timeout
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.get(str(request.documents))
            response.raise_for_status()
            
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Process document and answer questions
            answers = await processor.process_document_and_answer(
                pdf_path=temp_path,
                questions=request.questions
            )
            
            return QuestionResponse(answers=answers)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Failed to download PDF: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

# Vercel requires the app to be available as 'app'
# This is the entry point for Vercel - no custom handler needed
# app = app  # FastAPI app is already exported

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
