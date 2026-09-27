from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    identificacion: Mapped[str] = mapped_column(String(50), unique=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    ciudad: Mapped[str] = mapped_column(String(100))
    rol: Mapped[str] = mapped_column(String(20))

    actividades_asignadas = relationship(
        "Actividad",
        foreign_keys="Actividad.asociado_id",
        back_populates="asociado",
    )

    actividades_creadas = relationship(
        "Actividad",
        foreign_keys="Actividad.creador_id",
        back_populates="creador",
    )