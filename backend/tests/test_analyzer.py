import pytest
from app.analyzer import analyze_url

def test_safe_looking_url_is_not_claimed_safe():
    result = analyze_url("https://example.org/path")
    assert result["category"] == "NO_KNOWN_THREAT"
    assert 0 <= result["score"] <= 100
    assert result["reasons"]

def test_http_ip_with_login_is_suspicious_or_high_risk():
    result = analyze_url("http://203.0.113.7/login")
    assert result["category"] in {"SUSPICIOUS", "HIGH_RISK"}
    assert result["score"] >= 15

def test_demo_fixture_is_explicitly_synthetic():
    result = analyze_url("https://malware-test.example.com/")
    assert result["category"] == "CONFIRMED_THREAT"
    assert "Synthetic demonstration fixture" in result["reasons"][0]

def test_rejects_non_http_schemes():
    with pytest.raises(ValueError):
        analyze_url("javascript:alert(1)")

def test_rejects_missing_hostname():
    with pytest.raises(ValueError):
        analyze_url("https:///missing-host")
