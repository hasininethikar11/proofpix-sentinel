from urllib.parse import urlsplit
from .privacy import normalize_url
from .threat_intelligence import DEMO_THREAT_HOSTS

SHORTENER_HOSTS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "ow.ly", "buff.ly"}
SUSPICIOUS_TERMS = {"login", "verify", "account", "secure", "update", "password", "wallet", "invoice"}

def analyze_url(raw_url: str) -> dict:
    normalized, host, scheme = normalize_url(raw_url)
    path_query = (urlsplit(normalized).path + "?" + urlsplit(normalized).query).lower()
    reasons: list[str] = []
    score = 0

    if host in DEMO_THREAT_HOSTS:
        return {"url": normalized, "category": "CONFIRMED_THREAT", "score": 100,
                "reasons": ["Synthetic demonstration fixture matched; this is not a real threat-intelligence verdict."]}

    try:
        import ipaddress
        ipaddress.ip_address(host.strip("[]"))
        reasons.append("The destination uses an IP address instead of a conventional domain name.")
        score += 25
    except ValueError:
        pass

    if scheme == "http":
        reasons.append("The link uses HTTP rather than encrypted HTTPS.")
        score += 10

    if "xn--" in host:
        reasons.append("The domain contains an internationalized/punycode label that can merit closer inspection.")
        score += 20

    if host.count("-") >= 3:
        reasons.append("The hostname contains several hyphens, which can be used in deceptive domains.")
        score += 10

    if len(host) > 45:
        reasons.append("The hostname is unusually long.")
        score += 10

    if host in SHORTENER_HOSTS:
        reasons.append("This is a URL-shortening service, so the final destination is not visible here.")
        score += 15

    found_terms = sorted(term for term in SUSPICIOUS_TERMS if term in path_query)
    if found_terms:
        reasons.append("The path or query contains sensitive-action words: " + ", ".join(found_terms) + ".")
        score += min(20, 5 * len(found_terms))

    score = min(score, 95)
    if score >= 50:
        category = "HIGH_RISK"
    elif score >= 15:
        category = "SUSPICIOUS"
    else:
        category = "NO_KNOWN_THREAT"
    if not reasons:
        reasons.append("No configured heuristic indicators were found. This does not prove the URL is safe.")
    return {"url": normalized, "category": category, "score": score, "reasons": reasons}
