import uuid


def test_list_claims_returns_list(client):
    response = client.get("/api/claims")

    assert response.status_code == 200

    payload = response.json()
    assert "claims" in payload
    assert isinstance(payload["claims"], list)


def test_create_claim_returns_created_claim(client):
    claim_name = f"test-claim-{uuid.uuid4().hex}"

    response = client.post("/api/claims", json={"name": claim_name})

    assert response.status_code == 201

    payload = response.json()
    assert payload["name"] == claim_name
    assert "id" in payload


def test_delete_claim_removes_claim(client):
    claim_name = f"test-claim-delete-{uuid.uuid4().hex}"
    created = client.post("/api/claims", json={"name": claim_name})

    assert created.status_code == 201

    claim_id = created.json()["id"]
    response = client.delete(f"/api/claims/{claim_id}")

    assert response.status_code == 200


def test_create_claim_duplicate_returns_409(client):
    claim_name = f"test-claim-dup-{uuid.uuid4().hex}"
    client.post("/api/claims", json={"name": claim_name})

    response = client.post("/api/claims", json={"name": claim_name})

    assert response.status_code == 409
