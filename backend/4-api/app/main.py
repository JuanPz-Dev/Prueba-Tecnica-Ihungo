from fastapi import FastAPI

from app.routes.actividades import router as actividades_router
from app.routes.asociados import router as asociados_router
from app.routes.auth import router as auth_router
from app.routes.usuarios import router as usuarios_router
from app.routes.registros import router as registros_router
from app.admin import configurar_admin
from app.routes.carga_masiva import router as carga_masiva_router

app = FastAPI(
    title="API de asignación de actividades",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(asociados_router)
app.include_router(actividades_router)
app.include_router(usuarios_router)
app.include_router(registros_router)
configurar_admin(app)
app.include_router(carga_masiva_router)


@app.get("/api/health/")
def health():
    return {"status": "ok"}