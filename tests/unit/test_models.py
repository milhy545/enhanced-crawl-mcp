"""
Unit tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError
from datetime import datetime

from app.models import (
    CrawlRequest,
    BatchCrawlRequest,
    URLValidationRequest,
    CrawlResponse,
    JobStatus
)


class TestCrawlRequest:
    """Test CrawlRequest model."""
    
    def test_valid_request(self):
        """Test valid crawl request."""
        request = CrawlRequest(url="https://example.com")
        assert request.url == "https://example.com"
        assert request.include_links is False
        assert request.max_depth == 1
    
    def test_url_validation(self):
        """Test URL validation."""
        # Valid URLs
        request = CrawlRequest(url="  https://example.com  ")
        assert request.url == "https://example.com"
        
        # Invalid URLs
        with pytest.raises(ValidationError):
            CrawlRequest(url="")
        
        with pytest.raises(ValidationError):
            CrawlRequest(url="not-a-url")
    
    def test_max_depth_validation(self):
        """Test max_depth validation."""
        request = CrawlRequest(url="https://example.com", max_depth=3)
        assert request.max_depth == 3
        
        # Out of range
        with pytest.raises(ValidationError):
            CrawlRequest(url="https://example.com", max_depth=10)


class TestBatchCrawlRequest:
    """Test BatchCrawlRequest model."""
    
    def test_valid_request(self):
        """Test valid batch request."""
        request = BatchCrawlRequest(urls=["https://example.com", "https://example.org"])
        assert len(request.urls) == 2
    
    def test_urls_validation(self):
        """Test URLs validation."""
        # Strip whitespace
        request = BatchCrawlRequest(urls=["  https://example.com  ", "https://example.org"])
        assert request.urls == ["https://example.com", "https://example.org"]
        
        # Remove empty strings
        request = BatchCrawlRequest(urls=["https://example.com", "", "  "])
        assert len(request.urls) == 1
        
        # Invalid URL format
        with pytest.raises(ValidationError):
            BatchCrawlRequest(urls=["not-a-url"])
        
        # Empty list
        with pytest.raises(ValidationError):
            BatchCrawlRequest(urls=[])
        
        # Too many URLs
        with pytest.raises(ValidationError):
            BatchCrawlRequest(urls=["https://example.com"] * 101)


class TestCrawlResponse:
    """Test CrawlResponse model."""
    
    def test_response_creation(self):
        """Test response creation."""
        response = CrawlResponse(
            status="success",
            url="https://example.com",
            markdown="# Test"
        )
        assert response.status == "success"
        assert response.url == "https://example.com"
        assert isinstance(response.crawled_at, datetime)

