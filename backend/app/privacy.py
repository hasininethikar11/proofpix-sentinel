from urllib.parse import urlsplit, urlunsplit

def normalize_url(raw_url: str) -> tuple[str, str, str]:
    """Validate and normalize an HTTP(S) URL. Return normalized URL, hostname, scheme."""
    raw_url = raw_url.strip()
    if not raw_url or len(raw_url) > 4096:
        raise ValueError("URL is empty or too long")
    try:
        parts = urlsplit(raw_url)
        scheme = parts.scheme.lower()
        hostname = (parts.hostname or "").rstrip(".").lower()
        # Accessing .port can raise ValueError for malformed ports.
        port = parts.port
    except ValueError as exc:
        raise ValueError("Malformed URL") from exc
    if scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are supported")
    if not hostname or any(ch.isspace() for ch in hostname):
        raise ValueError("URL must include a valid hostname")
    if parts.username is not None or parts.password is not None:
        # Strip credentials from the returned URL to avoid reflecting secrets.
        netloc = hostname
        if port is not None:
            netloc += f":{port}"
    else:
        netloc = hostname + (f":{port}" if port is not None else "")
    normalized = urlunsplit((scheme, netloc, parts.path or "/", parts.query, ""))
    return normalized, hostname, scheme
