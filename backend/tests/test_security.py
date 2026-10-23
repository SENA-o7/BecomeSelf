from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings
from app.security import (
    ALGORITHM,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


# --- Şifre hash'leme ---


def test_hash_password_does_not_return_plain_password():
    hashed = hash_password("gizli123")

    assert hashed != "gizli123"
    assert "gizli123" not in hashed


def test_hash_password_gives_different_hash_each_time():
    first = hash_password("gizli123")
    second = hash_password("gizli123")

    assert first != second


def test_verify_password_accepts_correct_password():
    hashed = hash_password("gizli123")

    assert verify_password("gizli123", hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("gizli123")

    assert verify_password("Gizli123", hashed) is False
    assert verify_password("yanlis", hashed) is False
    assert verify_password("", hashed) is False


# --- Token ---


def test_access_token_round_trip_returns_user_id():
    token = create_access_token(42)

    assert decode_access_token(token) == 42


def test_decode_access_token_rejects_garbage():
    assert decode_access_token("sahte.token.123") is None
    assert decode_access_token("") is None


def test_decode_access_token_rejects_token_signed_with_other_key():
    payload = {"sub": "42", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)}
    forged = jwt.encode(payload, "saldirganin-bildigi-baska-bir-anahtar-123", algorithm=ALGORITHM)

    assert decode_access_token(forged) is None


def test_decode_access_token_rejects_expired_token():
    payload = {"sub": "42", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}
    expired = jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

    assert decode_access_token(expired) is None
