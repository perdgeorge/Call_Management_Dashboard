import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_calls():
    response = client.get("/calls")
    assert response.status_code == 200
    assert len(response.json()) > 0
