import uuid
from urllib.parse import urlparse, parse_qs

from tests.utils import authorize_code, create_client, create_user


def test_authorize_requires_login(client):
    redirect_uri = f"https://example.com/callback/{uuid.uuid4().hex}"
    _, client_response = create_client(client, redirect_uri=redirect_uri)
    client_id = client_response["client_id"]

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "read",
        "code_challenge": "0FLIKahrX7kqxncwhV5WD82lu_wi5GA8FsRSLubaOpU",
        "code_challenge_method": "S256",
    }
    response = client.get("/api/authorize", params=params, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "/login"


def test_authorize_redirects_with_code(client):
    redirect_uri = f"https://example.com/callback/{uuid.uuid4().hex}"
    _, client_response = create_client(client, redirect_uri=redirect_uri)
    client_id = client_response["client_id"]
    username, password, _ = create_user(client)

    login = client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )
    assert login.status_code == 302

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "read",
        "code_challenge": "0FLIKahrX7kqxncwhV5WD82lu_wi5GA8FsRSLubaOpU",
        "code_challenge_method": "S256",
    }
    response, code = authorize_code(client, client_id, redirect_uri)

    location = response.headers["location"]
    parsed = urlparse(location)
    assert location.startswith(redirect_uri)

    query = parse_qs(parsed.query)
    assert "code" in query
    assert code


def test_authorize_rejects_invalid_scope(client):
    redirect_uri = f"https://example.com/callback/{uuid.uuid4().hex}"
    _, client_response = create_client(client, redirect_uri=redirect_uri)
    client_id = client_response["client_id"]
    username, password, _ = create_user(client)

    login = client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )
    assert login.status_code == 302

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "invalid",
        "code_challenge": "0FLIKahrX7kqxncwhV5WD82lu_wi5GA8FsRSLubaOpU",
        "code_challenge_method": "S256",
    }
    response = client.get("/api/authorize", params=params)

    assert response.status_code == 400
