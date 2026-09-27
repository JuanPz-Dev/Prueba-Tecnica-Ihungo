def test_login_devuelve_tokens(client):
    response = client.post(
        "/api/auth/token/",
        json={
            "email": "admin@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access" in data
    assert "refresh" in data


def test_login_rechaza_credenciales_invalidas(client):
    response = client.post(
        "/api/auth/token/",
        json={
            "email": "noexiste@test.com",
            "password": "incorrecta",
        },
    )

    assert response.status_code == 401


def test_refresh_devuelve_nuevo_access_token(client):
    login = client.post(
        "/api/auth/token/",
        json={
            "email": "admin@test.com",
            "password": "123456",
        },
    )

    assert login.status_code == 200

    refresh = login.json()["refresh"]

    response = client.post(
        "/api/auth/token/refresh/",
        json={"refresh": refresh},
    )

    assert response.status_code == 200
    assert "access" in response.json()