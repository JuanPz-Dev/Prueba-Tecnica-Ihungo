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


def test_eliminar_actividad(client):
    token = obtener_token_admin(client)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    crear = client.post(
        "/api/actividades/",
        headers=headers,
        json={
            "tipo_actividad": "Actividad para eliminar",
            "descripcion": None,
            "fecha_inicio": "2030-01-10T10:00:00",
            "fecha_fin": "2030-01-10T12:00:00",
            "asociado_id": 2,
        },
    )
    assert crear.status_code == 201
    actividad_id = crear.json()["id"]
    response = client.delete(
        f"/api/actividades/{actividad_id}/",
        headers=headers,
    )

    assert response.status_code == 204

    consulta = client.get(
        "/api/actividades/",
        headers=headers,
    )

    assert consulta.status_code == 200

    assert all(
        actividad["id"] != actividad_id
        for actividad in consulta.json()
    )


def test_eliminar_actividad_inexistente(client):
    token = obtener_token_admin(client)

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = client.delete(
        "/api/actividades/9999/",
        headers=headers,
    )
    assert response.status_code == 404