from datetime import datetime, timedelta

def test_actualizar_actividad(client):
    inicio = datetime.now() + timedelta(days=1)
    fin = inicio + timedelta(hours=2)

    crear = client.post(
        "/api/actividades/",
        json={
            "tipo_actividad": "Visita técnica",
            "descripcion": "Actividad inicial",
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "asociado_id": 1,
        },
    )

    assert crear.status_code == 201
    actividad_id = crear.json()["id"]

    nuevo_inicio = inicio + timedelta(hours=3)
    nuevo_fin = nuevo_inicio + timedelta(hours=2)

    response = client.patch(
        f"/api/actividades/{actividad_id}/",
        json={
            "fecha_inicio": nuevo_inicio.isoformat(),
            "fecha_fin": nuevo_fin.isoformat(),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == actividad_id
    assert data["fecha_inicio"] == nuevo_inicio.isoformat()
    assert data["fecha_fin"] == nuevo_fin.isoformat()


def test_actualizar_actividad_rechaza_fecha_invalida(client):
    inicio = datetime.now() + timedelta(days=1)
    fin = inicio + timedelta(hours=2)

    crear = client.post(
        "/api/actividades/",
        json={
            "tipo_actividad": "Visita técnica",
            "descripcion": None,
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "asociado_id": 1,
        },
    )

    assert crear.status_code == 201
    actividad_id = crear.json()["id"]

    response = client.patch(
        f"/api/actividades/{actividad_id}/",
        json={
            "fecha_inicio": fin.isoformat(),
            "fecha_fin": inicio.isoformat(),
        },
    )

    assert response.status_code == 400

def test_actualizar_actividad_inexistente(client):
    response = client.patch(
        "/api/actividades/9999/",
        json={
            "tipo_actividad": "Actividad nueva",
        },
    )

    assert response.status_code == 404

def test_reprogramar_actividad_rechaza_solapamiento(client):
    base = datetime.now() + timedelta(days=3)

    primera = client.post(
        "/api/actividades/",
        json={
            "tipo_actividad": "Primera actividad",
            "descripcion": None,
            "fecha_inicio": base.isoformat(),
            "fecha_fin": (base + timedelta(hours=2)).isoformat(),
            "asociado_id": 1,
        },
    )

    assert primera.status_code == 201

    segunda = client.post(
        "/api/actividades/",
        json={
            "tipo_actividad": "Segunda actividad",
            "descripcion": None,
            "fecha_inicio": (
                base + timedelta(hours=3)
            ).isoformat(),
            "fecha_fin": (
                base + timedelta(hours=5)
            ).isoformat(),
            "asociado_id": 1,
        },
    )

    assert segunda.status_code == 201

    segunda_id = segunda.json()["id"]

    response = client.patch(
        f"/api/actividades/{segunda_id}/",
        json={
            "fecha_inicio": (
                base + timedelta(hours=1)
            ).isoformat(),
            "fecha_fin": (
                base + timedelta(hours=4)
            ).isoformat(),
        },
    )

    assert response.status_code == 409