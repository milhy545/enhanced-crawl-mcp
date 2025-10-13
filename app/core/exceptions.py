"""
Custom exceptions for the Crawl MCP application.
"""

from typing import Optional, Any


class CrawlMCPException(Exception):
    """Base exception for all Crawl MCP errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(CrawlMCPException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class URLValidationError(ValidationError):
    """Raised when URL validation fails."""
    
    def __init__(self, url: str, reason: str):
        message = f"Invalid URL: {url}. Reason: {reason}"
        super().__init__(message, details={"url": url, "reason": reason})


class CrawlError(CrawlMCPException):
    """Raised when crawling operation fails."""
    
    def __init__(self, message: str, url: Optional[str] = None, details: Optional[dict[str, Any]] = None):
        final_details = details or {}
        if url:
            final_details["url"] = url
        super().__init__(message, status_code=500, details=final_details)


class CrawlTimeoutError(CrawlError):
    """Raised when crawl operation times out."""
    
    def __init__(self, url: str, timeout: int):
        message = f"Crawl timeout for URL: {url} (timeout: {timeout}s)"
        super().__init__(message, url=url, details={"timeout": timeout})


class CrawlRetryExhaustedError(CrawlError):
    """Raised when all retry attempts are exhausted."""
    
    def __init__(self, url: str, attempts: int):
        message = f"All {attempts} retry attempts exhausted for URL: {url}"
        super().__init__(message, url=url, details={"attempts": attempts})


class BlockedDomainError(CrawlError):
    """Raised when attempting to crawl a blocked domain."""
    
    def __init__(self, url: str, domain: str):
        message = f"Domain {domain} is blocked from crawling"
        super().__init__(message, url=url, details={"domain": domain})


class RateLimitError(CrawlMCPException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        details = {"retry_after": retry_after} if retry_after else {}
        super().__init__(message, status_code=429, details=details)


class JobNotFoundError(CrawlMCPException):
    """Raised when a job is not found."""
    
    def __init__(self, job_id: str):
        message = f"Job not found: {job_id}"
        super().__init__(message, status_code=404, details={"job_id": job_id})


class ContentExtractionError(CrawlError):
    """Raised when content extraction fails."""
    
    def __init__(self, url: str, reason: str):
        message = f"Failed to extract content from {url}: {reason}"
        super().__init__(message, url=url, details={"reason": reason})

