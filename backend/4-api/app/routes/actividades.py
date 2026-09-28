from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import obtener_usuario_actual
from app.database import get_db
from app.schemas.actividad import (
    ActividadCreate,
    ActividadResponse,
    ActividadUpdate,
)
from app.services.actividad_service import (
    actualizar_actividad,
    crear_actividad,
    eliminar_actividad,
    listar_actividades,
)

router = APIRouter(
    prefix="/api/actividades",
    tags=["Actividades"],
)


@router.get("/",response_model=list[ActividadResponse],)
def listar(
    desde: datetime | None = None,
    hasta: datetime | None = None,
    usuario_actual: dict = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db),
):
    return listar_actividades(db,desde,hasta,int(usuario_actual["sub"]),usuario_actual["rol"],)

@router.post("/",response_model=ActividadResponse,status_code=201,)
def registrar_actividad(
    datos: ActividadCreate,
    usuario_actual: dict = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db),
):
    try:
        return crear_actividad(
            db=db,
            tipo_actividad=datos.tipo_actividad,
            descripcion=datos.descripcion,
            fecha_inicio=datos.fecha_inicio,
            fecha_fin=datos.fecha_fin,
            asociado_id=datos.asociado_id,
            creador_id=int(usuario_actual["sub"]),
        )
    except ValueError as exc:
        mensaje = str(exc)

        if "horario" in mensaje:
            raise HTTPException(
                status_code=409,
                detail=mensaje,
            ) from exc

        raise HTTPException(
            status_code=400,
            detail=mensaje,
        ) from exc


@router.patch(
    "/{actividad_id}/",
    response_model=ActividadResponse,
)
def modificar_actividad(
    actividad_id: int,
    datos: ActividadUpdate,
    db: Session = Depends(get_db),
):
    try:
        return actualizar_actividad(
            db=db,
            actividad_id=actividad_id,
            tipo_actividad=datos.tipo_actividad,
            descripcion=datos.descripcion,
            fecha_inicio=datos.fecha_inicio,
            fecha_fin=datos.fecha_fin,
            asociado_id=datos.asociado_id,
        )
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        mensaje = str(exc)

        if "horario" in mensaje:
            raise HTTPException(
                status_code=409,
                detail=mensaje,
            ) from exc

        raise HTTPException(
            status_code=400,
            detail=mensaje,
        ) from exc


@router.delete(
    "/{actividad_id}/",
    status_code=204,
)
def eliminar(
    actividad_id: int,
    db: Session = Depends(get_db),
):
    try:
        eliminar_actividad(
            db,
            actividad_id,
        )
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc