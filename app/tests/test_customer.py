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

def test_update_customer_with_bearer_with_passes(client):
    """Test successfully updating customer with Bearer token when customer has passes from that owner"""
    # Create customer and pass template setup
    headers = get_auth_headers(client)
    
    # Create customer
    customer_data = {
        "first_name": "David",
        "last_name": "Wilson", 
        "email": "david@example.com",
        "phone": "55566677",
        "birth_date": "1988-07-20"
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

    # Test: Update customer with Bearer token (should work - has passes from this owner)
    update_data = {
        "first_name": "David Updated",
        "last_name": "Wilson Updated",
        "email": "david.updated@example.com",
        "phone": "99988877",
        "birth_date": "1988-07-21"
    }
    response = client.patch(
        f"/api/v1/customers/{customer_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["first_name"] == "David Updated"
    assert response_data["last_name"] == "Wilson Updated"
    assert response_data["email"] == "david.updated@example.com"
    assert response_data["phone"] == "99988877"
    assert response_data["id"] == customer_id

def test_update_customer_forbidden_no_passes(client):
    """Test updating customer with Bearer token when customer has no passes from that owner"""
    # Create customer with Bearer token
    headers = get_auth_headers(client)
    customer_data = {
        "first_name": "Emma",
        "last_name": "Davis",
        "email": "emma@example.com", 
        "phone": "44455566",
        "birth_date": "1991-03-10"
    }
    customer_response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=headers
    )
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_id = customer_response.json()["id"]

    # Test: Update customer with Bearer token (should fail - no passes from this owner)
    update_data = {
        "first_name": "Emma Updated",
        "last_name": "Davis Updated",
        "email": "emma.updated@example.com",
        "phone": "77788899",
        "birth_date": "1991-03-11"
    }
    response = client.patch(
        f"/api/v1/customers/{customer_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "You can only update customers who have passes from your pass templates" in response.json()["detail"]

def test_update_customer_forbidden_other_owner(client):
    """Test that an owner cannot update customers that belong to another owner's pass templates"""
    # Setup: Create first owner and their customer with passes
    headers_owner1 = get_auth_headers(client)  # First owner (Andres)
    
    # Create customer with first owner
    customer_data = {
        "first_name": "Frank",
        "last_name": "Miller",
        "email": "frank@example.com",
        "phone": "11122233", 
        "birth_date": "1987-11-15"
    }
    customer_response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=headers_owner1
    )
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_id = customer_response.json()["id"]

    # Create pass template and customer pass with first owner
    pass_template_id = create_pass_template(client, headers_owner1)
    customer_pass_data = {
        "device": "android",
        "registration_method": "manual",
        "customer_id": customer_id,
        "pass_id": pass_template_id,
    }
    customer_pass_response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers_owner1
    )
    assert customer_pass_response.status_code == status.HTTP_201_CREATED

    # Create second owner with different credentials
    client.post(
        "/api/v1/sign-up",
        json={
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah@example.com",
            "phone": "5555444433", 
            "password": "differentpassword",
        },
    )
    
    # Login second owner
    login_resp = client.post(
        "/api/v1/sign-in", 
        json={
            "email": "sarah@example.com",
            "password": "differentpassword",
        },
    )
    token_owner2 = login_resp.json().get("token")
    headers_owner2 = {"Authorization": f"Bearer {token_owner2}"}

    # Test: Try to update first owner's customer using second owner's Bearer token
    # This should fail with 403 Forbidden
    update_data = {
        "first_name": "Frank Hacked",
        "last_name": "Miller Hacked", 
        "email": "frank.hacked@example.com",
        "phone": "99999999",
        "birth_date": "1987-11-16"
    }
    response = client.patch(
        f"/api/v1/customers/{customer_id}",
        json=update_data,
        headers=headers_owner2  # Second owner's Bearer token
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "You can only update customers who have passes from your pass templates" in response.json()["detail"]


def test_delete_customer_with_bearer_with_passes(client):
    """Test successfully deleting customer with Bearer token when customer has passes from that owner"""
    # Create customer and pass template setup
    headers = get_auth_headers(client)
    
    # Create customer
    customer_data = {
        "first_name": "Grace",
        "last_name": "Taylor", 
        "email": "grace@example.com",
        "phone": "66677788",
        "birth_date": "1990-04-25"
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

    # Test: Delete customer with Bearer token (should work - has passes from this owner)
    response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify customer was actually deleted by trying to get it by email
    get_response = client.get(
        f"/api/v1/customers/by-email/{customer_data['email']}",
        headers=headers
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_customer_forbidden_no_passes(client):
    """Test deleting customer with Bearer token when customer has no passes from that owner"""
    # Create customer with Bearer token
    headers = get_auth_headers(client)
    customer_data = {
        "first_name": "Henry",
        "last_name": "Brown",
        "email": "henry@example.com", 
        "phone": "77788899",
        "birth_date": "1993-06-12"
    }
    customer_response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=headers
    )
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_id = customer_response.json()["id"]

    # Test: Delete customer with Bearer token (should fail - no passes from this owner)
    response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "You can only delete customers who have passes from your pass templates" in response.json()["detail"]


def test_delete_customer_forbidden_other_owner(client):
    """Test that an owner cannot delete customers that belong to another owner's pass templates"""
    # Setup: Create first owner and their customer with passes
    headers_owner1 = get_auth_headers(client)  # First owner (Andres)
    
    # Create customer with first owner
    customer_data = {
        "first_name": "Iris",
        "last_name": "Wilson",
        "email": "iris@example.com",
        "phone": "88899900", 
        "birth_date": "1985-09-03"
    }
    customer_response = client.post(
        "/api/v1/customers",
        json=customer_data,
        headers=headers_owner1
    )
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_id = customer_response.json()["id"]

    # Create pass template and customer pass with first owner
    pass_template_id = create_pass_template(client, headers_owner1)
    customer_pass_data = {
        "device": "android",
        "registration_method": "manual",
        "customer_id": customer_id,
        "pass_id": pass_template_id,
    }
    customer_pass_response = client.post(
        "/api/v1/customer-passes",
        json=customer_pass_data,
        headers=headers_owner1
    )
    assert customer_pass_response.status_code == status.HTTP_201_CREATED

    # Create second owner with different credentials
    client.post(
        "/api/v1/sign-up",
        json={
            "first_name": "Jack",
            "last_name": "Davis",
            "email": "jack@example.com",
            "phone": "2223334444", 
            "password": "anothersecurepassword",
        },
    )
    
    # Login second owner
    login_resp = client.post(
        "/api/v1/sign-in", 
        json={
            "email": "jack@example.com",
            "password": "anothersecurepassword",
        },
    )
    token_owner2 = login_resp.json().get("token")
    headers_owner2 = {"Authorization": f"Bearer {token_owner2}"}

    # Test: Try to delete first owner's customer using second owner's Bearer token
    # This should fail with 403 Forbidden
    response = client.delete(
        f"/api/v1/customers/{customer_id}",
        headers=headers_owner2  # Second owner's Bearer token
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "You can only delete customers who have passes from your pass templates" in response.json()["detail"]