import uuid
from urllib.parse import parse_qs, urlparse

TEST_ADMIN_TOKEN = "test-admin-token"


def admin_headers(valid=True):

    if valid:
        return {"Authorization": f"Bearer {TEST_ADMIN_TOKEN}"}

    return {"Authorization": "Bearer test-admin-invalid"}


def create_user(client, client_name, username=None, password="test-password"):

    if username is None:
        username = f"test-user-{uuid.uuid4().hex}"

    response = client.post(
        f"/api/{client_name}/users",
        json={"username": username, "password": password},
        headers=admin_headers()
    )

    assert response.status_code == 201

    return username, password, response.json()


def make_client_payload(redirect_uri, grant_types=None, name=None):

    if grant_types is None:
        grant_types = ["authorization_code"]

    if name is None:
        name = f"test-client-{uuid.uuid4().hex[:8]}"

    return {
        "name": name,
        "redirect_uri": redirect_uri,
        "grant_types": grant_types,
        "client_type": "public",
        "scopes": ["read"],
        "response_type": "code",
        "token_exp": 10,
        "refresh_token_exp": 20,
        "code_exp": 5,
    }


def create_client(client, redirect_uri, grant_types=None, name=None):

    payload = make_client_payload(redirect_uri=redirect_uri, grant_types=grant_types, name=name)

    response = client.post("/api/clients", json=payload, headers=admin_headers())

    assert response.status_code == 201

    return payload, response.json()


def authorize_code(client, client_id, redirect_uri):
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
    location = response.headers["location"]
    query = parse_qs(urlparse(location).query)
    return response, query.get("code", [None])[0]
