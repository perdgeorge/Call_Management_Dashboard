import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_all_calls():
    response = client.get("/calls")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_call_by_id():
    response = client.get("/calls/2")
    assert response.status_code == 200
    assert response.json()
