from datetime import datetime, timedelta


def obtener_token_admin(client):
    response = client.post(
        "/api/auth/token/",
        json={
            "email": "admin@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    return response.json()["access"]


def test_crear_actividad(client):
    token = obtener_token_admin(client)

    inicio = datetime.now() + timedelta(days=1)
    fin = inicio + timedelta(hours=2)

    response = client.post(
        "/api/actividades/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "tipo_actividad": "Visita técnica",
            "descripcion": "Visita a las instalaciones",
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "asociado_id": 1,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["tipo_actividad"] == "Visita técnica"
    assert data["asociado_id"] == 1


def test_rechaza_fecha_fin_anterior(client):
    token = obtener_token_admin(client)

    inicio = datetime.now() + timedelta(days=1)
    fin = inicio - timedelta(hours=1)

    response = client.post(
        "/api/actividades/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "tipo_actividad": "Visita técnica",
            "descripcion": None,
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "asociado_id": 1,
        },
    )

    assert response.status_code == 400


def test_rechaza_actividad_solapada(client):
    token = obtener_token_admin(client)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    inicio = datetime.now() + timedelta(days=2)
    fin = inicio + timedelta(hours=2)

    primera = client.post(
        "/api/actividades/",
        headers=headers,
        json={
            "tipo_actividad": "Primera actividad",
            "descripcion": None,
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "asociado_id": 1,
        },
    )

    assert primera.status_code == 201

    segunda = client.post(
        "/api/actividades/",
        headers=headers,
        json={
            "tipo_actividad": "Segunda actividad",
            "descripcion": None,
            "fecha_inicio": (
                inicio + timedelta(hours=1)
            ).isoformat(),
            "fecha_fin": (
                fin + timedelta(hours=1)
            ).isoformat(),
            "asociado_id": 1,
        },
    )

    assert segunda.status_code == 409