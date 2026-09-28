from sqlalchemy.orm import Session

from app.models.registro import SolicitudRegistro


def crear_solicitud(
    db: Session,
    nombre: str,
    email: str,
) -> SolicitudRegistro:
    solicitud = SolicitudRegistro(
        nombre=nombre,
        email=email,
        estado="PENDIENTE",
    )
    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)

    return solicitud