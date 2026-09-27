from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.security import ALGORITHM, create_access_token
from app.database import get_db, settings
from app.schemas.auth import RefreshRequest, TokenRequest
from app.services.auth_service import autenticar_usuario, generar_tokens

router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"],
)


@router.post("/token/")
def login(
    datos: TokenRequest,
    db: Session = Depends(get_db),
):
    usuario = autenticar_usuario(
        db,
        datos.email,
        datos.password,
    )

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos.",
        )

    return generar_tokens(usuario)


@router.post("/token/refresh/")
def refresh_token(datos: RefreshRequest):
    try:
        payload = jwt.decode(
            datos.refresh,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="El token no es de tipo refresh.",
            )

        nuevo_access = create_access_token(
            {
                "sub": payload["sub"],
                "email": payload["email"],
                "rol": payload["rol"],
            }
        )

        return {"access": nuevo_access}

    except (JWTError, KeyError):
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido.",
        )