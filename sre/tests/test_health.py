import pytest
from flask import Flask
from apps.core.models import Project # Placeholder import to satisfy type checking if needed

# Note: We rely on the fixtures defined in conftest.py
# We use the auth_client fixture for authenticated tests.

def test_health_check_endpoint_returns_ok(client):
    """
    Tests that the /health endpoint returns a 200 OK status code,
    validating basic service availability.
    """
    # Assuming the client fixture is configured to hit the app's base URL
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == "OK"

def test_metrics_endpoint_is_accessible(client):
    """
    Tests that the /metrics endpoint is accessible and returns Prometheus format data.
    """
    response = client.get('/metrics')
    assert response.status_code == 200
    # Check for a known metric prefix to confirm Prometheus format
    assert "http_requests_total" in response.data
