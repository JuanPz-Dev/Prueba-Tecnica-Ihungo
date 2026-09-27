def test_obtener_asociados(client):
    response = client.get("/api/asociados/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_asociado(client):
    response = client.post(
        "/api/asociados/",
        json={
            "identificacion": "1001",
            "nombre": "Juan",
            "apellidos": "Perez",
            "email": "juan@test.com",
            "ciudad": "Cartagena",
            "password": "123456",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "juan@test.com"
    assert data["nombre"] == "Juan"
    assert data["rol"] == "ASOCIADO"


def test_no_permite_email_duplicado(client):
    datos = {
        "identificacion": "1002",
        "nombre": "Pedro",
        "apellidos": "Gomez",
        "email": "duplicado@test.com",
        "ciudad": "Cartagena",
        "password": "123456",
    }

    primera = client.post("/api/asociados/", json=datos)
    segunda = client.post("/api/asociados/", json=datos)

    assert primera.status_code == 201
    assert segunda.status_code == 409