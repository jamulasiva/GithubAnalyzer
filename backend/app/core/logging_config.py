"""
Comprehensive logging configuration for GitHub Audit Platform.
Logs all info, debug, errors, and database queries to files outside backend directory.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

# Get the logs directory (outside backend to avoid uvicorn restarts)
LOGS_DIR = Path(__file__).parent.parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green  
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)

class SQLAlchemyFilter(logging.Filter):
    """Filter to capture SQLAlchemy queries and format them nicely."""
    
    def filter(self, record):
        if record.name == 'sqlalchemy.engine.Engine':
            # Format SQL queries for better readability
            if hasattr(record, 'msg'):
                msg = str(record.msg)
                if msg.startswith('BEGIN') or msg.startswith('COMMIT') or msg.startswith('ROLLBACK'):
                    record.msg = f"🔄 TRANSACTION: {msg}"
                elif any(word in msg.upper() for word in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                    record.msg = f"🗄️  SQL QUERY: {msg}"
                elif '[generated in' in msg:
                    record.msg = f"⚡ QUERY TIME: {msg}"
                elif msg.startswith('[raw sql]'):
                    record.msg = f"📊 RAW SQL: {msg}"
                else:
                    record.msg = f"🔧 DB ENGINE: {msg}"
        return True

def setup_logging(log_level: str = "INFO"):
    """
    Setup comprehensive logging configuration.
    
    Creates multiple log files:
    - application.log: All application logs (info, debug, warnings, errors)
    - database.log: All SQLAlchemy database queries and operations
    - errors.log: Only error and critical logs
    - webhook_events.log: Specific webhook processing logs
    """
    
    # Convert log level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)-30s | %(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = ColoredFormatter(
        fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Create handlers
    handlers = []
    
    # 1. Application log file (rotating, keeps 5 files of 10MB each)
    app_handler = logging.handlers.RotatingFileHandler(
        filename=LOGS_DIR / "application.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(detailed_formatter)
    handlers.append(app_handler)
    
    # 2. Database log file (for SQLAlchemy queries)
    db_handler = logging.handlers.RotatingFileHandler(
        filename=LOGS_DIR / "database.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=3,
        encoding='utf-8'
    )
    db_handler.setLevel(logging.INFO)
    db_handler.setFormatter(detailed_formatter)
    db_handler.addFilter(SQLAlchemyFilter())
    handlers.append(db_handler)
    
    # 3. Error log file (errors and critical only)
    error_handler = logging.handlers.RotatingFileHandler(
        filename=LOGS_DIR / "errors.log",
        maxBytes=5*1024*1024,   # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    handlers.append(error_handler)
    
    # 4. Webhook events log file
    webhook_handler = logging.handlers.RotatingFileHandler(
        filename=LOGS_DIR / "webhook_events.log", 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    webhook_handler.setLevel(logging.INFO)
    webhook_handler.setFormatter(detailed_formatter)
    handlers.append(webhook_handler)
    
    # 5. Console handler (colored)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add our handlers
    for handler in handlers:
        root_logger.addHandler(handler)
    
    # Configure SQLAlchemy logging for database queries
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.INFO)
    sqlalchemy_logger.addHandler(db_handler)
    
    # Configure specific loggers
    loggers_config = {
        'app': logging.DEBUG,
        'app.api': logging.DEBUG, 
        'app.services': logging.DEBUG,
        'app.models': logging.DEBUG,
        'app.middleware': logging.DEBUG,
        'webhook_processor': logging.DEBUG,
        'uvicorn.access': logging.INFO,
        'uvicorn.error': logging.INFO,
        'fastapi': logging.INFO,
        'sqlalchemy.engine.Engine': logging.INFO,
    }
    
    for logger_name, level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
    
    # Create webhook-specific logger
    webhook_logger = logging.getLogger('webhook_processor')
    webhook_logger.addHandler(webhook_handler)
    webhook_logger.setLevel(logging.DEBUG)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("🚀 GitHub Audit Platform Logging System Initialized")
    logger.info(f"📂 Log files location: {LOGS_DIR}")
    logger.info(f"📊 Log level: {log_level}")
    logger.info(f"📝 Log files created:")
    logger.info(f"   • application.log - All application logs")
    logger.info(f"   • database.log - Database queries and operations")
    logger.info(f"   • errors.log - Errors and critical issues") 
    logger.info(f"   • webhook_events.log - Webhook processing logs")
    logger.info("=" * 80)
    
    return logger

def get_webhook_logger():
    """Get the webhook-specific logger."""
    return logging.getLogger('webhook_processor')

def log_webhook_event(event_type: str, delivery_id: str, message: str, level: str = "INFO"):
    """
    Log webhook events with consistent formatting.
    
    Args:
        event_type: GitHub event type (push, pull_request, etc.)
        delivery_id: GitHub delivery ID
        message: Log message
        level: Log level (DEBUG, INFO, WARNING, ERROR)
    """
    webhook_logger = get_webhook_logger()
    log_message = f"🔗 {event_type.upper()} | {delivery_id} | {message}"
    
    log_func = getattr(webhook_logger, level.lower(), webhook_logger.info)
    log_func(log_message)

def log_database_operation(operation: str, table: str, details: str = ""):
    """
    Log database operations with consistent formatting.
    
    Args:
        operation: Type of operation (INSERT, UPDATE, DELETE, SELECT)
        table: Database table name
        details: Additional details about the operation
    """
    logger = logging.getLogger('app.database')
    message = f"🗄️  {operation} on {table}"
    if details:
        message += f" | {details}"
    logger.info(message)

# Create a startup message when module is imported
if __name__ != "__main__":
    # Only log import message if not running directly
    logger = logging.getLogger(__name__)
    logger.debug("📋 Logging configuration module imported")