import uuid

from tests.utils import create_client, create_user


def test_login_form_returns_html(client):
    _, client_response = create_client(client, redirect_uri=f"https://example.com/callback/{uuid.uuid4().hex}")
    client_name = client_response["name"]

    response = client.get(f"/{client_name}/login")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_login_success_redirects(client):
    redirect_uri = f"https://oidcdebugger.com/{uuid.uuid4().hex}"
    client_payload, client_response = create_client(client, redirect_uri=redirect_uri)
    client_id = client_response["client_id"]
    client_name = client_response["name"]

    username, password, _ = create_user(client, client_name)

    authorize_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": client_payload["redirect_uri"],
        "scope": "read",
        "code_challenge": "a72fL0zbTgmgq4vJ2n_gwF_uMCyBy04aSbyTR2UuP7w",
        "code_challenge_method": "S256",
    }

    auth_response = client.get("/api/authorize", params=authorize_params, follow_redirects=False)

    assert auth_response.status_code == 302
    assert auth_response.headers["location"] == f"/{client_name}/login"

    response = client.post(
        f"/{client_name}/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["location"].startswith("http://testserver/api/authorize")


def test_login_invalid_credentials_returns_400(client):
    _, client_response = create_client(client, redirect_uri=f"https://example.com/callback/{uuid.uuid4().hex}")
    client_name = client_response["name"]

    response = client.post(f"/{client_name}/login", data={"username": "missing", "password": "wrong"})

    assert response.status_code == 400
