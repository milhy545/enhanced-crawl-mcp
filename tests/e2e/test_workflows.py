"""
End-to-end workflow tests.
"""

import pytest
from unittest.mock import patch, AsyncMock

from app.core.crawler import CrawlResult


@pytest.mark.e2e
class TestWorkflows:
    """Test complete user workflows."""
    
    @patch("app.api.routes.WebCrawler")
    def test_complete_crawl_workflow(self, mock_crawler_class, client):
        """Test complete crawl workflow."""
        # Create mock result
        mock_result = CrawlResult(
            url="https://example.com",
            markdown="# Example\n\nContent here.",
            links=["https://example.com/about"],
            images=["https://example.com/logo.png"],
            metadata={"title": "Example"},
            duration_ms=150.0,
            success=True
        )
        
        # Setup mock
        mock_instance = AsyncMock()
        mock_instance.crawl.return_value = mock_result
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_crawler_class.return_value = mock_instance
        
        # 1. Validate URL first
        response = client.post("/crawl/validate", json={"url": "https://example.com"})
        assert response.status_code == 200
        assert response.json()["is_valid"] is True
        
        # 2. Crawl the URL
        response = client.post(
            "/crawl",
            json={
                "url": "https://example.com",
                "include_links": True,
                "include_images": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["links"]) > 0
        assert len(data["images"]) > 0
    
    @patch("app.api.routes.WebCrawler")
    def test_batch_crawl_workflow(self, mock_crawler_class, client):
        """Test batch crawl workflow."""
        # Create mock results
        mock_result1 = CrawlResult(
            url="https://example.com",
            markdown="# Example 1",
            success=True
        )
        mock_result2 = CrawlResult(
            url="https://example.org",
            markdown="# Example 2",
            success=True
        )
        
        # Setup mock
        mock_instance = AsyncMock()
        mock_instance.crawl_batch.return_value = [mock_result1, mock_result2]
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_crawler_class.return_value = mock_instance
        
        # 1. Submit batch crawl
        response = client.post(
            "/crawl/batch",
            json={"urls": ["https://example.com", "https://example.org"]}
        )
        assert response.status_code == 200
        data = response.json()
        job_id = data["job_id"]
        assert data["total_urls"] == 2
        
        # 2. Check job status
        response = client.get(f"/crawl/status/{job_id}")
        assert response.status_code == 200
        status_data = response.json()
        assert status_data["job_id"] == job_id
        assert status_data["status"] == "completed"
    
    def test_error_handling_workflow(self, client):
        """Test error handling workflow."""
        # Invalid URL
        response = client.post("/crawl", json={"url": "ftp://invalid.com"})
        assert response.status_code == 422
        
        # Empty URL
        response = client.post("/crawl", json={"url": ""})
        assert response.status_code == 422
        
        # Job not found
        response = client.get("/crawl/status/nonexistent_job")
        assert response.status_code == 404

