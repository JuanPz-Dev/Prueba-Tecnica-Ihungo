def test_eliminar_actividad(client):
    crear = client.post(
        "/api/actividades/",
        json={
            "tipo_actividad": "Actividad para eliminar",
            "descripcion": None,
            "fecha_inicio": "2030-01-10T10:00:00",
            "fecha_fin": "2030-01-10T12:00:00",
            "asociado_id": 1,
        },
    )

    assert crear.status_code == 201

    actividad_id = crear.json()["id"]

    response = client.delete(
        f"/api/actividades/{actividad_id}/"
    )

    assert response.status_code == 204

    consulta = client.get(
        "/api/actividades/"
    )

    assert consulta.status_code == 200
    assert all(
        actividad["id"] != actividad_id
        for actividad in consulta.json()
    )


def test_eliminar_actividad_inexistente(client):
    response = client.delete(
        "/api/actividades/9999/"
    )

    assert response.status_code == 404