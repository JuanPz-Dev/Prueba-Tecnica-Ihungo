from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.actividad import ActividadCreate, ActividadResponse
from app.services.actividad_service import crear_actividad

router = APIRouter(
    prefix="/api/actividades",
    tags=["Actividades"],
)


@router.post(
    "/",
    response_model=ActividadResponse,
    status_code=201,
)
def registrar_actividad(
    datos: ActividadCreate,
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
            creador_id=1,
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