import os
import pytest
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
        json={"type": "TestType"},
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]

def create_pass_template(client):
    headers = get_auth_headers(client)
    pass_type_id = create_pass_type(client, headers)
    # Sample pass field object, adjust keys as needed for your schema
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
            "pass_fields": [sample_pass_field],  # <-- Correct field name and sample object
        },
        headers=headers,
    )
    print(response.json())  # For debugging if it fails
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Test Pass"


def test_create_customer_pass(client):
    headers = get_auth_headers(client)
    
    # Create a customer
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "birth_date": "1990-01-01"
        },
        headers=headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create a pass template using the existing function
    create_pass_template(client)
    
    # Get the created pass template ID by listing pass templates
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create customer pass
    customer_pass_data = {
        "device": "ios",
        "registration_method": "qr",
        "customer_id": customer_id,
        "pass_id": pass_id,
    }
    response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["device"] == "ios"
    assert data["registration_method"] == "qr"
    assert data["customer_id"] == customer_id
    assert data["pass_id"] == pass_id


def test_create_customer_pass_with_bearer_token(client):
    """Test customer pass creation specifically with Bearer token authentication"""
    headers = get_auth_headers(client)  # This returns Bearer token headers
    
    # Create a customer
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Bearer",
            "last_name": "User",
            "email": "bearer.user@example.com",
            "phone": "1234567899",
            "birth_date": "1992-06-15"
        },
        headers=headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create a pass template using the existing function
    create_pass_template(client)
    
    # Get the created pass template ID by listing pass templates
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create customer pass with Bearer token
    customer_pass_data = {
        "device": "android",
        "registration_method": "manual",
        "customer_id": customer_id,
        "pass_id": pass_id,
    }
    response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["device"] == "android"
    assert data["registration_method"] == "manual"
    assert data["customer_id"] == customer_id
    assert data["pass_id"] == pass_id
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Bearer ")


def test_create_customer_pass_with_api_key(client):
    """Test customer pass creation specifically with API key authentication"""
    # Setup: Create owner and pass template with Bearer token first
    bearer_headers = get_auth_headers(client)
    create_pass_template(client)
    
    # Get the pass template ID
    pass_list_resp = client.get("/api/v1/pass-template", headers=bearer_headers)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create a customer using API key authentication
    api_key = os.environ["API_KEY"]
    api_key_headers = {"Authorization": f"API-KEY {api_key}"}
    
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "ApiKey",
            "last_name": "User",
            "email": "apikey.user@example.com",
            "phone": "1234567898",
            "birth_date": "1988-09-20"
        },
        headers=api_key_headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create customer pass with API key authentication
    customer_pass_data = {
        "device": "web",
        "registration_method": "link",
        "customer_id": customer_id,
        "pass_id": pass_id,
    }
    response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=api_key_headers,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["device"] == "web"
    assert data["registration_method"] == "link"
    assert data["customer_id"] == customer_id
    assert data["pass_id"] == pass_id
    assert "Authorization" in api_key_headers
    assert api_key_headers["Authorization"].startswith("API-KEY ")


def test_create_customer_pass_forbidden_for_other_owner(client):
    """Test that Bearer token cannot create customer pass for another owner's pass template"""
    # Setup: Create first owner and their pass template
    headers_owner1 = get_auth_headers(client)  # First owner (Andres)
    create_pass_template(client)
    
    # Get the first owner's pass template ID
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers_owner1)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id_owner1 = pass_templates[0]["id"]
    
    # Create second owner with different credentials
    client.post(
        "/api/v1/sign-up",
        json={
            "first_name": "Maria",
            "last_name": "Rodriguez", 
            "email": "maria@example.com",
            "phone": "9876543210",
            "password": "anotherpassword",
        },
    )
    
    # Login second owner
    login_resp = client.post(
        "/api/v1/sign-in",
        json={
            "email": "maria@example.com",
            "password": "anotherpassword",
        },
    )
    token_owner2 = login_resp.json().get("token")
    headers_owner2 = {"Authorization": f"Bearer {token_owner2}"}
    
    # Create customer with second owner
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Test",
            "last_name": "Customer", 
            "email": "test@example.com",
            "phone": "1111111111",
            "birth_date": "1990-01-01"
        },
        headers=headers_owner2,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Try to create customer pass for first owner's pass template using second owner's Bearer token
    # This should fail with 403 Forbidden
    customer_pass_data = {
        "device": "android",
        "registration_method": "qr",
        "customer_id": customer_id,
        "pass_id": pass_id_owner1,  # First owner's pass template
    }
    response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers_owner2,  # Second owner's Bearer token
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "You can only create customer passes for your own pass templates" in response.json()["detail"]


def test_list_customer_passes(client):
    headers = get_auth_headers(client)
    
    # Create a customer
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com", 
            "phone": "1234567891",
            "birth_date": "1985-05-15"
        },
        headers=headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create a pass template
    create_pass_template(client)
    
    # Get the pass template ID
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create multiple customer passes
    customer_pass_1 = {
        "device": "ios",
        "registration_method": "qr",
        "customer_id": customer_id,
        "pass_id": pass_id,
    }
    
    response1 = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_1,
        headers=headers,
    )
    assert response1.status_code == status.HTTP_201_CREATED
    
    # List all customer passes
    list_response = client.get("/api/v1/customer-passes", headers=headers)
    assert list_response.status_code == status.HTTP_200_OK
    
    customer_passes = list_response.json()
    assert isinstance(customer_passes, list)
    assert len(customer_passes) >= 1
    
    # Verify the customer pass data
    found_pass = None
    for cp in customer_passes:
        if cp["customer_id"] == customer_id and cp["pass_id"] == pass_id:
            found_pass = cp
            break
    
    assert found_pass is not None
    assert found_pass["device"] == "ios"
    assert found_pass["registration_method"] == "qr"


def test_read_customer_pass(client):
    headers = get_auth_headers(client)
    
    # Create a customer
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob.johnson@example.com",
            "phone": "1234567892", 
            "birth_date": "1992-08-20"
        },
        headers=headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create a pass template
    create_pass_template(client)
    
    # Get the pass template ID
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create customer pass
    customer_pass_data = {
        "device": "android",
        "registration_method": "manual",
        "customer_id": customer_id,
        "pass_id": pass_id,
    }
    
    create_response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers,
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    created_pass = create_response.json()
    customer_pass_id = created_pass["id"]
    
    # Read the specific customer pass
    read_response = client.get(
        f"/api/v1/customer-passes/{customer_pass_id}",
        headers=headers,
    )
    assert read_response.status_code == status.HTTP_200_OK
    
    read_pass = read_response.json()
    assert read_pass["id"] == customer_pass_id
    assert read_pass["device"] == "android"
    assert read_pass["registration_method"] == "manual"
    assert read_pass["customer_id"] == customer_id
    assert read_pass["pass_id"] == pass_id
    assert read_pass["active"] == True


def test_update_customer_pass(client):
    headers = get_auth_headers(client)
    
    # Create a customer
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Alice",
            "last_name": "Williams", 
            "email": "alice.williams@example.com",
            "phone": "1234567893",
            "birth_date": "1988-12-10"
        },
        headers=headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create a pass template
    create_pass_template(client)
    
    # Get the pass template ID
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create customer pass
    customer_pass_data = {
        "device": "ios",
        "registration_method": "qr",
        "customer_id": customer_id,
        "pass_id": pass_id,
    }
    
    create_response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers,
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    created_pass = create_response.json()
    customer_pass_id = created_pass["id"]
    
    # Update the customer pass
    update_data = {
        "device": "web",
        "registration_method": "link",
        "apple_serial_number": "ABC123",
        "google_id_class": "updated_google_class"
    }
    
    update_response = client.patch(
        f"/api/v1/customer-passes/{customer_pass_id}",
        json=update_data,
        headers=headers,
    )
    assert update_response.status_code == status.HTTP_200_OK
    
    updated_pass = update_response.json()
    assert updated_pass["id"] == customer_pass_id
    assert updated_pass["device"] == "web"
    assert updated_pass["registration_method"] == "link"
    assert updated_pass["apple_serial_number"] == "ABC123"
    assert updated_pass["google_id_class"] == "updated_google_class"
    assert updated_pass["customer_id"] == customer_id  # Should remain unchanged
    assert updated_pass["pass_id"] == pass_id  # Should remain unchanged


