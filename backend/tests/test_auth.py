from sqlalchemy import select

from app.models import User
from app.security import decode_access_token, verify_password

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"


def register(client, email="sena@example.com", password="gizli1234"):
    return client.post(REGISTER_URL, json={"email": email, "password": password})


def login(client, email="sena@example.com", password="gizli1234"):
    return client.post(LOGIN_URL, json={"email": email, "password": password})


# --- Kayıt ---


def test_register_creates_user(client):
    response = register(client)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "sena@example.com"
    assert isinstance(body["id"], int)
    assert "created_at" in body


def test_register_response_does_not_contain_password(client):
    body = register(client).json()

    assert "password" not in body
    assert "hashed_password" not in body


def test_register_stores_hashed_password(client, db):
    register(client, password="gizli1234")

    user = db.scalar(select(User).where(User.email == "sena@example.com"))
    assert user is not None
    assert user.hashed_password != "gizli1234"
    assert verify_password("gizli1234", user.hashed_password)


def test_register_rejects_duplicate_email(client):
    register(client)

    response = register(client)

    assert response.status_code == 409


def test_register_treats_email_case_insensitively(client):
    register(client, email="sena@example.com")

    response = register(client, email="Sena@Example.com")

    assert response.status_code == 409


def test_register_rejects_invalid_email(client):
    response = register(client, email="bu-bir-eposta-degil")

    assert response.status_code == 422


def test_register_rejects_short_password(client):
    response = register(client, password="1234567")

    assert response.status_code == 422


def test_register_accepts_password_of_minimum_length(client):
    response = register(client, password="12345678")

    assert response.status_code == 201


# --- Giriş ---


def test_login_returns_token_for_correct_credentials(client):
    user_id = register(client).json()["id"]

    response = login(client)

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert decode_access_token(body["access_token"]) == user_id


def test_login_rejects_wrong_password(client):
    register(client, password="gizli1234")

    response = login(client, password="yanlis1234")

    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_login_rejects_unknown_email(client):
    response = login(client, email="kimse@example.com")

    assert response.status_code == 401


def test_login_gives_same_error_for_unknown_email_and_wrong_password(client):
    register(client)

    wrong_password = login(client, password="yanlis1234")
    unknown_email = login(client, email="kimse@example.com")

    assert wrong_password.json()["detail"] == unknown_email.json()["detail"]


def test_login_treats_email_case_insensitively(client):
    register(client, email="sena@example.com")

    response = login(client, email="Sena@Example.com")

    assert response.status_code == 200
