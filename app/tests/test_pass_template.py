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

def test_create_pass_template(client):
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

def test_update_pass_template(client):
    headers = get_auth_headers(client)
    pass_type_id = create_pass_type(client, headers)

    # 1) Create a pass template with one field
    create_resp = client.post(
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
            "pass_fields": [
                {"key": "field_key", "label": "Field Label", "value": "Field Value", "field_type": "text"}
            ],
        },
        headers=headers,
    )
    assert create_resp.status_code == status.HTTP_201_CREATED
    created = create_resp.json()
    pass_id = created["id"]
    field_id = created["pass_fields"][0]["id"]
    prev_updated_at = created["updated_at"]

    # 2) Patch: update title/stamp_goal and mutate the existing field
    patch_payload = {
        "title": "Updated Pass",
        "stamp_goal": 10,
        "logo_url": "https://example.com/logo.png",
        "text_color": "#000000",
        "background_color": "#ffffff",
        "google_class_id": "test_google_class",
        "apple_pass_type_identifier": "test_apple_id",
        "pass_fields": [
            {
                "id": field_id,                    # must send the id to update this field
                "key": "field_key",
                "label": "Updated Label",
                "value": "New Value",
                "field_type": "text",
            }
        ],
    }
    patch_resp = client.patch(f"/api/v1/pass-template/{pass_id}", json=patch_payload, headers=headers)
    assert patch_resp.status_code == status.HTTP_200_OK

    updated = patch_resp.json()
    assert updated["id"] == pass_id
    assert updated["title"] == "Updated Pass"
    assert updated["stamp_goal"] == 10

    # Field was updated in-place (same id) with new values
    assert len(updated["pass_fields"]) == 1
    uf = updated["pass_fields"][0]
    assert uf["id"] == field_id
    assert uf["label"] == "Updated Label"
    assert uf["value"] == "New Value"

    # updated_at should have changed on successful update
    assert updated["updated_at"] != prev_updated_at

def test_list_passes_template(client):
    headers = get_auth_headers(client)
    pass_type_id = create_pass_type(client, headers)

    # Create 2 pass templates (each with 1 field)
    def mk(title):
        r = client.post(
            "/api/v1/pass-template",
            json={
                "title": title,
                "stamp_goal": 5,
                "logo_url": "https://example.com/logo.png",
                "text_color": "#000000",
                "background_color": "#ffffff",
                "google_class_id": "test_google_class",
                "apple_pass_type_identifier": "test_apple_id",
                "pass_type_id": pass_type_id,
                "pass_fields": [
                    {"key": "k", "label": f"{title} Label", "value": "V", "field_type": "text"}
                ],
            },
            headers=headers,
        )
        assert r.status_code == status.HTTP_201_CREATED
        return r.json()

    p1 = mk("Pass A")
    p2 = mk("Pass B")

    # List
    resp = client.get("/api/v1/pass-template", headers=headers)
    assert resp.status_code == status.HTTP_200_OK

    items = resp.json()
    assert isinstance(items, list)
    # Expect exactly the two we created for this owner
    assert len(items) == 2

    # Normalize order by title for stable assertions
    items.sort(key=lambda x: x["title"])
    expected = sorted([p1["id"], p2["id"]])

    got_ids = sorted([items[0]["id"], items[1]["id"]])
    assert got_ids == expected

    # Each item should include its fields
    for item in items:
        assert "pass_fields" in item
        assert isinstance(item["pass_fields"], list)
        assert len(item["pass_fields"]) == 1
        f = item["pass_fields"][0]
        assert {"id", "key", "label", "value", "field_type"} <= set(f.keys())
 
def test_delete_pass(client):
    headers = get_auth_headers(client)
    pass_type_id = create_pass_type(client, headers)

    # Create a pass template with one field
    create_resp = client.post(
        "/api/v1/pass-template",
        json={
            "title": "To Delete",
            "stamp_goal": 5,
            "logo_url": "https://example.com/logo.png",
            "text_color": "#000000",
            "background_color": "#ffffff",
            "google_class_id": "test_google_class",
            "apple_pass_type_identifier": "test_apple_id",
            "pass_type_id": pass_type_id,
            "pass_fields": [
                {"key": "k", "label": "L", "value": "V", "field_type": "text"}
            ],
        },
        headers=headers,
    )
    assert create_resp.status_code == status.HTTP_201_CREATED
    pass_id = create_resp.json()["id"]

    # Delete it
    del_resp = client.delete(f"/api/v1/pass-template/{pass_id}", headers=headers)
    assert del_resp.status_code == status.HTTP_200_OK
    assert del_resp.json()["message"] == "Pass template deleted successfully"

    # Verify it's gone (soft-deleted)
    get_resp = client.get(f"/api/v1/pass-template/{pass_id}", headers=headers)
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND

    # Listing should not include it
    list_resp = client.get("/api/v1/pass-template", headers=headers)
    assert list_resp.status_code == status.HTTP_200_OK
    assert list_resp.json() == []

    # Further updates should fail
    patch_resp = client.patch(
        f"/api/v1/pass-template/{pass_id}",
        json={"title": "Should Fail", "stamp_goal": 6,
              "logo_url": "https://example.com/logo.png",
              "text_color": "#000000",
              "background_color": "#ffffff",
              "google_class_id": "test_google_class",
              "apple_pass_type_identifier": "test_apple_id",
              "pass_fields": []},
        headers=headers,
    )
    assert patch_resp.status_code == status.HTTP_404_NOT_FOUND       