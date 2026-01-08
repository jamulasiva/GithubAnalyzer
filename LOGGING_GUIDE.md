# GitHub Audit Platform - Enhanced Logging System

## 🎯 Overview

The GitHub Audit Platform now includes a comprehensive logging system that captures all info, debug, errors, and database queries in dedicated log files **outside the backend directory** to prevent uvicorn from restarting when logs are written.

## 📁 Log File Structure

All logs are saved in: `/home/sivaj/projects/AI-ML/AmzurGitHubAnalyzer/AmzurGitHubAnalyzer-WebHook/AmzurGitHubAnalyzer/logs/`

### Log Files Created:

1. **`application.log`** 📋
   - All application-level logging (INFO, DEBUG, WARNING, ERROR)
   - General application flow and processing
   - FastAPI request/response information
   - Service-level operations

2. **`database.log`** 🗄️
   - All SQLAlchemy database queries and operations
   - Connection management
   - Transaction information (BEGIN, COMMIT, ROLLBACK)
   - Query execution times and parameters

3. **`webhook_events.log`** 🔗
   - Dedicated webhook processing logs
   - Event-specific processing information
   - Delivery ID tracking
   - Webhook validation and signature verification

4. **`errors.log`** ❌
   - Error and critical level logs only
   - Exception details and stack traces
   - Failed operations and troubleshooting info

## 🔧 Features

### Rotating Log Files
- **Application/Database/Webhook logs**: 10MB max, keeps 5 backup files
- **Error logs**: 5MB max, keeps 5 backup files
- Automatic rotation prevents disk space issues

### Enhanced Formatting
- **Timestamp**: `YYYY-MM-DD HH:MM:SS`
- **Log Level**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Module**: Which part of the application generated the log
- **Location**: File and line number
- **Message**: Descriptive log message with emojis for easy identification

### Special Log Categories
- **🔄 TRANSACTION**: Database transactions (BEGIN, COMMIT, ROLLBACK)
- **🗄️ SQL QUERY**: Database SELECT, INSERT, UPDATE, DELETE operations
- **⚡ QUERY TIME**: Query execution timing information
- **🔗 Webhook Events**: GitHub webhook processing with delivery ID tracking
- **🔐 Security**: Signature validation and authentication

## 🚀 Usage

### Configuration
The logging system is automatically initialized when the backend starts. Configuration is controlled via environment variables:

```env
LOG_LEVEL=DEBUG    # DEBUG, INFO, WARNING, ERROR, CRITICAL
DEBUG=true         # Enables detailed logging
```

### Monitoring Logs
Use the provided monitoring script:

```bash
# Monitor all logs
./monitor_logs.sh all

# Monitor specific log types
./monitor_logs.sh app      # Application logs
./monitor_logs.sh db       # Database logs  
./monitor_logs.sh webhook  # Webhook events
./monitor_logs.sh error    # Errors only
```

### Programmatic Logging
The system provides specialized logging functions:

```python
from app.core.logging_config import log_webhook_event, log_database_operation

# Log webhook events
log_webhook_event('push', 'delivery-123', 'Processing push event', 'INFO')

# Log database operations  
log_database_operation('INSERT', 'webhook_events', 'Created new record')
```

## 📊 Log Examples

### Webhook Event Log
```
2026-01-07 11:02:46 | INFO | webhook_processor | 🔗 PUSH | delivery-123 | Processing push event
2026-01-07 11:02:46 | DEBUG | webhook_processor | 🔗 PUSH | delivery-123 | Signature validated
2026-01-07 11:02:46 | INFO | webhook_processor | 🔗 PUSH | delivery-123 | Event processed successfully
```

### Database Query Log
```
2026-01-07 11:02:47 | INFO | sqlalchemy.engine.Engine | 🔄 TRANSACTION: BEGIN (implicit)
2026-01-07 11:02:47 | INFO | sqlalchemy.engine.Engine | 🗄️ SQL QUERY: INSERT INTO webhook_events (...)
2026-01-07 11:02:47 | INFO | sqlalchemy.engine.Engine | ⚡ QUERY TIME: [generated in 0.00052s]
2026-01-07 11:02:47 | INFO | sqlalchemy.engine.Engine | 🔄 TRANSACTION: COMMIT
```

## 🔍 Benefits

### Development Benefits
- **Real-time Debugging**: See exactly what's happening in your application
- **Performance Monitoring**: Track database query execution times
- **Error Tracking**: Dedicated error logs for troubleshooting
- **Webhook Tracing**: Complete audit trail of GitHub webhook processing

### Production Benefits
- **No Backend Restarts**: Logs written outside backend directory
- **Automatic Rotation**: Prevents disk space issues
- **Comprehensive Coverage**: All application activities logged
- **Structured Format**: Easy to parse and analyze

### Testing Benefits
- **Test Data Tracking**: See exactly what data is created during tests
- **Database Operations**: Monitor all SQL queries during test execution  
- **Webhook Processing**: Trace complete webhook processing pipeline
- **Automatic Cleanup**: Test data removal is logged for verification

## 🎛️ Configuration Options

### Log Levels
- **DEBUG**: Everything (recommended for development)
- **INFO**: General information and normal operations
- **WARNING**: Warning messages and potential issues
- **ERROR**: Error conditions and exceptions only
- **CRITICAL**: Critical system errors only

### File Locations
All log files are automatically created in the `logs/` directory outside the backend folder to prevent uvicorn auto-restart issues.

## 🔧 Maintenance

### Log Rotation
- Files automatically rotate when they reach size limits
- Old log files are compressed and retained according to backup count
- No manual intervention required

### Disk Space
- Monitor the `logs/` directory size periodically
- Adjust rotation settings if needed for your environment
- Consider setting up log archival for long-term retention

## 🚀 Integration

The logging system is fully integrated with:
- **FastAPI application startup**
- **Webhook processing pipeline**
- **Database operations**
- **Test execution and cleanup**
- **Error handling and exceptions**

This provides complete visibility into your GitHub Audit Platform operations! 🎉