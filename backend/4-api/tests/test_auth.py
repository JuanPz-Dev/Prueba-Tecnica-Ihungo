from datetime import datetime, timedelta

import pytest


def test_crear_access_token():
    from app.core.security import create_access_token

    token = create_access_token({"sub": "usuario@test.com"})

    assert token
    assert isinstance(token, str)


def test_decode_access_token():
    from app.core.security import create_access_token, decode_access_token

    token = create_access_token({"sub": "usuario@test.com"})
    payload = decode_access_token(token)

    assert payload["sub"] == "usuario@test.com"


def test_token_invalido_es_rechazado():
    from app.core.security import decode_access_token

    with pytest.raises(ValueError):
        decode_access_token("token-invalido")