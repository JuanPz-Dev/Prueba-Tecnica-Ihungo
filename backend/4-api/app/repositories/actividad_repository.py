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
) -> bool:
    actividad = db.scalar(
        select(Actividad).where(
            Actividad.asociado_id == asociado_id,
            Actividad.fecha_inicio < fecha_fin,
            Actividad.fecha_fin > fecha_inicio,
        )
    )

    return actividad is not None