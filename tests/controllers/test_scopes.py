import uuid


def test_list_scopes_returns_list(client):
    response = client.get("/api/scopes")

    assert response.status_code == 200

    payload = response.json()
    assert "scopes" in payload
    assert isinstance(payload["scopes"], list)


def test_create_scope_returns_created_scope(client):
    scope_name = f"test-scope-{uuid.uuid4().hex}"

    response = client.post("/api/scopes", json={"name": scope_name})

    assert response.status_code == 201

    payload = response.json()
    assert payload["name"] == scope_name
    assert "id" in payload


def test_delete_scope_returns_success(client):
    scope_name = f"test-scope-delete-{uuid.uuid4().hex}"
    created = client.post("/api/scopes", json={"name": scope_name})

    assert created.status_code == 201

    scope_id = created.json()["id"]
    response = client.delete(f"/api/scopes/{scope_id}")

    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "success"
    assert "message" in payload


def test_create_scope_duplicate_returns_409(client):
    scope_name = f"test-scope-dup-{uuid.uuid4().hex}"
    client.post("/api/scopes", json={"name": scope_name})

    response = client.post("/api/scopes", json={"name": scope_name})

    assert response.status_code == 409
