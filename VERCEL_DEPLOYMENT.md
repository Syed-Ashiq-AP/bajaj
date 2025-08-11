# Vercel Deployment Guide

This guide explains how to deploy the Document Q&A API to Vercel's serverless platform.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **Git Repository**: Push your code to GitHub/GitLab/Bitbucket

## Project Structure for Vercel

```
├── api/
│   ├── index.py              # Vercel serverless entry point
│   ├── requirements.txt      # Python dependencies
│   ├── document_processor.py # Core processing logic
│   └── ai_generator.py       # AI answer generation
├── vercel.json              # Vercel configuration
├── .env.vercel              # Environment variables template
└── README.md                # Documentation
```

## Step 1: Environment Variables Setup

In your Vercel dashboard, go to **Settings → Environment Variables** and add:

```
A4F_API_KEY_1 = ddc-a4f-b09618069a99435482ddb643588c748a
A4F_API_KEY_2 = ddc-a4f-b3c73ba57e1e454982d716b2d1eab0e0
A4F_API_KEY_3 = ddc-a4f-832b8dc986bf41bd889f6b75930be6f3
A4F_API_KEY_4 = ddc-a4f-2fcfcb59d9114c8dab949a50436434b6
ENVIRONMENT = production
```

**Note**: These should be added as **Secrets** in Vercel for security.

## Step 2: Deploy via CLI

```bash
# Login to Vercel
vercel login

# Deploy from project directory
cd /path/to/your/project
vercel

# Follow the prompts:
# ? Set up and deploy "~/Project/bajaj/self"? [Y/n] y
# ? Which scope do you want to deploy to? [Your Team]
# ? Link to existing project? [y/N] n
# ? What's your project's name? document-qa-api
# ? In which directory is your code located? ./
```

## Step 3: Deploy via GitHub Integration

1. **Push to GitHub**:

    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git remote add origin https://github.com/username/document-qa-api.git
    git push -u origin main
    ```

2. **Connect to Vercel**:
    - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
    - Click "New Project"
    - Import your GitHub repository
    - Configure environment variables
    - Deploy

## Step 4: Verify Deployment

After deployment, you'll get a URL like: `https://document-qa-api.vercel.app`

Test the endpoints:

```bash
# Health check
curl https://your-app.vercel.app/health

# API test
curl -X POST "https://your-app.vercel.app/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5" \
  -d '{
    "documents": "https://example.com/document.pdf",
    "questions": ["What is covered?"]
  }'
```

## Vercel Configuration Details

### vercel.json

```json
{
    "version": 2,
    "builds": [
        {
            "src": "api/index.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "api/index.py"
        }
    ],
    "functions": {
        "api/index.py": {
            "maxDuration": 300
        }
    }
}
```

### Key Features:

-   **Cold Start Handling**: Optimized initialization
-   **Timeout Configuration**: 300 seconds for large documents
-   **Memory Optimization**: Efficient resource usage
-   **Error Handling**: Robust serverless error management

## Performance Considerations

### Vercel Limits:

-   **Function Duration**: 300 seconds (5 minutes) max
-   **Memory**: 1008 MB max
-   **Request Size**: 4.5 MB max
-   **Response Size**: 4.5 MB max

### Optimizations Applied:

-   Lazy loading of ML models
-   Efficient memory management
-   Streaming for large documents
-   Connection pooling for API calls

## Monitoring & Debugging

### Vercel Analytics:

-   Function invocations
-   Duration metrics
-   Error rates
-   Memory usage

### Logs Access:

```bash
# View deployment logs
vercel logs https://your-app.vercel.app

# Real-time logs
vercel logs --follow
```

## Troubleshooting

### Common Issues:

1. **Cold Start Timeouts**:

    - Solution: Implemented lazy initialization
    - Models load on first request

2. **Memory Limits**:

    - Solution: Optimized dependencies
    - Using CPU-only versions

3. **Environment Variables**:

    - Ensure all A4F keys are set
    - Check variable names match exactly

4. **Import Errors**:
    - All dependencies in `api/requirements.txt`
    - Modules copied to `api/` directory

## Custom Domain Setup

1. **Add Domain** in Vercel dashboard
2. **Configure DNS** with your provider
3. **SSL Certificate** (automatic)

## Scaling Considerations

-   **Concurrent Requests**: Vercel handles automatically
-   **Rate Limiting**: Implement if needed
-   **Caching**: Consider Redis for frequent queries
-   **Load Balancing**: Built into Vercel platform

## Security Best Practices

1. **API Keys**: Store as Vercel secrets
2. **Authentication**: Bearer token validation
3. **CORS**: Configure if needed for web clients
4. **Input Validation**: Implemented in API models

## Cost Optimization

-   **Function Duration**: Optimized processing time
-   **Memory Usage**: Minimal resource footprint
-   **Bandwidth**: Efficient response compression
-   **Invocations**: Smart caching strategies

Your API is now ready for production use on Vercel! 🚀
