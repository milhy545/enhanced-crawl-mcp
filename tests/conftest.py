"""
Pytest configuration and fixtures.
"""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.core.crawler import CrawlResult
from app.main import app


@pytest.fixture
def client():
    """Fixture for FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_crawl_result():
    """Fixture for mock CrawlResult."""
    return CrawlResult(
        url="https://example.com",
        markdown="# Example Domain\n\nThis is an example.",
        links=["https://example.com/about"],
        images=["https://example.com/logo.png"],
        metadata={"title": "Example Domain"},
        duration_ms=123.45,
        success=True,
    )


@pytest.fixture
def mock_crawler(mock_crawl_result):
    """Fixture for mock WebCrawler."""
    mock = AsyncMock()
    mock.crawl.return_value = mock_crawl_result
    mock.crawl_batch.return_value = [mock_crawl_result]
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    return mock


@pytest.fixture
def sample_urls():
    """Fixture for sample URLs."""
    return ["https://example.com", "https://example.org", "http://example.net"]


@pytest.fixture
def invalid_urls():
    """Fixture for invalid URLs."""
    return [
        "not-a-url",
        "ftp://invalid-scheme.com",
        "javascript:alert('xss')",
        "",
        "   ",
    ]
