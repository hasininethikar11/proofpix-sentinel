from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analyze_endpoint():
    response = client.post("/analyze", json={"url": "https://example.org"})
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "NO_KNOWN_THREAT"
    assert "reasons" in body

def test_invalid_scheme_returns_422():
    response = client.post("/analyze", json={"url": "file:///etc/passwd"})
    assert response.status_code == 422
