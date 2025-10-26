from xmlrpc import client
import pytest
from fastapi import status

from app.tests.test_customer_pass import get_auth_headers, create_pass_template

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



def test_claim_rewards(client):
    headers = get_auth_headers(client)
    
    # Create a customer
    customer_resp = client.post(
        "/api/v1/customers",
        json={
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com",
            "phone": "1111111111",
            "birth_date": "1990-01-01"
        },
        headers=headers,
    )
    if customer_resp.status_code != status.HTTP_201_CREATED:
        print(f"Customer creation failed: {customer_resp.status_code}")
        print(f"Response: {customer_resp.text}")
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
        "active_stamps": 3,
        "active_rewards": 2,
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
    assert data["active_stamps"] == 3
    assert data["active_rewards"] == 2
    customer_pass_id = data["id"]    
 
    
    # Additional verification: check that customer pass can be retrieved
    retrieve_response = client.get(
        f"/api/v1/customer-passes/{customer_pass_id}",
        headers=headers,
    )
    assert retrieve_response.status_code == status.HTTP_200_OK
    retrieved_data = retrieve_response.json()
    assert retrieved_data["id"] == customer_pass_id
    assert retrieved_data["active_stamps"] == 3
    assert retrieved_data["active_rewards"] == 2
    
	# --- Check customer pass state before claiming ---
    get_pass_response = client.get(f"/api/v1/customer-passes/{customer_pass_id}", headers=headers)
    assert get_pass_response.status_code == status.HTTP_200_OK
    customer_pass_before = get_pass_response.json()
    active_rewards = customer_pass_before["active_rewards"]

    # --- Claim reward ---
    number_of_rewards_to_claim = 2
    claim_response = client.get(
        f"/api/v1/rewards/claim-reward/{customer_pass_id}",
        params={"number_of_rewards": number_of_rewards_to_claim},
        headers=headers,
    )
    assert claim_response.status_code == status.HTTP_200_OK
    customer_pass_after = claim_response.json()
    assert customer_pass_after["active_rewards"] == active_rewards - number_of_rewards_to_claim
    


    # --- Check customer pass state after claiming ---
    get_pass_after_response = client.get(f"/api/v1/customer-passes/{customer_pass_id}", headers=headers)
    assert get_pass_after_response.status_code == status.HTTP_200_OK
    customer_pass_final = get_pass_after_response.json()
    assert customer_pass_final["active_rewards"] == active_rewards - number_of_rewards_to_claim



