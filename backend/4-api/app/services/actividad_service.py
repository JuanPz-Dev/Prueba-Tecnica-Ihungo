from datetime import datetime


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