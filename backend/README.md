# GitHub Audit Platform - Backend

FastAPI-based backend for processing GitHub webhooks and providing audit analytics with Supabase integration.

## 🏗️ Architecture

- **FastAPI**: Modern async Python web framework
- **Supabase**: Backend-as-a-Service with PostgreSQL and real-time capabilities  
- **SQLAlchemy 2.0**: ORM with async support
- **Webhook Processing**: Direct integration with existing `webhook_models` package
- **Real-time Updates**: Supabase subscriptions for live dashboard updates

## 📋 Prerequisites

- Python 3.8+ 
- Supabase project (PostgreSQL database)
- Redis (optional, for background tasks)

## 🚀 Quick Start

1. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

2. **Install and run**:
   ```bash
   ./start.sh
   ```
   
   Or manually:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python main.py
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs  
   - Health Check: http://localhost:8000/health

## 🔧 Configuration

Configure these environment variables in `.env`:

### Required
```bash
# Supabase (get from your Supabase dashboard)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Database (Supabase PostgreSQL connection string)  
DATABASE_URL=postgresql+asyncpg://postgres:password@host:5432/database

# GitHub Webhook Secret
GITHUB_WEBHOOK_SECRET=your_webhook_secret
```

### Optional
```bash
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info
```

## 📊 Database Setup

The backend automatically creates tables on startup, but for production use Supabase migrations:

1. Copy `database_schema.sql` to your Supabase SQL editor
2. Execute the schema to create tables, indexes, and Row Level Security policies
3. The backend will work with the existing schema

## 🔗 API Endpoints

### Webhooks
- `POST /api/v1/webhooks/github` - Main GitHub webhook receiver
- `GET /api/v1/webhooks/github/events` - List supported events
- `GET /api/v1/webhooks/github/test` - Test endpoint
- `POST /api/v1/webhooks/github/simulate` - Simulate events (dev only)

### Audit Data
- `GET /api/v1/audit/organizations` - List organizations
- `GET /api/v1/audit/organizations/{login}` - Organization details  
- `GET /api/v1/audit/repositories` - List repositories
- `GET /api/v1/audit/events` - List webhook events with filtering
- `GET /api/v1/audit/events/{id}` - Event details
- `GET /api/v1/audit/analytics/summary` - Analytics summary

### System
- `GET /health` - Health check
- `GET /api/v1/health` - Detailed health check

## 🎯 Supported GitHub Events

The backend supports 21+ GitHub webhook event types:

- **Repository**: created, publicized, forked, deleted
- **Branches**: create, delete, push  
- **Pull Requests**: opened, closed, merged, reviewed
- **Issues**: opened, closed, commented
- **Members**: added, permission changed, team changes
- **Security**: code scanning, dependabot, secret scanning
- **Organization**: member changes, installations
- **Special**: ping, meta, personal access tokens

## 🏢 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies  
├── .env.example           # Environment configuration template
├── start.sh               # Startup script
├── database_schema.sql    # Complete PostgreSQL schema
└── app/
    ├── api/               # API routes and endpoints
    │   ├── __init__.py   # Main API router
    │   ├── webhooks.py   # GitHub webhook endpoints  
    │   └── audit.py      # Audit data endpoints
    ├── core/              # Core infrastructure
    │   ├── config.py     # Configuration management
    │   └── database.py   # Database connections & Supabase  
    ├── models/            # SQLAlchemy database models
    │   ├── core.py       # Core entities (User, Repo, Org)
    │   └── events.py     # Event-specific models
    ├── services/          # Business logic services
    │   ├── webhook_service.py    # Webhook processing
    │   └── entity_service.py     # Entity management
    └── middleware/        # Custom middleware
        ├── logging.py    # Request/response logging
        └── timing.py     # Performance monitoring
```

## 🔄 Webhook Processing Flow

1. **Receive**: GitHub sends webhook to `/api/v1/webhooks/github`
2. **Validate**: Verify signature using `GITHUB_WEBHOOK_SECRET`  
3. **Parse**: Use existing `webhook_models` to validate payload
4. **Process**: Extract and normalize entities (users, repos, orgs)
5. **Store**: Save to PostgreSQL with full audit trail
6. **Notify**: Real-time updates via Supabase subscriptions

## 🛠️ Development

### Testing
```bash
pytest                    # Run tests
pytest --cov             # With coverage
```

### Code Quality  
```bash
black .                   # Format code
isort .                   # Sort imports
flake8                    # Lint code
```

### Database Migrations
For production, use Supabase migrations instead of auto-creation:
```sql
-- Run database_schema.sql in Supabase SQL editor
-- Backend will connect to existing schema
```

## 📈 Monitoring

- **Health Checks**: `/health` and `/api/v1/health`
- **Logging**: Structured JSON logs with request tracking
- **Metrics**: Response times via `X-Process-Time` headers
- **Database Health**: PostgreSQL and Supabase connectivity checks

## 🔐 Security

- **Webhook Signature Validation**: All GitHub webhooks verified
- **CORS**: Configured for frontend domains
- **Rate Limiting**: Supabase built-in protection  
- **Input Validation**: Pydantic model validation
- **SQL Injection**: SQLAlchemy ORM protection

## 🚀 Production Deployment

1. **Environment**: Set `ENVIRONMENT=production` and `DEBUG=false`
2. **Database**: Use Supabase production instance
3. **Secrets**: Store credentials securely (not in code)
4. **Monitoring**: Set up logging and health check monitoring
5. **Scaling**: Configure uvicorn workers for high traffic

## 🤝 Integration

This backend integrates seamlessly with:
- **Webhook Models**: Direct use of existing `webhook_models` package
- **Supabase Dashboard**: Real-time data views
- **Frontend**: CORS-enabled API for React dashboard
- **GitHub**: Complete webhook event support

---

*Ready for Supabase credentials! Once you share the connection details, the backend will be fully operational.*