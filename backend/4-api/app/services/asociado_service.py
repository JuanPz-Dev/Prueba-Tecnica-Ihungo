from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.repositories import asociado_repository


def obtener_asociados(db: Session) -> list[Usuario]:
    return asociado_repository.obtener_asociados(db)


def crear_asociado(
    db: Session,
    identificacion: str,
    nombre: str,
    apellidos: str,
    email: str,
    ciudad: str,
    password: str,
) -> Usuario:
    if asociado_repository.buscar_por_email(db, email):
        raise ValueError("El email ya está registrado.")

    if asociado_repository.buscar_por_identificacion(
        db,
        identificacion,
    ):
        raise ValueError("La identificación ya está registrada.")

    usuario = Usuario(
        identificacion=identificacion,
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        ciudad=ciudad,
        password_hash=hash_password(password),
        rol="ASOCIADO",
    )

    return asociado_repository.guardar(db, usuario)

def obtener_usuario_por_email(
    db: Session,
    email: str,
) -> Usuario | None:
    return asociado_repository.buscar_por_email(
        db,
        email,
    )