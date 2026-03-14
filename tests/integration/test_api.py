"""
Integration tests for API endpoints.
"""

from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.integration
class TestAPIEndpoints:
    """Test API endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data

    def test_stats_endpoint(self, client):
        """Test stats endpoint."""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert "uptime_seconds" in data
        assert "total_requests" in data

    @patch("app.api.routes.WebCrawler")
    def test_crawl_endpoint_success(self, mock_crawler_class, client, mock_crawl_result):
        """Test successful crawl."""
        # Setup mock
        mock_instance = AsyncMock()
        mock_instance.crawl.return_value = mock_crawl_result
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_crawler_class.return_value = mock_instance

        # Make request
        response = client.post("/crawl", json={"url": "https://example.com"})

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["url"] == "https://example.com"
        assert "markdown" in data

    def test_crawl_endpoint_invalid_url(self, client):
        """Test crawl with invalid URL."""
        response = client.post("/crawl", json={"url": "not-a-url"})
        assert response.status_code == 422  # Validation error

    def test_crawl_endpoint_missing_url(self, client):
        """Test crawl without URL."""
        response = client.post("/crawl", json={})
        assert response.status_code == 422

    def test_validate_url_endpoint_valid(self, client):
        """Test URL validation with valid URL."""
        response = client.post("/crawl/validate", json={"url": "https://example.com"})
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert data["scheme"] == "https"
        assert data["domain"] == "example.com"

    def test_validate_url_endpoint_invalid(self, client):
        """Test URL validation with invalid URL."""
        response = client.post("/crawl/validate", json={"url": "not-a-url"})
        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False

    @patch("app.api.routes.WebCrawler")
    def test_batch_crawl_endpoint(self, mock_crawler_class, client, mock_crawl_result):
        """Test batch crawl endpoint."""
        # Setup mock
        mock_instance = AsyncMock()
        mock_instance.crawl_batch.return_value = [mock_crawl_result, mock_crawl_result]
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_crawler_class.return_value = mock_instance

        # Make request
        response = client.post(
            "/crawl/batch",
            json={"urls": ["https://example.com", "https://example.org"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["total_urls"] == 2
        assert data["completed"] == 2

