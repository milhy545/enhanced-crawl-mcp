"""
Edge case and stress tests.
"""

import pytest
from unittest.mock import patch, AsyncMock
import asyncio

from app.core.crawler import CrawlResult


@pytest.mark.integration
class TestEdgeCases:
    """Test edge cases and error scenarios."""
    
    def test_invalid_url_schemes(self, client):
        """Test various invalid URL schemes."""
        invalid_urls = [
            "ftp://example.com",
            "file:///etc/passwd",
            "javascript:alert('xss')",
            "data:text/html,<script>alert('xss')</script>"
        ]
        
        for url in invalid_urls:
            response = client.post("/crawl/validate", json={"url": url})
            assert response.status_code == 200
            assert response.json()["is_valid"] is False
    
    def test_malformed_urls(self, client, invalid_urls):
        """Test malformed URLs."""
        for url in invalid_urls:
            if url.strip():  # Skip empty strings
                response = client.post("/crawl", json={"url": url})
                assert response.status_code in [400, 422]
    
    @patch("app.api.routes.WebCrawler")
    def test_timeout_handling(self, mock_crawler_class, client):
        """Test timeout handling."""
        # Setup mock to raise timeout
        mock_instance = AsyncMock()
        mock_instance.crawl.side_effect = asyncio.TimeoutError()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_crawler_class.return_value = mock_instance
        
        response = client.post(
            "/crawl",
            json={"url": "https://slow-website.com", "timeout": 5}
        )
        # Should handle timeout gracefully
        assert response.status_code in [500, 504]
    
    def test_very_long_url(self, client):
        """Test very long URL."""
        long_url = "https://example.com/" + "a" * 10000
        response = client.post("/crawl", json={"url": long_url})
        # Should either accept or reject gracefully
        assert response.status_code in [200, 400, 422, 500]
    
    @patch("app.api.routes.WebCrawler")
    def test_concurrent_requests(self, mock_crawler_class, client):
        """Test handling of concurrent requests."""
        mock_result = CrawlResult(
            url="https://example.com",
            markdown="# Test",
            success=True
        )
        
        # Setup mock
        mock_instance = AsyncMock()
        mock_instance.crawl.return_value = mock_result
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_crawler_class.return_value = mock_instance
        
        # Make multiple concurrent requests
        import concurrent.futures
        
        def make_request():
            return client.post("/crawl", json={"url": "https://example.com"})
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All should succeed
        assert all(r.status_code == 200 for r in results)
    
    def test_batch_with_max_urls(self, client):
        """Test batch crawl with maximum URLs."""
        urls = [f"https://example{i}.com" for i in range(100)]
        response = client.post("/crawl/batch", json={"urls": urls})
        assert response.status_code in [200, 400]
        
        # Test exceeding limit
        urls = [f"https://example{i}.com" for i in range(101)]
        response = client.post("/crawl/batch", json={"urls": urls})
        assert response.status_code == 422
    
    def test_special_characters_in_url(self, client):
        """Test URLs with special characters."""
        special_urls = [
            "https://example.com/path?param=value&other=test",
            "https://example.com/路径/中文",
            "https://example.com/path#fragment",
            "https://user:pass@example.com/path"
        ]
        
        for url in special_urls:
            response = client.post("/crawl/validate", json={"url": url})
            # Should either validate or reject gracefully
            assert response.status_code == 200

