from datetime import datetime, timedelta

import pytest


def test_rechaza_actividad_con_fin_anterior_al_inicio():
    from app.services.actividad_service import validar_fechas

    inicio = datetime(2026, 9, 27, 10, 0)
    fin = datetime(2026, 9, 27, 9, 0)

    with pytest.raises(ValueError):
        validar_fechas(inicio, fin)


def test_acepta_actividad_con_fin_posterior_al_inicio():
    from app.services.actividad_service import validar_fechas

    inicio = datetime(2026, 9, 27, 10, 0)
    fin = datetime(2026, 9, 27, 11, 0)

    validar_fechas(inicio, fin)


def test_detecta_solapamiento():
    from app.services.actividad_service import hay_solapamiento

    inicio_existente = datetime(2026, 9, 27, 10, 0)
    fin_existente = datetime(2026, 9, 27, 12, 0)

    inicio_nueva = datetime(2026, 9, 27, 11, 0)
    fin_nueva = datetime(2026, 9, 27, 13, 0)

    assert hay_solapamiento(
        inicio_existente,
        fin_existente,
        inicio_nueva,
        fin_nueva,
    )


def test_no_detecta_solapamiento():
    from app.services.actividad_service import hay_solapamiento

    inicio_existente = datetime(2026, 9, 27, 10, 0)
    fin_existente = datetime(2026, 9, 27, 12, 0)

    inicio_nueva = datetime(2026, 9, 27, 12, 0)
    fin_nueva = datetime(2026, 9, 27, 13, 0)

    assert not hay_solapamiento(
        inicio_existente,
        fin_existente,
        inicio_nueva,
        fin_nueva,
    )