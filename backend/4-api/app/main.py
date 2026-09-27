from fastapi import FastAPI

from app.routes.auth import router as auth_router

app = FastAPI(
    title="API de asignación de actividades",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/api/health/")
def health():
    return {"status": "ok"}