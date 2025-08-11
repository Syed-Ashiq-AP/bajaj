# Vercel Deployment Checklist

Use this checklist to ensure a successful deployment to Vercel.

## Pre-Deployment Checklist

### ✅ Code Preparation

-   [ ] All unwanted files removed (`example.py`, `main.py`, etc.)
-   [ ] Core modules copied to `api/` directory
-   [ ] `vercel.json` configuration file created
-   [ ] `api/requirements.txt` with correct dependencies
-   [ ] Environment variables template (`.env.vercel`) created

### ✅ API Structure

-   [ ] `api/index.py` - Vercel entry point created
-   [ ] `api/document_processor.py` - Core logic available
-   [ ] `api/ai_generator.py` - AI integration available
-   [ ] All imports working correctly
-   [ ] Serverless optimizations applied

### ✅ Configuration

-   [ ] Maximum function duration set (300 seconds)
-   [ ] Memory optimizations implemented
-   [ ] Cold start handling added
-   [ ] Error handling for serverless environment

## Deployment Steps

### Step 1: Environment Setup

-   [ ] Vercel account created
-   [ ] Vercel CLI installed (`npm i -g vercel`)
-   [ ] A4F API keys ready

### Step 2: Repository Setup

-   [ ] Code pushed to GitHub/GitLab/Bitbucket
-   [ ] Repository is public or Vercel has access
-   [ ] `.gitignore` configured properly

### Step 3: Vercel Configuration

-   [ ] Project connected to Vercel
-   [ ] Environment variables added:
    -   [ ] `A4F_API_KEY_1`
    -   [ ] `A4F_API_KEY_2`
    -   [ ] `A4F_API_KEY_3`
    -   [ ] `A4F_API_KEY_4`
    -   [ ] `ENVIRONMENT=production`

### Step 4: Deploy

-   [ ] Run `vercel` command or deploy via dashboard
-   [ ] Build successful (no errors)
-   [ ] Functions deployed correctly
-   [ ] URL generated

## Post-Deployment Verification

### ✅ Basic Functionality

-   [ ] Root endpoint (`/`) responds correctly
-   [ ] Health check (`/health`) shows AI enabled
-   [ ] Authentication working with Bearer token
-   [ ] CORS headers configured if needed

### ✅ API Testing

-   [ ] PDF download and processing works
-   [ ] Semantic search functioning
-   [ ] AI answer generation working
-   [ ] Response format matches specification
-   [ ] Error handling working properly

### ✅ Performance Testing

-   [ ] Cold start time acceptable (< 30 seconds)
-   [ ] Processing time within limits (< 5 minutes)
-   [ ] Memory usage efficient
-   [ ] Concurrent requests handled

## Testing Commands

```bash
# Test health endpoint
curl https://your-app.vercel.app/health

# Test main API
curl -X POST "https://your-app.vercel.app/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer e6faf945ec7e60f041eb2a7069834e67ee6c31f847e7cb7f0dee01e6d11312b5" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
      "What is the grace period for premium payment?",
      "What is the waiting period for pre-existing diseases?"
    ]
  }'

# Run comprehensive test
python test_vercel.py https://your-app.vercel.app
```

## Monitoring Setup

### ✅ Vercel Analytics

-   [ ] Analytics enabled in dashboard
-   [ ] Function performance monitoring
-   [ ] Error tracking configured
-   [ ] Usage metrics reviewed

### ✅ Logging

-   [ ] Log levels configured
-   [ ] Error logs accessible via `vercel logs`
-   [ ] Performance metrics tracked

## Troubleshooting Guide

### Common Issues & Solutions

#### ❌ Build Failures

-   Check `api/requirements.txt` for correct dependencies
-   Ensure all imports are available in `api/` directory
-   Verify Python version compatibility

#### ❌ Timeout Errors

-   Check function duration limit (300s max)
-   Optimize model loading (lazy initialization)
-   Reduce PDF processing complexity

#### ❌ Memory Issues

-   Use CPU-only versions of ML libraries
-   Implement efficient memory management
-   Monitor memory usage in logs

#### ❌ API Key Issues

-   Verify environment variables in Vercel dashboard
-   Check variable names match exactly
-   Ensure keys are marked as secrets

#### ❌ Import Errors

-   All required modules in `api/` directory
-   Check relative import paths
-   Verify dependencies in requirements.txt

## Success Criteria

Your deployment is successful when:

-   [ ] ✅ Health endpoint returns `{"status": "healthy", "ai_enabled": true}`
-   [ ] ✅ Main API processes PDF and returns answers
-   [ ] ✅ Response time < 2 minutes for typical documents
-   [ ] ✅ Error rate < 1%
-   [ ] ✅ All test cases pass

## Next Steps After Deployment

1. **Domain Setup**: Configure custom domain if needed
2. **Rate Limiting**: Implement if expecting high traffic
3. **Caching**: Add Redis/memory caching for performance
4. **Monitoring**: Set up alerts for errors/performance
5. **Documentation**: Update API docs with production URL

## Production URL

Once deployed, your API will be available at:

```
https://your-project-name.vercel.app
```

Update all documentation and client code with the production URL.

---

**Deployment Status**: ⏳ Ready for deployment
**Last Updated**: August 11, 2025
**Version**: 1.0.0
