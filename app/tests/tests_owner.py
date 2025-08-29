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
    assert response.status_code == status.HTTP_201_CREATED
