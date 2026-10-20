#!/usr/bin/env python3
"""Unit tests for GEFE Main Application"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


def test_health_check(client):
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "GEFE" in data["service"]


def test_openapi_docs(client):
    """Test OpenAPI documentation"""
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_api_version(client):
    """Test API version information"""
    response = client.get("/openapi.json")
    data = response.json()
    assert data["info"]["version"] == "1.0.0"
    assert "Global Economic Forecast Engine" in data["info"]["title"]
