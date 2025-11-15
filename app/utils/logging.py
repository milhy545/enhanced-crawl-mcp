"""
Logging configuration and utilities.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from app.config import get_settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if hasattr(record, "url"):
            log_data["url"] = record.url

        if hasattr(record, "duration"):
            log_data["duration_ms"] = record.duration

        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code

        return json.dumps(log_data)


class TextFormatter(logging.Formatter):
    """Custom text formatter for readable logging."""

    def __init__(self):
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        super().__init__(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")


def setup_logging() -> logging.Logger:
    """
    Setup application logging.

    Returns:
        Configured logger instance
    """
    settings = get_settings()

    # Get root logger
    logger = logging.getLogger("crawl_mcp")
    logger.setLevel(settings.log_level)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level)

    # Choose formatter based on settings
    if settings.log_format == "json":
        formatter = JSONFormatter()
    else:
        formatter = TextFormatter()

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if log file is specified
    if settings.log_file:
        log_path = Path(settings.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(settings.log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "crawl_mcp") -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class RequestLogger:
    """Helper class for logging HTTP requests."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_request(self, method: str, path: str, request_id: str, **kwargs: Any) -> None:
        """Log incoming request."""
        extra = {"request_id": request_id, **kwargs}
        self.logger.info(f"Request: {method} {path}", extra=extra)

    def log_response(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        request_id: str,
        **kwargs: Any,
    ) -> None:
        """Log outgoing response."""
        extra = {
            "request_id": request_id,
            "status_code": status_code,
            "duration": duration_ms,
            **kwargs,
        }
        self.logger.info(
            f"Response: {method} {path} - {status_code} ({duration_ms:.2f}ms)", extra=extra
        )

    def log_error(self, message: str, request_id: str, exc_info: Any = None, **kwargs: Any) -> None:
        """Log error with request context."""
        extra = {"request_id": request_id, **kwargs}
        self.logger.error(message, exc_info=exc_info, extra=extra)


class CrawlerLogger:
    """Helper class for logging crawler operations."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_crawl_start(self, url: str, request_id: str, **kwargs: Any) -> None:
        """Log start of crawl operation."""
        extra = {"url": url, "request_id": request_id, **kwargs}
        self.logger.info(f"Starting crawl: {url}", extra=extra)

    def log_crawl_success(
        self, url: str, request_id: str, duration_ms: float, content_length: int, **kwargs: Any
    ) -> None:
        """Log successful crawl."""
        extra = {
            "url": url,
            "request_id": request_id,
            "duration": duration_ms,
            "content_length": content_length,
            **kwargs,
        }
        self.logger.info(
            f"Crawl successful: {url} ({content_length} bytes, {duration_ms:.2f}ms)", extra=extra
        )

    def log_crawl_failure(
        self, url: str, request_id: str, error: str, exc_info: Any = None, **kwargs: Any
    ) -> None:
        """Log failed crawl."""
        extra = {"url": url, "request_id": request_id, "error": error, **kwargs}
        self.logger.error(f"Crawl failed: {url} - {error}", exc_info=exc_info, extra=extra)

    def log_retry(
        self, url: str, request_id: str, attempt: int, max_attempts: int, **kwargs: Any
    ) -> None:
        """Log retry attempt."""
        extra = {
            "url": url,
            "request_id": request_id,
            "attempt": attempt,
            "max_attempts": max_attempts,
            **kwargs,
        }
        self.logger.warning(
            f"Retrying crawl: {url} (attempt {attempt}/{max_attempts})", extra=extra
        )
