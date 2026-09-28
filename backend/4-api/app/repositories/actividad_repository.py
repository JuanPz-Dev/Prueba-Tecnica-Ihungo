from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.actividad import Actividad


def guardar(db: Session, actividad: Actividad) -> Actividad:
    db.add(actividad)
    db.commit()
    db.refresh(actividad)
    return actividad


def existe_solapamiento(
    db: Session,
    asociado_id: int,
    fecha_inicio,
    fecha_fin,
    excluir_id: int | None = None,
) -> bool:
    consulta = select(Actividad).where(
        Actividad.asociado_id == asociado_id,
        Actividad.fecha_inicio < fecha_fin,
        Actividad.fecha_fin > fecha_inicio,
    )

    if excluir_id is not None:
        consulta = consulta.where(
            Actividad.id != excluir_id
        )

    actividad = db.scalar(consulta)

    return actividad is not None

def listar(
    db: Session,
    desde=None,
    hasta=None,
    usuario_id: int | None = None,
    rol: str | None = None,
) -> list[Actividad]:
    consulta = select(Actividad)

    if desde is not None:
        consulta = consulta.where(
            Actividad.fecha_inicio >= desde
        )
    if hasta is not None:
        consulta = consulta.where(
            Actividad.fecha_fin <= hasta
        )
    if rol != "ADMIN" and usuario_id is not None:
        consulta = consulta.where(
            (Actividad.asociado_id == usuario_id)
            | (Actividad.creador_id == usuario_id)
        )
    consulta = consulta.order_by(
        Actividad.fecha_inicio
    )
    return list(db.scalars(consulta))

def buscar_por_id(
    db: Session,
    actividad_id: int,
) -> Actividad | None:
    return db.scalar(
        select(Actividad).where(
            Actividad.id == actividad_id
        )
    )

def actualizar(
    db: Session,
    actividad: Actividad,
) -> Actividad:
    db.commit()
    db.refresh(actividad)
    return actividad

def eliminar(
    db: Session,
    actividad: Actividad,
) -> None:
    db.delete(actividad)
    db.commit()