#!/usr/bin/env python3
"""
Simplified Document Q&A Processor - Vercel Compatible Version

This is a lightweight version of the document processor optimized for 
Vercel serverless deployment. It uses simple text search instead of 
vector embeddings to reduce dependencies and cold start time.

Classes:
    SimpleDocumentProcessor: Handles PDF processing and text chunking
    SimpleDocumentQAProcessor: Main orchestrator for the Q&A pipeline

Author: AI Assistant  
Date: August 11, 2025
Version: 1.0.0 (Vercel Optimized)
"""

import os
import re
import tempfile
from typing import List, Dict, Optional, Tuple
import PyPDF2
from dotenv import load_dotenv

from .ai_generator import AIAnswerGenerator

# Load environment variables
load_dotenv()


class SimpleDocumentProcessor:
    """
    Simplified document processor that handles PDF text extraction and chunking
    without heavy ML dependencies.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        """
        Initialize the simple document processor.
        
        Args:
            chunk_size: Maximum size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF content.
        
        Args:
            pdf_content: Raw PDF file content as bytes
            
        Returns:
            Extracted text from all pages
        """
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(pdf_content)
                temp_file.flush()
                
                with open(temp_file.name, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        text += page_text + "\n"
                
                os.unlink(temp_file.name)
                return text
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        
        return text.strip()
    
    def create_chunks(self, text: str) -> List[Dict[str, any]]:
        """
        Split text into overlapping chunks for processing.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of chunk dictionaries with metadata
        """
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at word boundaries
            if end < len(text):
                # Find the last space within the chunk
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'start_pos': start,
                    'end_pos': end,
                    'length': len(chunk_text)
                })
                chunk_id += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        return chunks


class SimpleDocumentQAProcessor:
    """
    Simplified document Q&A processor using basic text search.
    """
    
    def __init__(self):
        """Initialize the simple Q&A processor."""
        self.document_processor = SimpleDocumentProcessor()
        
        print("🔍 Loading A4F API keys from environment...")
        
        # Load A4F API keys from environment variables
        api_keys = []
        for i in range(1, 5):  # A4F_API_KEY_1 through A4F_API_KEY_4
            key = os.getenv(f'A4F_API_KEY_{i}')
            if key:
                stripped_key = key.strip()
                api_keys.append(stripped_key)
                print(f"✅ Found A4F_API_KEY_{i} (ending in ...{stripped_key[-8:]})")
            else:
                print(f"❌ A4F_API_KEY_{i} not found in environment")
        
        if not api_keys:
            print("🔄 No individual keys found, checking old format...")
            # Fallback to the old format if available
            old_format = os.getenv('A4F_API_KEYS', '')
            if old_format:
                api_keys = [key.strip() for key in old_format.split(',') if key.strip()]
                print(f"✅ Found {len(api_keys)} keys in old format")
            else:
                print("❌ No A4F_API_KEYS found in old format either")
        
        print(f"🔑 Total API keys loaded: {len(api_keys)}")
        
        try:
            if api_keys:
                self.ai_generator = AIAnswerGenerator(api_keys)
                self.ai_enabled = True
                print("✅ AI Generator initialized successfully")
            else:
                self.ai_generator = None
                self.ai_enabled = False
                print("❌ No API keys available - AI generation disabled")
        except Exception as e:
            print(f"💥 Failed to initialize AI generator: {e}")
            print(f"💥 Error type: {type(e).__name__}")
            self.ai_generator = None
            self.ai_enabled = False
            
        self.document_chunks = []
        self.document_text = ""
    
    async def process_document(self, pdf_content: bytes) -> Dict[str, any]:
        """
        Process a PDF document for Q&A.
        
        Args:
            pdf_content: Raw PDF file content
            
        Returns:
            Processing result with metadata
        """
        try:
            # Extract and clean text
            raw_text = self.document_processor.extract_text_from_pdf(pdf_content)
            self.document_text = self.document_processor.clean_text(raw_text)
            
            # Create chunks
            self.document_chunks = self.document_processor.create_chunks(self.document_text)
            
            return {
                'success': True,
                'message': 'Document processed successfully',
                'chunks_count': len(self.document_chunks),
                'total_characters': len(self.document_text),
                'processing_time': 'N/A (simple processing)'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error processing document: {str(e)}',
                'chunks_count': 0,
                'total_characters': 0
            }
    
    def simple_text_search(self, query: str, top_k: int = 3) -> List[Dict[str, any]]:
        """
        Perform simple text-based search through document chunks.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant chunks with scores
        """
        if not self.document_chunks:
            return []
        
        query_words = set(query.lower().split())
        scored_chunks = []
        
        for chunk in self.document_chunks:
            chunk_text = chunk['text'].lower()
            chunk_words = set(chunk_text.split())
            
            # Simple scoring based on word matches
            common_words = query_words.intersection(chunk_words)
            score = len(common_words) / len(query_words) if query_words else 0
            
            # Boost score for exact phrase matches
            if query.lower() in chunk_text:
                score += 0.5
            
            if score > 0:
                scored_chunks.append({
                    'chunk': chunk,
                    'score': score,
                    'text': chunk['text']
                })
        
        # Sort by score and return top_k
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        return scored_chunks[:top_k]
    
    async def answer_question(self, question: str) -> Dict[str, any]:
        """
        Answer a question about the processed document.
        
        Args:
            question: User's question
            
        Returns:
            Answer with metadata and context
        """
        try:
            if not self.document_chunks:
                return {
                    'success': False,
                    'answer': 'No document has been processed yet. Please upload a document first.',
                    'context_used': [],
                    'confidence': 0.0
                }
            
            # Find relevant chunks
            relevant_chunks = self.simple_text_search(question, top_k=3)
            
            if not relevant_chunks:
                return {
                    'success': False,
                    'answer': 'I could not find relevant information in the document to answer your question.',
                    'context_used': [],
                    'confidence': 0.0
                }
            
            # Prepare context for AI
            context_text = "\n\n".join([chunk['text'] for chunk in relevant_chunks])
            
            # Generate answer using AI
            ai_answer = self.ai_generator.generate_answer(question, context_text)
            
            if ai_answer:
                return {
                    'success': True,
                    'answer': ai_answer,
                    'context_used': [chunk['chunk'] for chunk in relevant_chunks],
                    'confidence': 0.8,
                    'model_used': 'A4F API',
                    'search_method': 'simple_text_search'
                }
            else:
                return {
                    'success': False,
                    'answer': 'Failed to generate answer using AI.',
                    'context_used': [chunk['chunk'] for chunk in relevant_chunks],
                    'confidence': 0.0,
                    'error': 'AI generator returned None'
                }
        
        except Exception as e:
            return {
                'success': False,
                'answer': f'Error processing question: {str(e)}',
                'context_used': [],
                'confidence': 0.0
            }
    
    async def process_document_and_answer(self, pdf_path: str = None, pdf_content: bytes = None, questions: List[str] = None) -> List[str]:
        """
        Complete pipeline: process PDF document and answer multiple questions.
        
        Args:
            pdf_path: Path to PDF file (optional)
            pdf_content: PDF file content as bytes (optional)
            questions: List of questions to answer
            
        Returns:
            List of answers corresponding to the questions
        """
        try:
            # Handle both pdf_path and pdf_content inputs
            if pdf_path and not pdf_content:
                # Read the file to get pdf_content
                with open(pdf_path, 'rb') as file:
                    pdf_content = file.read()
            elif not pdf_content:
                raise ValueError("Either pdf_path or pdf_content must be provided")
            
            if not questions:
                questions = []
            
            # Step 1: Process the document
            doc_result = await self.process_document(pdf_content)
            if not doc_result['success']:
                return [f"Error processing document: {doc_result.get('message', 'Unknown error')}" for _ in questions]
            
            # Step 2: Answer all questions
            answers = []
            for question in questions:
                answer_result = await self.answer_question(question)
                if answer_result['success']:
                    answers.append(answer_result['answer'])
                else:
                    answers.append(f"Error: {answer_result.get('error', 'Failed to generate answer')}")
            
            return answers
            
        except Exception as e:
            error_msg = f"Processing failed: {str(e)}"
            return [error_msg for _ in questions] if questions else [error_msg]

    def get_document_summary(self) -> Dict[str, any]:
        """
        Get summary information about the processed document.
        
        Returns:
            Document summary with statistics
        """
        if not self.document_text:
            return {
                'processed': False,
                'message': 'No document processed'
            }
        
        return {
            'processed': True,
            'total_characters': len(self.document_text),
            'total_chunks': len(self.document_chunks),
            'avg_chunk_size': sum(chunk['length'] for chunk in self.document_chunks) / len(self.document_chunks) if self.document_chunks else 0,
            'search_method': 'simple_text_search',
            'preview': self.document_text[:500] + '...' if len(self.document_text) > 500 else self.document_text
        }
