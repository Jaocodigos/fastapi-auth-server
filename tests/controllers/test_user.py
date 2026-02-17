import uuid


def test_list_users_returns_list(client):
    response = client.get("/api/users")

    assert response.status_code == 200

    payload = response.json()
    assert "users" in payload
    assert isinstance(payload["users"], list)


def test_create_user_returns_created_user(client):
    username = f"test-user-{uuid.uuid4().hex}"
    payload = {"username": username, "password": "test-password"}

    response = client.post("/api/users", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["username"] == username
    assert "id" in data


def test_delete_user_returns_success(client):
    username = f"test-user-delete-{uuid.uuid4().hex}"
    created = client.post("/api/users", json={"username": username, "password": "test-password"})

    assert created.status_code == 201

    user_id = created.json()["id"]
    response = client.delete(f"/api/users/{user_id}")

    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "success"
    assert "message" in payload


def test_create_user_duplicate_returns_409(client):
    username = f"test-user-dup-{uuid.uuid4().hex}"
    client.post("/api/users", json={"username": username, "password": "test-password"})

    response = client.post("/api/users", json={"username": username, "password": "test-password"})

    assert response.status_code == 409
