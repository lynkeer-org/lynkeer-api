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

def create_pass_type(client, headers):
    response = client.post(
        "/api/v1/types-passes",
        json={"type": "Test Pass Type"},
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]

def create_pass_template(client, headers):
    pass_type_id = create_pass_type(client, headers)
    sample_pass_field = {
        "key": "field_key",
        "label": "Field Label", 
        "value": "Field Value",
        "field_type": "text"
    }
    response = client.post(
        "/api/v1/pass-template",
        json={
            "title": "Test Pass",
            "stamp_goal": 5,
            "logo_url": "https://example.com/logo.png",
            "text_color": "#000000",
            "background_color": "#ffffff",
            "google_class_id": "test_google_class",
            "apple_pass_type_identifier": "test_apple_id",
            "pass_type_id": pass_type_id,
            "pass_fields": [sample_pass_field],
        },
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]

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

def test_get_customer_by_email_with_apikey(client):
    """Test retrieving customer with API key (unrestricted access)"""
    # Create customer with Bearer token
    headers = get_auth_headers(client)
    customer_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "phone": "12345678",
        "birth_date": "1990-01-01"
    }
    customer_response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=headers
    )
    assert customer_response.status_code == status.HTTP_201_CREATED

    # Test: Get customer by email with API key (should work regardless of owner)
    api_key = os.environ["API_KEY"]
    api_key_headers = {"Authorization": f"API-KEY {api_key}"}
    response = client.get(
        f"/api/v1/customers/by-email/alice@example.com",
        headers=api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["email"] == "alice@example.com"

def test_get_customer_by_email_with_bearer_no_passes(client):
    """Test retrieving customer with Bearer token when customer has no passes"""
    # Create customer with Bearer token
    headers = get_auth_headers(client)
    customer_data = {
        "first_name": "Bob",
        "last_name": "Brown",
        "email": "bob@example.com",
        "phone": "87654321",
        "birth_date": "1985-05-05"
    }
    customer_response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=headers
    )
    assert customer_response.status_code == status.HTTP_201_CREATED

    # Test: Get customer by email with Bearer token (should fail - no passes)
    response = client.get(
        f"/api/v1/customers/by-email/bob@example.com",
        headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_customer_by_email_with_bearer_with_passes(client):
    """Test retrieving customer with Bearer token when customer has passes from that owner"""
    # Create customer and pass template setup
    headers = get_auth_headers(client)
    
    # Create customer
    customer_data = {
        "first_name": "Charlie",
        "last_name": "Green",
        "email": "charlie@example.com",
        "phone": "11223344",
        "birth_date": "1992-03-15"
    }
    customer_response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=headers
    )
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_id = customer_response.json()["id"]

    # Create pass template
    pass_template_id = create_pass_template(client, headers)

    # Create customer pass relationship
    customer_pass_data = {
        "device": "ios",
        "registration_method": "qr",
        "customer_id": customer_id,
        "pass_id": pass_template_id,
    }
    customer_pass_response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers
    )
    assert customer_pass_response.status_code == status.HTTP_201_CREATED

    # Test: Get customer by email with Bearer token (should work - has passes from this owner)
    response = client.get(
        f"/api/v1/customers/by-email/charlie@example.com",
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["email"] == "charlie@example.com"