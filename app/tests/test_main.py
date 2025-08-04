from fastapi.testclient import TestClient


def test_client(client):
    assert isinstance(client, TestClient)
