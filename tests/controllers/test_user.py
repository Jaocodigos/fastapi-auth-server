import uuid

from tests.utils import admin_headers, create_client, create_user


def test_list_users_returns_list(client):
    _, client_response = create_client(client, redirect_uri=f"https://example.com/callback/{uuid.uuid4().hex}")
    client_name = client_response["name"]

    response = client.get(f"/api/{client_name}/users", headers=admin_headers())

    assert response.status_code == 200

    payload = response.json()
    assert "users" in payload
    assert isinstance(payload["users"], list)


def test_create_user_returns_created_user(client):
    _, client_response = create_client(client, redirect_uri=f"https://example.com/callback/{uuid.uuid4().hex}")
    client_name = client_response["name"]
    username = f"test-user-{uuid.uuid4().hex}"

    response = client.post(
        f"/api/{client_name}/users",
        json={"username": username, "password": "test-password"},
        headers=admin_headers()
    )

    assert response.status_code == 201

    data = response.json()
    assert data["username"] == username
    assert "id" in data


def test_delete_user_returns_success(client):
    _, client_response = create_client(client, redirect_uri=f"https://example.com/callback/{uuid.uuid4().hex}")
    client_name = client_response["name"]
    username, _, _ = create_user(client, client_name)

    response = client.delete(f"/api/{client_name}/users/{username}", headers=admin_headers())

    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "success"
    assert "message" in payload


def test_create_user_duplicate_returns_409(client):
    _, client_response = create_client(client, redirect_uri=f"https://example.com/callback/{uuid.uuid4().hex}")
    client_name = client_response["name"]
    username = f"test-user-dup-{uuid.uuid4().hex}"

    client.post(f"/api/{client_name}/users", json={"username": username, "password": "test-password"}, headers=admin_headers())
    response = client.post(f"/api/{client_name}/users", json={"username": username, "password": "test-password"}, headers=admin_headers())

    assert response.status_code == 409
