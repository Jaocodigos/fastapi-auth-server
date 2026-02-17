def test_jwks_returns_keys(client):
    response = client.get("/api/.well-known/jwks.json")

    assert response.status_code == 200

    payload = response.json()
    assert "keys" in payload
    assert isinstance(payload["keys"], list)
    assert payload["keys"]

    key = payload["keys"][0]
    assert key["kty"] == "RSA"
    assert "kid" in key
    assert key["use"] == "sig"
    assert key["alg"] == "RS256"
    assert "n" in key
    assert "e" in key
