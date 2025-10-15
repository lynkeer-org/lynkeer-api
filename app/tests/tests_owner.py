from fastapi import status


def test_create_owner(client):
    response = client.post(
        "/api/v1/sign-up",
        json={
            "first_name": "Andres",
            "last_name": "Gonzalez",
            "email": "andres@example.com",
            "phone": "1234567890",
            "password": "securepassword",
        },
    )
    
    # Print response details for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    
    assert response.status_code == status.HTTP_201_CREATED


def test_login_owner(client):
    test_create_owner(client)
    response = client.post(
        "/api/v1/sign-in",
        json={
            "email": "andres@example.com",
            "password": "securepassword",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json().get("token")
    assert token is not None
    return token
