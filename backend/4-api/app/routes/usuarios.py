from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import obtener_usuario_actual
from app.database import get_db
from app.schemas.usuario import UsuarioResponse
from app.services.asociado_service import obtener_usuario_por_email

router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuarios"],
)


@router.get("/me/",response_model=UsuarioResponse,)
def obtener_perfil(
    usuario_actual: dict = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db),
):
    usuario = obtener_usuario_por_email(
        db,
        usuario_actual["email"],
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado.",
        )
    return usuario