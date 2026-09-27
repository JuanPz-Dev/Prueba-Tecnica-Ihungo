from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.usuario import Usuario


def autenticar_usuario(
    db: Session,
    email: str,
    password: str,
) -> Usuario | None:
    usuario = db.scalar(
        select(Usuario).where(Usuario.email == email)
    )

    if usuario is None:
        return None

    if not verify_password(password, usuario.password_hash):
        return None

    return usuario


def generar_tokens(usuario: Usuario) -> dict:
    datos = {
        "sub": str(usuario.id),
        "email": usuario.email,
        "rol": usuario.rol,
    }

    return {
        "access": create_access_token(datos),
        "refresh": create_refresh_token(datos),
    }