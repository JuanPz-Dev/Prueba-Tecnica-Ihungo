from datetime import datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Actividad(Base):
    __tablename__ = "actividades"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo_actividad: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_inicio: Mapped[datetime]
    fecha_fin: Mapped[datetime]

    asociado_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    creador_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    asociado = relationship(
        "Usuario",
        foreign_keys=[asociado_id],
        back_populates="actividades_asignadas",
    )

    creador = relationship(
        "Usuario",
        foreign_keys=[creador_id],
        back_populates="actividades_creadas",
    )