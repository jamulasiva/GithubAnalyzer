"""
Request timing middleware to track API response times.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track request timing and log slow requests.
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process the request
        response: Response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add timing header
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log slow requests (over 1 second)
        if process_time > 1.0:
            logger.warning(
                f"Slow request: {request.method} {request.url} "
                f"took {process_time:.2f}s"
            )
        
        return response