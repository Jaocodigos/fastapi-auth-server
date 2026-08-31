from tests.utils import admin_headers, create_client, make_client_payload

def test_list_clients_requires_admin_header(client):
    response = client.get("/api/clients")

    assert response.status_code == 401


def test_list_clients_rejects_invalid_admin_token(client):
    response = client.get("/api/clients", headers=admin_headers(False))

    assert response.status_code == 403


def test_list_clients_returns_payload(client):
    response = client.get("/api/clients", headers=admin_headers())

    assert response.status_code == 200

    payload = response.json()
    assert "clients" in payload
    assert isinstance(payload["clients"], list)


def test_create_client_returns_created_client(client):
    _, payload = create_client(client, redirect_uri="https://example.com/callback/test")

    assert "client_id" in payload
    assert "client_secret" in payload
    assert payload["redirect_uri"].startswith("https://example.com/callback/")


def test_create_client_rejects_invalid_grant_type(client):
    payload = make_client_payload(
        redirect_uri="https://example.com/callback/invalid-grant",
        grant_types=["invalid_grant_type"],
    )

    response = client.post("/api/clients", json=payload, headers=admin_headers())

    assert response.status_code == 400

    payload = response.json()
    assert payload["message"] == "Invalid grant type"


def test_create_client_rejects_unknown_scope(client):
    payload = make_client_payload(
        redirect_uri="https://example.com/callback/invalid-scope",
        grant_types=["authorization_code"],
    )
    payload["scopes"] = ["does-not-exist"]

    response = client.post("/api/clients", json=payload, headers=admin_headers())

    assert response.status_code == 404


def test_delete_client_returns_success(client):
    _, created = create_client(client, redirect_uri="https://example.com/callback/delete")
    client_id = created["client_id"]
    response = client.delete(f"/api/clients/{client_id}", headers=admin_headers())

    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "success"
    assert "message" in payload
