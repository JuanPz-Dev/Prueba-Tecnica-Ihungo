from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.usuario import Usuario


def obtener_asociados(db: Session) -> list[Usuario]:
    return list(
        db.scalars(
            select(Usuario).where(Usuario.rol == "ASOCIADO")
        )
    )


def buscar_por_email(db: Session, email: str) -> Usuario | None:
    return db.scalar(
        select(Usuario).where(Usuario.email == email)
    )


def buscar_por_identificacion(
    db: Session,
    identificacion: str,
) -> Usuario | None:
    return db.scalar(
        select(Usuario).where(
            Usuario.identificacion == identificacion
        )
    )


def guardar(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario