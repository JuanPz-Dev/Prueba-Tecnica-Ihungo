from io import BytesIO
from datetime import datetime, timedelta

def obtener_token(client, email="admin@test.com", password="123456"):
    response = client.post(
        "/api/auth/token/",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access"]

def test_carga_masiva_asociados(client):
    token = obtener_token(client)
    csv_content = (
        "identificacion,nombre,apellidos,email,ciudad,password\n"
        "2001,Ana,Gomez,ana@test.com,Cartagena,123456\n"
        "2002,Carlos,Perez,carlos@test.com,Barranquilla,123456\n"
    )

    response = client.post(
        "/api/carga-masiva/asociados/",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "archivo": (
                "asociados.csv",
                BytesIO(csv_content.encode("utf-8")),
                "text/csv",
            )
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["procesadas"] == 2
    assert data["creadas"] == 2
    assert data["errores"] == []

def test_carga_masiva_continua_si_una_fila_falla(client):
    token = obtener_token(client)
    csv_content = (
        "identificacion,nombre,apellidos,email,ciudad,password\n"
        "3001,Ana,Gomez,ana2@test.com,Cartagena,123456\n"
        "3002,Carlos,Perez,correo-invalido,Barranquilla,123456\n"
        "3003,Laura,Diaz,laura@test.com,Cartagena,123456\n"
    )

    response = client.post(
        "/api/carga-masiva/asociados/",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "archivo": (
                "asociados.csv",
                BytesIO(csv_content.encode("utf-8")),
                "text/csv",
            )
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["procesadas"] == 3
    assert data["creadas"] == 2
    assert len(data["errores"]) == 1

def test_carga_masiva_rechaza_archivo_no_csv(client):
    token = obtener_token(client)
    response = client.post(
        "/api/carga-masiva/asociados/",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "archivo": (
                "asociados.txt",
                BytesIO(b"archivo incorrecto"),
                "text/plain",
            )
        },
    )
    assert response.status_code == 400

def test_carga_masiva_actividades(client):
    token = obtener_token(client)
    inicio = datetime.now() + timedelta(days=5)
    fin = inicio + timedelta(hours=2)
    csv_content = (
        "tipo_actividad,descripcion,fecha_inicio,fecha_fin,asociado_id\n"
        f"Reunion,Reunion de prueba,{inicio.isoformat()},{fin.isoformat()},{2}\n"
    )
    response = client.post(
        "/api/carga-masiva/actividades/",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "archivo": (
                "actividades.csv",
                BytesIO(csv_content.encode("utf-8")),
                "text/csv",
            )
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["procesadas"] == 1
    assert data["creadas"] == 1
    assert data["errores"] == []

def test_carga_masiva_actividades_continua_si_una_fila_falla(client):
    token = obtener_token(client)
    inicio = datetime.now() + timedelta(days=10)
    fin = inicio + timedelta(hours=2)
    inicio2 = inicio + timedelta(days=1)
    fin2 = fin + timedelta(days=1)
    csv_content = (
        "tipo_actividad,descripcion,fecha_inicio,fecha_fin,asociado_id\n"
        f"Valida,,{inicio.isoformat()},{fin.isoformat()},2\n"
        f"Invalida,,{fin.isoformat()},{inicio.isoformat()},2\n"
        f"Otra valida,,{inicio2.isoformat()},{fin2.isoformat()},2\n"
    )
    response = client.post(
        "/api/carga-masiva/actividades/",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "archivo": (
                "actividades.csv",
                BytesIO(csv_content.encode("utf-8")),
                "text/csv",
            )
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["procesadas"] == 3
    assert data["creadas"] == 2
    assert len(data["errores"]) == 1