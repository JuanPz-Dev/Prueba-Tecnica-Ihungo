from datetime import datetime, timedelta


def obtener_token(client, email, password):
    response = client.post(
        "/api/auth/token/",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access"]


def crear_actividad(client, token, asociado_id, dias):
    inicio = datetime.now() + timedelta(days=dias)
    fin = inicio + timedelta(hours=2)

    return client.post(
        "/api/actividades/",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "tipo_actividad": "Actividad de prueba",
            "descripcion": None,
            "fecha_inicio": inicio.isoformat(),
            "fecha_fin": fin.isoformat(),
            "asociado_id": asociado_id,
        },
    )


def test_admin_puede_ver_actividades(client):
    token_admin = obtener_token(
        client,
        "admin@test.com",
        "123456",
    )

    crear = crear_actividad(
        client,
        token_admin,
        asociado_id=2,
        dias=5,
    )

    assert crear.status_code == 201

    response = client.get(
        "/api/actividades/",
        headers={
            "Authorization": f"Bearer {token_admin}",
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_asociado_puede_ver_su_actividad(client):
    token_admin = obtener_token(
        client,
        "admin@test.com",
        "123456",
    )

    crear = crear_actividad(
        client,
        token_admin,
        asociado_id=2,
        dias=5,
    )

    assert crear.status_code == 201

    token_asociado = obtener_token(
        client,
        "asociado@test.com",
        "123456",
    )

    response = client.get(
        "/api/actividades/",
        headers={
            "Authorization": f"Bearer {token_asociado}",
        },
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["asociado_id"] == 2

def test_asociado_no_puede_ver_actividad_de_otro_asociado(client):
    token_admin = obtener_token(
        client,
        "admin@test.com",
        "123456",
    )
    crear = crear_actividad(
        client,
        token_admin,
        asociado_id=3,
        dias=6,
    )
    assert crear.status_code == 201
    token_asociado = obtener_token(
        client,
        "asociado@test.com",
        "123456",
    )
    response = client.get(
        "/api/actividades/",
        headers={
            "Authorization": f"Bearer {token_asociado}",
        },
    )
    assert response.status_code == 200
    actividades = response.json()
    assert len(actividades) == 0