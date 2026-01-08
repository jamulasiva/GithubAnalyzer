# GitHub Analyzer - Webhook Processing Platform

A comprehensive GitHub webhook processing and audit platform that captures, validates, and analyzes GitHub repository activities in real-time.

## 🚀 Overview

This production-ready platform processes GitHub webhook events through a FastAPI backend with comprehensive Pydantic validation, providing detailed audit trails and analytics for GitHub organization activity.

## ✨ Features

- **25+ GitHub Event Types Supported**
  - Member events (add, permission changes)
  - Organization events (member additions)
  - Repository events (creation, public changes, protection rules)
  - Security events (code scanning, secret scanning, Dependabot alerts)
  - Development events (push, pull requests, issues, reviews)
  - Administrative events (installations, webhooks, teams)

- **Production-Ready Architecture**
  - FastAPI backend with async support
  - Comprehensive Pydantic validation models
  - SQLAlchemy database integration with audit trails
  - Advanced error handling and logging
  - Complete test suite with live server integration

- **Security & Validation**
  - GitHub webhook signature validation
  - Complete payload validation for all event types
  - Secure environment configuration
  - Request/response logging with sanitization

## 🏗️ Architecture

```
├── backend/                     # FastAPI backend application
│   ├── app/                    # Main application code
│   │   ├── api/                # API endpoints
│   │   ├── core/               # Core configuration and database
│   │   ├── middleware/         # Request/response middleware
│   │   ├── models/             # SQLAlchemy database models
│   │   ├── services/           # Business logic services
│   │   └── webhook_models/     # Pydantic webhook validation models
│   ├── tests/                  # Comprehensive test suite
│   │   ├── api/                # API integration tests
│   │   └── payloads/           # Test webhook payloads
│   └── requirements.txt        # Python dependencies
├── documents/                  # Detailed documentation
├── logs/                       # Application logs
└── monitor_logs.sh            # Log monitoring script
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.8+
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Validation**: Pydantic models
- **Testing**: Pytest with live server integration
- **Logging**: Structured logging with rotation
- **Deployment**: Docker-ready, environment-based config

## 📚 Documentation

Comprehensive documentation is available in the `documents/` folder:

- [Requirements](documents/requirements.md) - Detailed project requirements
- [Architecture](documents/architecture.md) - System architecture overview
- [Technology Stack](documents/technology-stack.md) - Technology decisions and rationale
- [Implementation Roadmap](documents/implementation-roadmap.md) - Development roadmap
- [GitHub Webhook Events](documents/github-webhook-events-api.md) - Supported webhook events
- [GitHub Webhook Payloads](documents/github-webhook-payloads.md) - Payload structure documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub webhook endpoint access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jamulasiva/GithubAnalyzer.git
   cd GithubAnalyzer
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database**
   ```bash
   python deploy_schema.py
   ```

5. **Start the server**
   ```bash
   ./start.sh
   # Or manually: uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/api/test_live_server.py -v     # Live server tests
python -m pytest tests/api/test_webhooks.py -v       # Webhook processing tests
```

## 📋 API Endpoints

### Health & Info
- `GET /health` - Health check
- `GET /` - Root endpoint with API info

### Webhooks
- `POST /api/v1/webhooks/github` - GitHub webhook receiver
- `GET /api/v1/webhooks/events` - List supported events

### Audit & Analytics
- `GET /api/v1/audit/organizations` - Organization audit data
- `GET /api/v1/audit/repositories` - Repository audit data
- `GET /api/v1/audit/events` - Webhook event history
- `GET /api/v1/audit/analytics/summary` - Analytics summary

## 🔒 Security

- **Webhook Signature Validation**: All GitHub webhooks are verified using HMAC-SHA256
- **Environment Security**: Sensitive data stored in environment variables
- **Request Sanitization**: All request/response data is sanitized in logs
- **Error Handling**: Comprehensive error handling prevents information leakage

## 🧪 Testing

The platform includes a comprehensive test suite:

- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Live Server Tests**: Real webhook processing validation
- **Payload Validation Tests**: Complete webhook payload validation

## 📊 Monitoring & Logging

- **Structured Logging**: JSON-formatted logs with request tracking
- **Log Rotation**: Automatic log rotation and management
- **Real-time Monitoring**: Live log monitoring scripts
- **Error Tracking**: Dedicated error logging and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 Status

✅ **Production Ready** - All webhook validation errors resolved, comprehensive test coverage, production deployment ready

---

**GitHub Analyzer Platform** - Comprehensive webhook processing for GitHub audit and analytics
