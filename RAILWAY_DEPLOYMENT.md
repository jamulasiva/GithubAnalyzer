# Railway.com Deployment Guide

## Prerequisites

1. [Railway.com](https://railway.app) account
2. GitHub repository (already set up)
3. Railway CLI (optional but recommended)

## Deployment Steps

### 1. Connect Repository to Railway

1. Go to [Railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `jamulasiva/GithubAnalyzer` repository
5. Railway will automatically detect the Python project and deploy from the root directory

### 2. Configure Environment Variables

In Railway dashboard, add these environment variables:

#### Required Variables:
```bash
# Database (Railway will auto-provide DATABASE_URL when you add PostgreSQL)
DATABASE_URL=<auto-provided-by-railway-postgres>

# GitHub Webhook Secret (create this in your GitHub webhook settings)
GITHUB_WEBHOOK_SECRET=your-webhook-secret-here

# Security (generate a secure random string)
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
```

#### Optional Variables:
```bash
# CORS (update with your frontend domains)
ALLOWED_ORIGINS=["https://your-frontend.com"]

# Redis (if using Railway Redis add-on)
REDIS_URL=<auto-provided-by-railway-redis>
```

### 3. Add Database Service

1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway will automatically provide the `DATABASE_URL` environment variable

### 4. Configure GitHub Webhook

1. Go to your GitHub repository settings
2. Navigate to "Webhooks" → "Add webhook"
3. Set Payload URL to: `https://your-app.railway.app/api/v1/webhooks/github`
4. Set Content type: `application/json`
5. Set Secret: Use the same value as `GITHUB_WEBHOOK_SECRET`
6. Select events you want to monitor

### 5. Deploy

Railway will automatically deploy when you push to your repository. You can also:

1. Manual deploy from Railway dashboard
2. Use Railway CLI: `railway deploy`

## Post-Deployment

### 1. Initialize Database
The application will automatically create tables on first run.

### 2. Health Check
Visit: `https://your-app.railway.app/health`

### 3. API Documentation
Visit: `https://your-app.railway.app/docs`

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | Auto-provided |
| `GITHUB_WEBHOOK_SECRET` | GitHub webhook secret | Yes | None |
| `SECRET_KEY` | Application secret key | Yes | None |
| `ENVIRONMENT` | Environment name | No | production |
| `DEBUG` | Debug mode | No | false |
| `LOG_LEVEL` | Logging level | No | info |
| `ALLOWED_ORIGINS` | CORS allowed origins | No | [] |
| `REDIS_URL` | Redis connection string | No | None |

## Monitoring

- **Logs**: Available in Railway dashboard
- **Metrics**: Railway provides CPU, memory, and network metrics
- **Health Check**: `/health` endpoint for monitoring

## Scaling

Railway automatically scales based on traffic. You can configure:
- Memory limits
- CPU limits
- Auto-scaling triggers

## Custom Domain

1. In Railway dashboard, go to your service
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Configure DNS records as instructed

## Troubleshooting

### Common Issues:

1. **Build Failures**: Check `requirements.txt` and Python version
2. **Database Connection**: Ensure `DATABASE_URL` is set correctly
3. **Environment Variables**: Verify all required variables are set
4. **Port Issues**: Railway automatically sets `$PORT`, don't override it

### Logs:
```bash
# Using Railway CLI
railway logs

# Or check Railway dashboard logs section
```

### Local Testing:
```bash
# Set environment variables
export ENVIRONMENT=production
export DEBUG=false
# ... other variables

# Test locally
uvicorn main:app --host 0.0.0.0 --port 8000
```