from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings
from app.security import ALGORITHM, create_access_token, decode_access_token

ME_URL = "/me"


def register_and_login(client, email="sena@example.com", password="gizli1234"):
    client.post("/auth/register", json={"email": email, "password": password})
    response = client.post("/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


def test_me_returns_current_user(client):
    token = register_and_login(client, email="sena@example.com")

    response = client.get(ME_URL, headers=bearer(token))

    assert response.status_code == 200
    assert response.json()["email"] == "sena@example.com"


def test_me_returns_the_token_owner_not_another_user(client):
    register_and_login(client, email="ali@example.com")
    sena_token = register_and_login(client, email="sena@example.com")

    response = client.get(ME_URL, headers=bearer(sena_token))

    assert response.json()["email"] == "sena@example.com"


def test_me_does_not_contain_password(client):
    token = register_and_login(client)

    body = client.get(ME_URL, headers=bearer(token)).json()

    assert "password" not in body
    assert "hashed_password" not in body


def test_me_rejects_request_without_token(client):
    response = client.get(ME_URL)

    assert response.status_code == 401


def test_me_rejects_garbage_token(client):
    response = client.get(ME_URL, headers=bearer("sahte.token.123"))

    assert response.status_code == 401


def test_me_rejects_wrong_auth_scheme(client):
    token = register_and_login(client)

    response = client.get(ME_URL, headers={"Authorization": f"Basic {token}"})

    assert response.status_code == 401


def test_me_rejects_expired_token(client):
    user_id = decode_access_token(register_and_login(client))
    payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}
    expired = jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

    response = client.get(ME_URL, headers=bearer(expired))

    assert response.status_code == 401


def test_me_rejects_valid_token_of_nonexistent_user(client):
    token = create_access_token(999999)

    response = client.get(ME_URL, headers=bearer(token))

    assert response.status_code == 401
