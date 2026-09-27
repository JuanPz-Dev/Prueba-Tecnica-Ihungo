from datetime import datetime, timedelta


def test_listar_actividades(client):
    inicio = datetime.now() + timedelta(days=1)
    fin = inicio + timedelta(hours=2)

    crear = client.post(
        "/api/actividades/",
        json={
            "tipo_actividad": "Visita técnica",
            "descripcion": "Actividad de prueba",
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "asociado_id": 1,
        },
    )

    assert crear.status_code == 201

    response = client.get("/api/actividades/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_filtrar_actividades_por_rango(client):
    base = datetime.now() + timedelta(days=2)

    primera = client.post(
        "/api/actividades/",
        json={
            "tipo_actividad": "Actividad dentro",
            "descripcion": None,
            "fecha_inicio": base.isoformat(),
            "fecha_fin": (base + timedelta(hours=1)).isoformat(),
            "asociado_id": 1,
        },
    )

    assert primera.status_code == 201

    fuera = base + timedelta(days=5)

    segunda = client.post(
        "/api/actividades/",
        json={
            "tipo_actividad": "Actividad fuera",
            "descripcion": None,
            "fecha_inicio": fuera.isoformat(),
            "fecha_fin": (fuera + timedelta(hours=1)).isoformat(),
            "asociado_id": 1,
        },
    )

    assert segunda.status_code == 201

    desde = base - timedelta(hours=1)
    hasta = base + timedelta(hours=2)

    response = client.get(
        "/api/actividades/",
        params={
            "desde": desde.isoformat(),
            "hasta": hasta.isoformat(),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["tipo_actividad"] == "Actividad dentro"