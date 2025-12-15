"""
Unit tests for validators module.
"""

import pytest

from app.core.exceptions import URLValidationError
from app.utils.validators import extract_domain, is_valid_url, normalize_url, validate_url


class TestValidators:
    """Test URL validators."""

    def test_validate_url_success(self):
        """Test successful URL validation."""
        scheme, domain = validate_url("https://example.com")
        assert scheme == "https"
        assert domain == "example.com"

        scheme, domain = validate_url("http://example.org")
        assert scheme == "http"
        assert domain == "example.org"

    def test_validate_url_missing_scheme(self):
        """Test URL without scheme."""
        with pytest.raises(URLValidationError) as exc:
            validate_url("example.com")
        assert "Missing URL scheme" in str(exc.value)

    def test_validate_url_invalid_scheme(self):
        """Test URL with invalid scheme."""
        with pytest.raises(URLValidationError) as exc:
            validate_url("ftp://example.com")
        assert "not allowed" in str(exc.value)

    def test_validate_url_missing_domain(self):
        """Test URL without domain."""
        with pytest.raises(URLValidationError) as exc:
            validate_url("https://")
        assert "Missing domain" in str(exc.value)

    def test_is_valid_url(self):
        """Test is_valid_url function."""
        assert is_valid_url("https://example.com") is True
        assert is_valid_url("http://example.org") is True
        assert is_valid_url("ftp://invalid.com") is False
        assert is_valid_url("not-a-url") is False

    def test_normalize_url(self):
        """Test URL normalization."""
        assert normalize_url("example.com") == "https://example.com"
        assert normalize_url("http://example.com/") == "http://example.com"
        assert normalize_url("  https://example.com  ") == "https://example.com"

    def test_extract_domain(self):
        """Test domain extraction."""
        assert extract_domain("https://example.com") == "example.com"
        assert (
            extract_domain("http://subdomain.example.org:8080/path") == "subdomain.example.org:8080"
        )

        with pytest.raises(URLValidationError):
            extract_domain("not-a-url")
