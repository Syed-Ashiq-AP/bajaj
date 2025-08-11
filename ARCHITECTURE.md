"""
Project Structure Documentation
=====================================

This document outlines the structure and components of the Document Q&A API project.

## 📁 Project Structure

```
/home/syedtl/Project/bajaj/self/
├── 📄 api.py                    # FastAPI application and endpoints
├── 📄 document_processor.py     # PDF processing and FAISS search
├── 📄 ai_generator.py          # A4F API integration for AI answers
├── 📄 start_api.py             # API server startup script
├── 📄 test_api.py              # Local testing and validation
├── 📄 test_client.py           # API client testing
├── 📄 requirements.txt         # Python dependencies
├── 📄 README.md                # Project documentation
├── 📄 .env                     # Environment variables (API keys)
├── 📄 policy.pdf               # Sample document for testing
└── 📁 .venv/                   # Python virtual environment
```

## 🔧 Core Components

### 1. api.py - FastAPI Application

-   **Purpose**: Main web application providing RESTful API endpoints
-   **Key Features**:
    -   Authentication with Bearer tokens
    -   PDF document processing endpoint
    -   Health check endpoint
    -   Comprehensive API documentation
    -   Error handling and validation

### 2. document_processor.py - Document Processing Engine

-   **Purpose**: Handles PDF processing and semantic search
-   **Key Features**:
    -   PDF text extraction using PyPDF2
    -   Intelligent text chunking with overlap
    -   FAISS vector index creation
    -   Semantic search using sentence transformers
    -   Integration with AI answer generation

### 3. ai_generator.py - AI Answer Generation

-   **Purpose**: Generates AI-powered answers using A4F API
-   **Key Features**:
    -   Multiple API key load balancing
    -   Round-robin key rotation
    -   Retry logic with exponential backoff
    -   Provider prefix model support
    -   Error handling and fallbacks

## 🚀 API Endpoints

### POST /hackrx/run

-   **Function**: Process PDF documents and answer questions
-   **Authentication**: Bearer token required
-   **Input**: PDF URL + list of questions
-   **Output**: List of AI-generated answers
-   **Processing Flow**:
    1. Download PDF from URL
    2. Extract and clean text
    3. Create vector embeddings
    4. Build FAISS search index
    5. Search for relevant content per question
    6. Generate AI answers using A4F API

### GET /health

-   **Function**: API health check
-   **Authentication**: None required
-   **Output**: Health status and AI availability

### GET /

-   **Function**: Root endpoint with API information
-   **Authentication**: None required
-   **Output**: API metadata and navigation links

## 📦 Dependencies

### Core Processing

-   **faiss-cpu**: Fast similarity search and clustering
-   **sentence-transformers**: Pre-trained embedding models
-   **PyPDF2**: PDF text extraction
-   **tiktoken**: Token counting for language models
-   **numpy**: Numerical computations

### Web Framework

-   **fastapi**: Modern web framework for APIs
-   **uvicorn**: ASGI server implementation
-   **pydantic**: Data validation and parsing
-   **httpx**: Async HTTP client for PDF downloads

### Utilities

-   **python-dotenv**: Environment variable management
-   **requests**: HTTP library for AI API calls

## 🔐 Security

### Authentication

-   Bearer token authentication for main endpoint
-   Token validation on each request
-   Configurable token in environment variables

### Data Handling

-   Temporary file management for PDF processing
-   Automatic cleanup of downloaded files
-   No persistent storage of user documents

## 🎯 Performance Characteristics

### Semantic Search

-   **Model**: all-MiniLM-L6-v2 (384 dimensions)
-   **Index Type**: FAISS IndexFlatIP (cosine similarity)
-   **Chunk Size**: 400 tokens with 2-sentence overlap
-   **Search Results**: Top 3 most relevant chunks per question

### AI Generation

-   **Model**: provider-2/gpt-4o-mini via A4F API
-   **Load Balancing**: 4 API keys in round-robin
-   **Timeout**: 30 seconds per request
-   **Retry Logic**: 3 attempts with exponential backoff
-   **Response Length**: ~150 tokens (1-2 sentences)

## 🧪 Testing

### Local Testing

-   `test_api.py`: Tests document processor directly
-   `test_client.py`: Tests API endpoints via HTTP
-   Sample questions and expected response format
-   Performance benchmarking capabilities

### Development Server

-   `start_api.py`: Starts development server
-   Interactive documentation at `/docs`
-   Health monitoring at `/health`
-   Configurable host and port settings

## 🔄 Processing Pipeline

```
📥 PDF URL Input
    ↓
🌐 Download PDF
    ↓
📄 Extract Text (PyPDF2)
    ↓
🧹 Clean & Normalize Text
    ↓
✂️ Chunk into Segments (400 tokens)
    ↓
🧠 Generate Embeddings (sentence-transformers)
    ↓
🔍 Build FAISS Index
    ↓
❓ Process Questions
    ↓
🎯 Semantic Search (top 3 chunks)
    ↓
🤖 AI Answer Generation (A4F API)
    ↓
📤 Return Structured Response
```

## 📈 Scalability Considerations

### Horizontal Scaling

-   Stateless design allows multiple instances
-   Load balancing across API keys
-   Independent processing per request

### Performance Optimization

-   FAISS for fast similarity search
-   Efficient text chunking strategy
-   Concurrent question processing capability
-   Optimized embedding model selection

### Resource Management

-   Temporary file cleanup
-   Memory-efficient document processing
-   Configurable timeout and retry limits
-   Graceful error handling and recovery

## 🚀 Deployment Options

### Local Development

```bash
python start_api.py
```

### Production (Docker)

```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment

-   Compatible with AWS Lambda, Google Cloud Run, Azure Functions
-   Requires environment variable configuration for API keys
-   Scalable based on request volume

This architecture provides a robust, scalable solution for document Q&A
with high accuracy and performance characteristics suitable for production use.
"""
