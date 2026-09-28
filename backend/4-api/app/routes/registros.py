from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.registro import RegistroCreate, RegistroResponse
from app.services.registro_service import crear_solicitud

router = APIRouter(
    prefix="/api/registro",
    tags=["Registro"],
)

@router.post("/",response_model=RegistroResponse,status_code=201,)
def registrar_solicitud(
    datos: RegistroCreate,
    db: Session = Depends(get_db),
):
    return crear_solicitud(
        db,
        datos.nombre,
        datos.email,
    )