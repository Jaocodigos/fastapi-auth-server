import uuid

from tests.utils import authorize_code, create_client, create_user


def test_token_exchange_authorization_code(client):
    redirect_uri = f"https://example.com/callback/{uuid.uuid4().hex}"
    _, client_response = create_client(
        client,
        redirect_uri=redirect_uri,
        grant_types=["authorization_code", "refresh_token"],
    )
    client_id = client_response["client_id"]
    client_name = client_response["name"]
    username, password, _ = create_user(client, client_name)

    login = client.post(
        f"/{client_name}/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )
    assert login.status_code == 302
    _, code = authorize_code(client, client_id, redirect_uri)

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_verifier": "test-code-verifier",
    }
    response = client.post("/api/token", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data


def test_token_exchange_refresh_token(client):
    redirect_uri = f"https://example.com/callback/{uuid.uuid4().hex}"
    _, client_response = create_client(
        client,
        redirect_uri=redirect_uri,
        grant_types=["authorization_code", "refresh_token"],
    )
    client_id = client_response["client_id"]
    client_name = client_response["name"]
    username, password, _ = create_user(client, client_name)

    login = client.post(
        f"/{client_name}/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )
    assert login.status_code == 302
    _, code = authorize_code(client, client_id, redirect_uri)

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_verifier": "test-code-verifier",
    }
    response = client.post("/api/token", json=payload)
    assert response.status_code == 200

    refresh_token = response.json()["refresh_token"]

    refresh_payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
    }
    refreshed = client.post("/api/token", json=refresh_payload)

    assert refreshed.status_code == 200

    data = refreshed.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data


def test_token_exchange_rejects_invalid_code(client):
    redirect_uri = f"https://example.com/callback/{uuid.uuid4().hex}"
    _, client_response = create_client(client, redirect_uri=redirect_uri)
    client_id = client_response["client_id"]

    payload = {
        "grant_type": "authorization_code",
        "code": "invalid-code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_verifier": "test-code-verifier",
    }
    response = client.post("/api/token", json=payload)

    assert response.status_code == 400
