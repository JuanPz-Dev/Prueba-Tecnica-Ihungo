#Alembic necesita conocer nuestros modelos.

from app.models.actividad import Actividad
from app.models.registro import SolicitudRegistro
from app.models.usuario import Usuario

__all__ = ["Usuario", "Actividad", "SolicitudRegistro"]