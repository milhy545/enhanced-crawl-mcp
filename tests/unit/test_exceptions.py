"""
Unit tests for exceptions module.
"""

import pytest

from app.core.exceptions import (
    CrawlMCPException,
    ValidationError,
    URLValidationError,
    CrawlError,
    CrawlTimeoutError,
    BlockedDomainError,
    RateLimitError,
    JobNotFoundError
)


class TestExceptions:
    """Test custom exceptions."""
    
    def test_base_exception(self):
        """Test base CrawlMCPException."""
        exc = CrawlMCPException("Test error", status_code=500, details={"key": "value"})
        assert exc.message == "Test error"
        assert exc.status_code == 500
        assert exc.details == {"key": "value"}
        assert str(exc) == "Test error"
    
    def test_validation_error(self):
        """Test ValidationError."""
        exc = ValidationError("Invalid input", details={"field": "url"})
        assert exc.status_code == 400
        assert exc.details == {"field": "url"}
    
    def test_url_validation_error(self):
        """Test URLValidationError."""
        exc = URLValidationError("https://example.com", "Invalid format")
        assert exc.status_code == 400
        assert exc.details["url"] == "https://example.com"
        assert exc.details["reason"] == "Invalid format"
    
    def test_crawl_timeout_error(self):
        """Test CrawlTimeoutError."""
        exc = CrawlTimeoutError("https://example.com", 30)
        assert "timeout" in exc.message.lower()
        assert exc.details["timeout"] == 30
    
    def test_blocked_domain_error(self):
        """Test BlockedDomainError."""
        exc = BlockedDomainError("https://blocked.com", "blocked.com")
        assert "blocked" in exc.message.lower()
        assert exc.details["domain"] == "blocked.com"
    
    def test_rate_limit_error(self):
        """Test RateLimitError."""
        exc = RateLimitError(retry_after=60)
        assert exc.status_code == 429
        assert exc.details["retry_after"] == 60
    
    def test_job_not_found_error(self):
        """Test JobNotFoundError."""
        exc = JobNotFoundError("job_123")
        assert exc.status_code == 404
        assert exc.details["job_id"] == "job_123"

