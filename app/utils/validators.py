"""
URL validation utilities.
"""

from urllib.parse import urlparse

from app.config import get_settings
from app.core.exceptions import BlockedDomainError, URLValidationError


def validate_url(url: str) -> tuple[str, str]:
    """
    Validate URL and extract scheme and domain.

    Args:
        url: URL string to validate

    Returns:
        Tuple of (scheme, domain)

    Raises:
        URLValidationError: If URL is invalid
        BlockedDomainError: If domain is blocked
    """
    settings = get_settings()

    # Parse URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise URLValidationError(url, f"Failed to parse URL: {str(e)}") from e

    # Validate scheme
    if not parsed.scheme:
        raise URLValidationError(url, "Missing URL scheme")

    if parsed.scheme not in settings.allowed_schemes:
        raise URLValidationError(
            url,
            f"Scheme '{parsed.scheme}' not allowed. Allowed schemes: {', '.join(settings.allowed_schemes)}",
        )

    # Validate domain
    if not parsed.netloc:
        raise URLValidationError(url, "Missing domain")

    domain = parsed.netloc.lower()

    # Check blocked domains
    for blocked in settings.blocked_domains:
        if blocked.lower() in domain:
            raise BlockedDomainError(url, domain)

    return parsed.scheme, domain


def is_valid_url(url: str) -> bool:
    """
    Check if URL is valid without raising exceptions.

    Args:
        url: URL string to check

    Returns:
        True if valid, False otherwise
    """
    try:
        validate_url(url)
        return True
    except (URLValidationError, BlockedDomainError):
        return False


def normalize_url(url: str) -> str:
    """
    Normalize URL by adding scheme if missing and removing trailing slashes.

    Args:
        url: URL to normalize

    Returns:
        Normalized URL
    """
    url = url.strip()

    # Add https:// if no scheme
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    # Remove trailing slash
    if url.endswith("/") and len(url) > 1:
        url = url.rstrip("/")

    return url


def extract_domain(url: str) -> str:
    """
    Extract domain from URL.

    Args:
        url: URL to extract domain from

    Returns:
        Domain string

    Raises:
        URLValidationError: If URL is invalid
    """
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            raise URLValidationError(url, "Cannot extract domain - missing netloc")
        return parsed.netloc.lower()
    except Exception as e:
        raise URLValidationError(url, f"Failed to extract domain: {str(e)}") from e
