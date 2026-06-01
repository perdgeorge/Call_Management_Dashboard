import pytest
from fastapi.testclient import TestClient
from .factories import make_call_payload


@pytest.mark.anyio
def test_create_call(client: TestClient):
    payload = make_call_payload()
    payload_json = payload.model_dump(mode="json")
    resp = client.post("/calls", json=payload_json)
    assert resp.status_code == 201
    data = resp.json()
    assert data["direction"] == payload.direction
    assert data["from_number"] == payload.from_number
    assert data["to_number"] == payload.to_number
    assert data["call_type"] == payload.call_type
    assert data["duration"] == payload.duration
    assert data["is_archived"] == payload.is_archived
    assert "id" in data
    assert "created_at" in data
    if payload.notes:
        assert data["notes"] == [note.model_dump(mode="json") for note in payload.notes]
