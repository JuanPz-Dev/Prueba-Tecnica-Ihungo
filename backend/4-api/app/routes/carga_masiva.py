from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.security import obtener_usuario_actual
from app.database import get_db
from app.services.carga_service import cargar_asociados

router = APIRouter(
    prefix="/api/carga-masiva",
    tags=["Carga masiva"],
)


@router.post("/asociados/", status_code=201)
def cargar_asociados_endpoint(
    archivo: UploadFile = File(...),
    usuario_actual=Depends(obtener_usuario_actual),
    db: Session = Depends(get_db),
):
    if usuario_actual["rol"] != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Solo un administrador puede realizar cargas masivas.",
        )

    if not archivo.filename or not archivo.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser CSV.",
        )

    try:
        return cargar_asociados(db, archivo)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc