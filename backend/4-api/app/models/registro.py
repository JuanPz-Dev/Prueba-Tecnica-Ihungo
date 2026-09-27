from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SolicitudRegistro(Base):
    __tablename__ = "solicitudes_registro"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))
    estado: Mapped[str] = mapped_column(String(20), default="PENDIENTE")
    fecha_solicitud: Mapped[datetime] = mapped_column(default=datetime.utcnow)