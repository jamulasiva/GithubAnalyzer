"""
Request logging middleware for audit and monitoring.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import json
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all API requests for audit and monitoring purposes.
    """
    
    def __init__(self, app, log_requests: bool = True, log_responses: bool = False):
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID for tracking
        request_id = f"{int(time.time())}-{hash(str(request.url))}"
        
        # Log request
        if self.log_requests:
            await self._log_request(request, request_id)
        
        # Process the request
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        # Log response
        if self.log_responses:
            await self._log_response(response, request_id, process_time)
        
        return response
    
    async def _log_request(self, request: Request, request_id: str):
        """Log incoming request details."""
        try:
            log_data = {
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "client": getattr(request.client, 'host', 'unknown') if request.client else 'unknown',
                "user_agent": request.headers.get("user-agent", "unknown")
            }
            
            # Don't log sensitive headers
            sensitive_headers = ['authorization', 'x-hub-signature-256', 'cookie']
            for header in sensitive_headers:
                if header in log_data["headers"]:
                    log_data["headers"][header] = "[REDACTED]"
            
            logger.info(f"Request: {json.dumps(log_data)}")
            
        except Exception as e:
            logger.error(f"Error logging request: {e}")
    
    async def _log_response(self, response: Response, request_id: str, process_time: float):
        """Log response details."""
        try:
            log_data = {
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time": round(process_time, 4),
                "response_headers": dict(response.headers)
            }
            
            logger.info(f"Response: {json.dumps(log_data)}")
            
        except Exception as e:
            logger.error(f"Error logging response: {e}")