def test_update_customer_pass_forbidden_for_other_owner(client):
    """Test that an owner cannot update customer passes for another owner's pass template"""
    # Setup: Create first owner and their customer pass
    headers_owner1 = get_auth_headers(client)  # First owner (Andres)
    
    # Create customer with first owner
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Test",
            "last_name": "Customer",
            "email": "test@example.com", 
            "phone": "1111111111",
            "birth_date": "1990-01-01"
        },
        headers=headers_owner1,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create pass template with first owner
    create_pass_template(client)
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers_owner1)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create customer pass with first owner
    customer_pass_data = {
        "device": "ios",
        "registration_method": "qr",
        "customer_id": customer_id,
        "pass_id": pass_id,
    }
    create_response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers_owner1,
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    customer_pass_id = create_response.json()["id"]
    
    # Create second owner with different credentials
    client.post(
        "/api/v1/sign-up",
        json={
            "first_name": "Maria",
            "last_name": "Rodriguez",
            "email": "maria@example.com", 
            "phone": "9876543210",
            "password": "anotherpassword",
        },
    )
    
    # Login second owner
    login_resp = client.post(
        "/api/v1/sign-in",
        json={
            "email": "maria@example.com",
            "password": "anotherpassword",
        },
    )
    token_owner2 = login_resp.json().get("token")
    headers_owner2 = {"Authorization": f"Bearer {token_owner2}"}
    
    # Try to update first owner's customer pass using second owner's Bearer token
    # This should fail with 403 Forbidden
    update_data = {
        "device": "android",
        "registration_method": "manual",
    }
    response = client.patch(
        f"/api/v1/customer-passes/{customer_pass_id}",
        json=update_data,
        headers=headers_owner2,  # Second owner's Bearer token
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "You can only update customer passes for your own pass templates" in response.json()["detail"]


def test_delete_customer_pass(client):
    headers = get_auth_headers(client)
    
    # Create a customer  
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "charlie.brown@example.com",
            "phone": "1234567894",
            "birth_date": "1995-03-25"
        },
        headers=headers,
    )
    assert customer_resp.status_code == status.HTTP_201_CREATED
    customer_id = customer_resp.json()["id"]
    
    # Create a pass template
    create_pass_template(client)
    
    # Get the pass template ID
    pass_list_resp = client.get("/api/v1/pass-template", headers=headers)
    assert pass_list_resp.status_code == status.HTTP_200_OK
    pass_templates = pass_list_resp.json()
    assert len(pass_templates) > 0
    pass_id = pass_templates[0]["id"]
    
    # Create customer pass
    customer_pass_data = {
        "device": "android",
        "registration_method": "manual",
        "customer_id": customer_id,
        "pass_id": pass_id,
    }
    
    create_response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers,
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    created_pass = create_response.json()
    customer_pass_id = created_pass["id"]
    
    # Delete the customer pass
    delete_response = client.delete(
        f"/api/v1/customer-passes/{customer_pass_id}",
        headers=headers,
    )
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify the customer pass is soft-deleted (should still exist but be inactive)
    read_response = client.get(
        f"/api/v1/customer-passes/{customer_pass_id}",
        headers=headers,
    )
    assert read_response.status_code == status.HTTP_200_OK
    deleted_pass = read_response.json()
    assert deleted_pass["active"] == False  # Should be marked as inactive


def test_read_nonexistent_customer_pass(client):
    headers = get_auth_headers(client)
    
    # Try to read a nonexistent customer pass
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(
        f"/api/v1/customer-passes/{fake_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_customer_pass(client):
    headers = get_auth_headers(client)
    
    # Try to update a nonexistent customer pass
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    update_data = {"device": "web"}
    
    response = client.patch(
        f"/api/v1/customer-passes/{fake_uuid}",
        json=update_data,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_customer_pass(client):
    headers = get_auth_headers(client)
    
    # Try to delete a nonexistent customer pass
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    
    response = client.delete(
        f"/api/v1/customer-passes/{fake_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    