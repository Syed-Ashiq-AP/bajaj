# Deployment Guide - Document Q&A API

This guide provides step-by-step instructions for deploying the Document Q&A API in various environments.

## 🚀 Quick Start

### Prerequisites

-   Python 3.11+
-   pip package manager
-   4GB+ RAM recommended
-   Internet access for AI API calls

### 1. Local Development Setup

```bash
# Clone or navigate to project directory
cd /home/syedtl/Project/bajaj/self

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the API server
python start_api.py
```

The API will be available at:

-   **Main API**: http://localhost:8000
-   **Interactive Docs**: http://localhost:8000/docs
-   **Health Check**: http://localhost:8000/health

### 2. Test the API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test document processing
curl -X POST "http://localhost:8000/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5" \
  -d '{
    "documents": "https://example.com/document.pdf",
    "questions": ["What is this document about?"]
  }'
```

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run Docker Container

```bash
# Build the image
docker build -t document-qa-api .

# Run the container
docker run -d \
  --name document-qa \
  -p 8000:8000 \
  -e A4F_API_KEYS="key1,key2,key3,key4" \
  document-qa-api

# Check logs
docker logs document-qa

# Test the containerized API
curl http://localhost:8000/health
```

## ☁️ Cloud Deployment

### AWS Lambda + API Gateway

#### 1. Install Lambda Dependencies

```bash
# Install additional dependencies for Lambda
pip install mangum

# Create lambda_function.py
cat > lambda_function.py << EOF
from mangum import Mangum
from api import app

handler = Mangum(app)
EOF
```

#### 2. Package for Lambda

```bash
# Create deployment package
mkdir lambda-package
pip install -r requirements.txt -t lambda-package/
cp *.py lambda-package/
cd lambda-package && zip -r ../deployment-package.zip .
```

#### 3. Deploy to AWS Lambda

```bash
# Create Lambda function
aws lambda create-function \
  --function-name document-qa-api \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.handler \
  --zip-file fileb://deployment-package.zip \
  --timeout 300 \
  --memory-size 1024

# Update environment variables
aws lambda update-function-configuration \
  --function-name document-qa-api \
  --environment Variables='{
    "A4F_API_KEY_1":"ddc-a4f-b09618069a99435482ddb643588c748a",
    "A4F_API_KEY_2":"ddc-a4f-b3c73ba57e1e454982d716b2d1eab0e0",
    "A4F_API_KEY_3":"ddc-a4f-832b8dc986bf41bd889f6b75930be6f3",
    "A4F_API_KEY_4":"ddc-a4f-2fcfcb59d9114c8dab949a50436434b6"
  }'
```

### Google Cloud Run

#### 1. Create cloudbuild.yaml

```yaml
steps:
    - name: "gcr.io/cloud-builders/docker"
      args: ["build", "-t", "gcr.io/$PROJECT_ID/document-qa-api", "."]
    - name: "gcr.io/cloud-builders/docker"
      args: ["push", "gcr.io/$PROJECT_ID/document-qa-api"]
    - name: "gcr.io/cloud-builders/gcloud"
      args:
          - "run"
          - "deploy"
          - "document-qa-api"
          - "--image=gcr.io/$PROJECT_ID/document-qa-api"
          - "--region=us-central1"
          - "--platform=managed"
          - "--allow-unauthenticated"
          - "--memory=2Gi"
          - "--cpu=2"
          - "--timeout=300"
```

#### 2. Deploy to Cloud Run

```bash
# Build and deploy
gcloud builds submit --config cloudbuild.yaml

# Set environment variables
gcloud run services update document-qa-api \
  --region=us-central1 \
  --set-env-vars="A4F_API_KEY_1=ddc-a4f-b09618069a99435482ddb643588c748a"
```

### Azure Container Instances

```bash
# Create resource group
az group create --name document-qa-rg --location eastus

# Deploy container
az container create \
  --resource-group document-qa-rg \
  --name document-qa-api \
  --image your-registry/document-qa-api:latest \
  --cpu 2 \
  --memory 4 \
  --ports 8000 \
  --dns-name-label document-qa-api \
  --environment-variables \
    A4F_API_KEY_1="ddc-a4f-b09618069a99435482ddb643588c748a" \
    A4F_API_KEY_2="ddc-a4f-b3c73ba57e1e454982d716b2d1eab0e0"
```

## 🔧 Production Configuration

### Environment Variables

```bash
# Required API Keys
export A4F_API_KEY_1="ddc-a4f-b09618069a99435482ddb643588c748a"
export A4F_API_KEY_2="ddc-a4f-b3c73ba57e1e454982d716b2d1eab0e0"
export A4F_API_KEY_3="ddc-a4f-832b8dc986bf41bd889f6b75930be6f3"
export A4F_API_KEY_4="ddc-a4f-2fcfcb59d9114c8dab949a50436434b6"

# Optional Configuration
export API_HOST="0.0.0.0"
export API_PORT="8000"
export LOG_LEVEL="info"
export MAX_RETRIES="3"
export REQUEST_TIMEOUT="30"
```

### Production Settings

```python
# production_config.py
import os

class Settings:
    # Server Configuration
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", 8000))

    # AI Configuration
    A4F_API_KEYS = [
        os.getenv("A4F_API_KEY_1"),
        os.getenv("A4F_API_KEY_2"),
        os.getenv("A4F_API_KEY_3"),
        os.getenv("A4F_API_KEY_4")
    ]

    # Performance Settings
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))

    # Security
    AUTH_TOKEN = os.getenv("AUTH_TOKEN", "e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5")
```

## 📊 Monitoring and Logging

### Health Checks

```bash
# Simple health check
curl -f http://your-api-url/health || exit 1

# Detailed health check
curl -s http://your-api-url/health | jq '.ai_enabled'
```

### Logging Configuration

```python
# Add to api.py for production logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api.log')
    ]
)
```

### Performance Monitoring

```python
# Add performance metrics
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        logging.info(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper
```

## 🔒 Security Considerations

### API Security

-   Use HTTPS in production
-   Rotate API keys regularly
-   Implement rate limiting
-   Add request validation
-   Log security events

### Data Security

-   Temporary file cleanup
-   No persistent data storage
-   Secure API key management
-   Input sanitization

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**

    ```bash
    # Reinstall dependencies
    pip install -r requirements.txt --force-reinstall
    ```

2. **API Key Issues**

    ```bash
    # Test API keys
    python -c "from ai_generator import AIAnswerGenerator; AIAnswerGenerator(['your-key']).test_connection()"
    ```

3. **Memory Issues**

    ```bash
    # Increase container memory
    docker run -m 4g document-qa-api
    ```

4. **Timeout Issues**
    ```python
    # Increase timeout in ai_generator.py
    self.timeout = 60  # seconds
    ```

### Debug Mode

```bash
# Start with debug logging
uvicorn api:app --host 0.0.0.0 --port 8000 --log-level debug
```

## 📈 Scaling

### Horizontal Scaling

-   Deploy multiple instances behind load balancer
-   Use container orchestration (Kubernetes)
-   Implement session-less design

### Performance Optimization

-   Cache embeddings for repeated documents
-   Use faster embedding models
-   Implement request queuing
-   Add CDN for static assets

This deployment guide should cover most common scenarios. Choose the deployment method that best fits your infrastructure and requirements.
