from app import app


def test_home_endpoint():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert "version" in response.json


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_readiness_and_metrics_endpoints():
    client = app.test_client()

    assert client.get("/ready").json["status"] == "ready"
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert b"http_requests_total" in metrics.data
