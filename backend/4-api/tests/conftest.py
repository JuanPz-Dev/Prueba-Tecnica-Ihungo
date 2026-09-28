import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.database import Base, get_db
from app.main import app
from app.models.actividad import Actividad
from app.models.registro import SolicitudRegistro
from app.models.usuario import Usuario


SQLALCHEMY_DATABASE_URL = "sqlite://"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    usuario = Usuario(
        identificacion="123456",
        nombre="Admin",
        apellidos="Prueba",
        email="admin@test.com",
        password_hash=hash_password("123456"),
        ciudad="Cartagena",
        rol="ADMIN",
    )

    asociado = Usuario(
        identificacion="654321",
        nombre="Asociado",
        apellidos="Prueba",
        email="asociado@test.com",
        password_hash=hash_password("123456"),
        ciudad="Cartagena",
        rol="ASOCIADO",
    )

    otro_asociado = Usuario(
        identificacion="789012",
        nombre="Otro",
        apellidos="Asociado",
        email="otro@test.com",
        password_hash=hash_password("123456"),
        ciudad="Cartagena",
        rol="ASOCIADO",
    )

    db.add(usuario)
    db.add(asociado)
    db.add(otro_asociado)
    db.commit()

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)