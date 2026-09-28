import csv
from io import TextIOWrapper

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.usuario import Usuario

def cargar_asociados(db: Session, archivo) -> dict:
    lector = csv.DictReader(TextIOWrapper(archivo.file, encoding="utf-8-sig"))
    requeridas = {"identificacion", "nombre", "apellidos", "email", "ciudad","password",}
    if not lector.fieldnames or not requeridas.issubset(lector.fieldnames):
        raise ValueError("El CSV no contiene las columnas requeridas.")
    procesadas = 0
    creadas = 0
    errores = []
    for numero_fila, fila in enumerate(lector, start=2):
        procesadas += 1

        try:
            if not fila["email"] or "@" not in fila["email"]:
                raise ValueError("Email inválido.")

            if db.query(Usuario).filter(
                (Usuario.email == fila["email"])
                | (Usuario.identificacion == fila["identificacion"])
            ).first():
                raise ValueError("El asociado ya existe.")

            asociado = Usuario(
                identificacion=fila["identificacion"],
                nombre=fila["nombre"],
                apellidos=fila["apellidos"],
                email=fila["email"],
                ciudad=fila["ciudad"],
                password_hash=hash_password(fila["password"]),
                rol="ASOCIADO",
            )

            db.add(asociado)
            db.commit()
            creadas += 1

        except Exception as exc:
            db.rollback()
            errores.append(
                {
                    "fila": numero_fila,
                    "error": str(exc),
                }
            )
    return {"procesadas": procesadas,"creadas": creadas,"errores": errores,}