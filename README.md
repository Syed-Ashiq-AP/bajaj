# Document Q&A API

A FastAPI-based service that processes PDF documents and answers questions using semantic search combined with AI-powered answer generation.

## Features

-   **PDF Processing**: Extracts and processes text from PDF documents
-   **Semantic Search**: Uses FAISS vector similarity search with sentence transformers
-   **AI Answer Generation**: Generates concise answers using A4F API with multiple key load balancing
-   **RESTful API**: Clean FastAPI interface with authentication
-   **Scalable**: Processes multiple questions efficiently

## API Endpoints

### POST `/hackrx/run`

Process a PDF document and answer questions.

**Headers:**

-   `Content-Type: application/json`
-   `Authorization: Bearer e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5`

**Request Body:**

```json
{
    "documents": "https://example.com/document.pdf",
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?"
    ]
}
```

**Response:**

```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment after the due date.",
        "The waiting period for pre-existing diseases is thirty-six (36) months of continuous coverage."
    ]
}
```

### GET `/health`

Check API health and AI status.

**Response:**

```json
{
    "status": "healthy",
    "ai_enabled": true
}
```

## Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**

```bash
# Create .env file with API keys (already configured)
```

## Running the API

### Development

```bash
python start_api.py
```

### Production

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

The API will be available at:

-   **Main API**: http://localhost:8000
-   **Interactive Docs**: http://localhost:8000/docs
-   **Health Check**: http://localhost:8000/health

## Testing

### Test the document processor locally:

```bash
python test_api.py
```

### Test the API client:

```bash
# Make sure API is running first
python test_client.py
```

## Architecture

```
├── api.py                    # FastAPI application
├── document_processor.py     # Main document processing logic
├── ai_generator.py          # AI answer generation
├── start_api.py            # API startup script
├── test_api.py             # Local testing
├── test_client.py          # API client testing
└── requirements.txt        # Dependencies
```

### Core Components

1. **DocumentProcessor**: Handles PDF text extraction and chunking
2. **DocumentQAProcessor**: Main processor combining search + AI
3. **AIAnswerGenerator**: A4F API integration with load balancing
4. **FastAPI App**: RESTful API interface with authentication

## Performance

-   **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
-   **Search Engine**: FAISS IndexFlatIP for cosine similarity
-   **Chunk Size**: 400 tokens with 2-sentence overlap
-   **AI Model**: provider-2/gpt-4o-mini via A4F API
-   **Load Balancing**: Round-robin across 4 API keys

## Error Handling

-   PDF download failures return 400 status
-   Processing errors return 500 status
-   AI generation failures provide fallback responses
-   Authentication errors return 401 status

## Example Usage

```python
import httpx
import asyncio

async def query_document():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/hackrx/run",
            json={
                "documents": "https://example.com/policy.pdf",
                "questions": ["What is covered?", "How to claim?"]
            },
            headers={
                "Authorization": "Bearer e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5"
            }
        )
        return response.json()

result = asyncio.run(query_document())
```

## Dependencies

-   **faiss-cpu**: Vector similarity search
-   **sentence-transformers**: Text embeddings
-   **PyPDF2**: PDF text extraction
-   **fastapi**: Web framework
-   **httpx**: HTTP client for PDF downloads
-   **tiktoken**: Token counting
-   **requests**: AI API calls

## License

MIT License
