import csv
from datetime import datetime
from io import TextIOWrapper

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.actividad import Actividad
from app.models.usuario import Usuario
from app.repositories import actividad_repository

def cargar_asociados(db: Session, archivo) -> dict:
    lector = csv.DictReader(
        TextIOWrapper(archivo.file, encoding="utf-8-sig")
    )

    requeridas = {
        "identificacion",
        "nombre",
        "apellidos",
        "email",
        "ciudad",
        "password",
    }

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

    return {
        "procesadas": procesadas,
        "creadas": creadas,
        "errores": errores,
    }

def cargar_actividades(db: Session, archivo) -> dict:
    lector = csv.DictReader(
        TextIOWrapper(archivo.file, encoding="utf-8-sig")
    )
    requeridas = {
        "tipo_actividad",
        "descripcion",
        "fecha_inicio",
        "fecha_fin",
        "asociado_id",
    }
    if not lector.fieldnames or not requeridas.issubset(lector.fieldnames):
        raise ValueError("El CSV no contiene las columnas requeridas.")

    procesadas = 0
    creadas = 0
    errores = []

    for numero_fila, fila in enumerate(lector, start=2):
        procesadas += 1

        try:
            inicio = datetime.fromisoformat(fila["fecha_inicio"])
            fin = datetime.fromisoformat(fila["fecha_fin"])
            asociado_id = int(fila["asociado_id"])
            if fin <= inicio: raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")
            asociado = db.get(Usuario, asociado_id)
            if asociado is None or asociado.rol != "ASOCIADO":
                raise ValueError("El asociado no existe.")
            if actividad_repository.existe_solapamiento(
                db,
                asociado_id,
                inicio,
                fin,
            ):
                raise ValueError("El asociado ya tiene una actividad en ese horario.")
            actividad = Actividad(
                tipo_actividad=fila["tipo_actividad"],
                descripcion=fila["descripcion"] or None,
                fecha_inicio=inicio,
                fecha_fin=fin,
                asociado_id=asociado_id,
                creador_id=int(asociado_id),
            )
            db.add(actividad)
            db.commit()
            creadas += 1
        except Exception as exc:
            db.rollback()
            errores.append(
                {"fila": numero_fila,"error": str(exc),})

    return {
        "procesadas": procesadas,
        "creadas": creadas,
        "errores": errores,
    }

def cargar_actividades(db: Session,archivo,creador_id: int,) -> dict:
    lector = csv.DictReader(
        TextIOWrapper(archivo.file, encoding="utf-8-sig")
    )

    requeridas = {"tipo_actividad","descripcion","fecha_inicio","fecha_fin","asociado_id",}

    if not lector.fieldnames or not requeridas.issubset(lector.fieldnames):
        raise ValueError("El CSV no contiene las columnas requeridas.")

    procesadas = 0
    creadas = 0
    errores = []

    for numero_fila, fila in enumerate(lector, start=2):
        procesadas += 1

        try:
            inicio = datetime.fromisoformat(fila["fecha_inicio"])
            fin = datetime.fromisoformat(fila["fecha_fin"])
            asociado_id = int(fila["asociado_id"])

            if fin <= inicio:
                raise ValueError(
                    "La fecha de fin debe ser posterior a la fecha de inicio."
                )

            asociado = db.get(Usuario, asociado_id)
            if asociado is None or asociado.rol != "ASOCIADO":
                raise ValueError("El asociado no existe.")
            if actividad_repository.existe_solapamiento(
                db,
                asociado_id,
                inicio,
                fin,
            ):
                raise ValueError(
                    "El asociado ya tiene una actividad en ese horario."
                )

            actividad = Actividad(
                tipo_actividad=fila["tipo_actividad"],
                descripcion=fila["descripcion"] or None,
                fecha_inicio=inicio,
                fecha_fin=fin,
                asociado_id=asociado_id,
                creador_id=creador_id,
            )

            db.add(actividad)
            db.commit()
            creadas += 1

        except Exception as exc:
            db.rollback()
            errores.append({"fila": numero_fila,"error": str(exc),})
    return {
        "procesadas": procesadas,
        "creadas": creadas,
        "errores": errores,
    }