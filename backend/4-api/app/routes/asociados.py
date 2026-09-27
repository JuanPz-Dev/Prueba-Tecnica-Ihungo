from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuario import AsociadoCreate, AsociadoResponse
from app.services.asociado_service import (
    crear_asociado,
    obtener_asociados,
)

router = APIRouter(
    prefix="/api/asociados",
    tags=["Asociados"],
)


@router.get("/", response_model=list[AsociadoResponse])
def listar_asociados(
    db: Session = Depends(get_db),
):
    return obtener_asociados(db)


@router.post(
    "/",
    response_model=AsociadoResponse,
    status_code=201,
)
def registrar_asociado(
    datos: AsociadoCreate,
    db: Session = Depends(get_db),
):
    try:
        return crear_asociado(
            db,
            datos.identificacion,
            datos.nombre,
            datos.apellidos,
            datos.email,
            datos.ciudad,
            datos.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="El asociado ya está registrado.",
        ) from exc