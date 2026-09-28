from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.database import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

password_hash = PasswordHash.recommended()

security = HTTPBearer()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    password: str,
    password_hash_value: str,
) -> bool:
    return password_hash.verify(
        password,
        password_hash_value,
    )


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["type"] = "access"
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def create_refresh_token(data: dict) -> str:
    payload = data.copy()
    payload["type"] = "refresh"
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS,
    )

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        if payload.get("type") != "access":
            raise ValueError("Token inválido.")

        return payload

    except JWTError as exc:
        raise ValueError("Token inválido.") from exc


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    try:
        return decode_access_token(
            credentials.credentials,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail="Token inválido.",
        ) from exc