from datetime import datetime

from sqlalchemy.orm import Session

from app.models.actividad import Actividad
from app.repositories import actividad_repository


def validar_fechas(inicio: datetime, fin: datetime) -> None:
    if fin <= inicio:
        raise ValueError(
            "La fecha de fin debe ser posterior a la fecha de inicio."
        )


def hay_solapamiento(
    inicio_existente: datetime,
    fin_existente: datetime,
    inicio_nueva: datetime,
    fin_nueva: datetime,
) -> bool:
    return inicio_nueva < fin_existente and fin_nueva > inicio_existente


def crear_actividad(
    db: Session,
    tipo_actividad: str,
    descripcion: str | None,
    fecha_inicio: datetime,
    fecha_fin: datetime,
    asociado_id: int,
    creador_id: int,
) -> Actividad:
    validar_fechas(fecha_inicio, fecha_fin)

    if actividad_repository.existe_solapamiento(
        db,
        asociado_id,
        fecha_inicio,
        fecha_fin,
    ):
        raise ValueError(
            "El asociado ya tiene una actividad en ese horario."
        )

    actividad = Actividad(
        tipo_actividad=tipo_actividad,
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        asociado_id=asociado_id,
        creador_id=creador_id,
    )

    return actividad_repository.guardar(db, actividad)

def listar_actividades(
    db: Session,
    desde=None,
    hasta=None,
) -> list[Actividad]:
    return actividad_repository.listar(
        db,
        desde,
        hasta,
    )