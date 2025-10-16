"""
API dependencies and utilities.
"""

import time
import uuid
from typing import Any

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import get_settings
from app.utils.logging import RequestLogger, get_logger

logger = get_logger(__name__)
request_logger = RequestLogger(logger)

# In-memory storage for stats (in production, use Redis or database)
server_stats: dict[str, Any] = {
    "start_time": time.time(),
    "total_requests": 0,
    "successful_crawls": 0,
    "failed_crawls": 0,
    "active_jobs": 0,
    "response_times": [],
}

# In-memory job storage (in production, use Redis or database)
jobs_storage: dict = {}


def get_request_id() -> str:
    """Generate a unique request ID."""
    return str(uuid.uuid4())


def get_stats() -> dict:
    """Get current server statistics."""
    uptime = time.time() - server_stats["start_time"]
    avg_response_time = (
        sum(server_stats["response_times"]) / len(server_stats["response_times"])
        if server_stats["response_times"]
        else 0.0
    )

    return {
        "uptime_seconds": uptime,
        "total_requests": server_stats["total_requests"],
        "successful_crawls": server_stats["successful_crawls"],
        "failed_crawls": server_stats["failed_crawls"],
        "active_jobs": server_stats["active_jobs"],
        "avg_response_time": avg_response_time,
    }


def increment_request_count():
    """Increment total request counter."""
    server_stats["total_requests"] += 1


def increment_crawl_success():
    """Increment successful crawl counter."""
    server_stats["successful_crawls"] += 1


def increment_crawl_failure():
    """Increment failed crawl counter."""
    server_stats["failed_crawls"] += 1


def add_response_time(duration_ms: float):
    """Add response time to statistics."""
    server_stats["response_times"].append(duration_ms)
    # Keep only last 1000 response times
    if len(server_stats["response_times"]) > 1000:
        server_stats["response_times"] = server_stats["response_times"][-1000:]


def store_job(job_id: str, job_data: dict):
    """Store job data."""
    jobs_storage[job_id] = job_data


def get_job(job_id: str) -> dict | None:
    """Retrieve job data."""
    return jobs_storage.get(job_id)


def update_job(job_id: str, updates: dict):
    """Update job data."""
    if job_id in jobs_storage:
        jobs_storage[job_id].update(updates)


def delete_job(job_id: str):
    """Delete job data."""
    if job_id in jobs_storage:
        del jobs_storage[job_id]


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add request ID to all requests."""

    async def dispatch(self, request: Request, call_next):
        request_id = get_request_id()
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging."""

    async def dispatch(self, request: Request, call_next):
        request_id = getattr(request.state, "request_id", "unknown")
        start_time = time.time()

        # Log request
        request_logger.log_request(request.method, request.url.path, request_id)

        # Increment request counter
        increment_request_count()

        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Request processing error: {str(e)}", exc_info=e)
            raise

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        add_response_time(duration_ms)

        # Log response
        request_logger.log_response(
            request.method, request.url.path, response.status_code, duration_ms, request_id
        )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""

    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        settings = get_settings()

        if not settings.rate_limit_enabled:
            return await call_next(request)

        # Use IP address as key (in production, use API key or user ID)
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Clean old entries
        self.requests = {
            ip: timestamps
            for ip, timestamps in self.requests.items()
            if any(t > current_time - 60 for t in timestamps)
        }

        # Check rate limit
        if client_ip in self.requests:
            # Remove timestamps older than 1 minute
            self.requests[client_ip] = [
                t for t in self.requests[client_ip] if t > current_time - 60
            ]

            if len(self.requests[client_ip]) >= settings.rate_limit_requests:
                raise HTTPException(
                    status_code=429, detail="Rate limit exceeded. Please try again later."
                )
        else:
            self.requests[client_ip] = []

        # Add current request
        self.requests[client_ip].append(current_time)

        return await call_next(request)
