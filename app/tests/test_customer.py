import os
from fastapi import status

def get_auth_headers(client):
    # Create owner
    client.post(
        "/api/v1/sign-up",
        json={
            "first_name": "Andres",
            "last_name": "Gonzalez",
            "email": "andres@example.com",
            "phone": "1234567890",
            "password": "securepassword",
        },
    )
    # Login owner
    response = client.post(
        "/api/v1/sign-in",
        json={
            "email": "andres@example.com",
            "password": "securepassword",
        },
    )
    token = response.json().get("token")
    assert token is not None
    return {"Authorization": f"Bearer {token}"}

def test_create_customer_with_bearer(client):
    # Simulate owner authentication
    headers = get_auth_headers(client)
    customer_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "phone": "12345678",
        "birth_date": "1990-01-01"
    }
    response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["first_name"] == "Alice"
    assert data["active"] is True

def test_create_customer_with_apikey(client):
    # Simulate customer authentication with API-KEY
    api_key = os.environ["API_KEY"]
    api_key_headers = {"Authorization": f"API-KEY {api_key}"}
    customer_data = {
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bob@example.com",
        "phone": "87654321",
        "birth_date": "1985-05-05"
    }
    response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=api_key_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "bob@example.com"
    assert data["first_name"] == "Bob"
    assert data["active"] is True