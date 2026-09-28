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
    usuario_id: int | None = None,
    rol: str | None = None,
) -> list[Actividad]:
    return actividad_repository.listar(
        db,desde,hasta,usuario_id,rol,
    )

def validar_permiso_actividad(
    actividad: Actividad,
    usuario_id: int,
    rol: str,
) -> None:
    if rol == "ADMIN":
        return

    if actividad.asociado_id != usuario_id:
        raise PermissionError(
            "No tiene permiso para modificar esta actividad."
        )

    if actividad.fecha_inicio < datetime.now():
        raise PermissionError(
            "Las actividades pasadas son solo de lectura."
        )

def actualizar_actividad(
    db: Session,
    actividad_id: int,
    usuario_id: int,
    rol: str,
    tipo_actividad: str | None = None,
    descripcion: str | None = None,
    fecha_inicio: datetime | None = None,
    fecha_fin: datetime | None = None,
    asociado_id: int | None = None,
) -> Actividad:
    actividad = actividad_repository.buscar_por_id(
        db,
        actividad_id,
    )

    if actividad is None:
        raise LookupError("La actividad no existe.")

    validar_permiso_actividad(
        actividad,
        usuario_id,
        rol,
    )

    nuevo_inicio = (
        fecha_inicio
        if fecha_inicio is not None
        else actividad.fecha_inicio
    )

    nuevo_fin = (
        fecha_fin
        if fecha_fin is not None
        else actividad.fecha_fin
    )

    validar_fechas(
        nuevo_inicio,
        nuevo_fin,
    )

    nuevo_asociado = (
        asociado_id
        if asociado_id is not None
        else actividad.asociado_id
    )

    if actividad_repository.existe_solapamiento(
        db,
        nuevo_asociado,
        nuevo_inicio,
        nuevo_fin,
        excluir_id=actividad_id,
    ):
        raise ValueError(
            "El asociado ya tiene una actividad en ese horario."
        )

    if tipo_actividad is not None:
        actividad.tipo_actividad = tipo_actividad

    if descripcion is not None:
        actividad.descripcion = descripcion

    if fecha_inicio is not None:
        actividad.fecha_inicio = fecha_inicio

    if fecha_fin is not None:
        actividad.fecha_fin = fecha_fin

    if asociado_id is not None:
        actividad.asociado_id = asociado_id

    return actividad_repository.actualizar(
        db,
        actividad,
    )

def eliminar_actividad(
    db: Session,
    actividad_id: int,
    usuario_id: int,
    rol: str,
) -> None:
    actividad = actividad_repository.buscar_por_id(
        db,
        actividad_id,
    )
    if actividad is None:
        raise LookupError("La actividad no existe.")
    validar_permiso_actividad(
        actividad,
        usuario_id,
        rol,
    )
    actividad_repository.eliminar(
        db,
        actividad,
    )