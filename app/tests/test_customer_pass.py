from fastapi import status
import os

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

def test_create_customer_pass(client):
    headers = get_auth_headers(client)
    customer_pass_data = {
        "device": "iPhone",
        "registration_method": "app",
        "customer_id": 1,  # Replace with actual customer ID
        "pass_id": 1,      # Replace with actual pass ID
    }
    response = client.post(
        "/api/v1/customer-pass",
        json=customer_pass_data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["device"] == "iPhone"
    assert data["registration_method"] == "app"

def test_get_customer_pass(client):
    headers = get_auth_headers(client)
    # Create a customer pass
    customer_pass_data = {
        "device": "iPhone",
        "registration_method": "app",
        "customer_id": 1,  # Replace with actual customer ID
        "pass_id": 1,      # Replace with actual pass ID
    }
    client.post(
        "/api/v1/customer-pass",
        json=customer_pass_data,
        headers=headers,
    )

    # Retrieve the customer pass
    response = client.get(
        "/api/v1/customer-pass/1",  # Replace with actual customer pass ID
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["device"] == "iPhone"
    assert data["registration_method"] == "app"

def test_create_customer_pass_with_bearer(client):
    headers = get_auth_headers(client)
    customer_pass_data = {
        "device": "iPhone",
        "registration_method": "app",
        "customer_id": 1,  # Replace with actual customer ID
        "pass_id": 1,      # Replace with actual pass ID
    }
    response = client.post(
        "/api/v1/customer-pass",
        json=customer_pass_data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["device"] == "iPhone"
    assert data["registration_method"] == "app"

def test_create_customer_pass_with_apikey(client):
    api_key = os.environ["API_KEY"]
    api_key_headers = {"Authorization": f"API-KEY {api_key}"}
    customer_pass_data = {
        "device": "Android",
        "registration_method": "web",
        "customer_id": 2,  # Replace with actual customer ID
        "pass_id": 2,      # Replace with actual pass ID
    }
    response = client.post(
        "/api/v1/customer-pass",
        json=customer_pass_data,
        headers=api_key_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["device"] == "Android"
    assert data["registration_method"] == "web"
