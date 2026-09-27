from datetime import datetime

from pydantic import BaseModel


class ActividadCreate(BaseModel):
    tipo_actividad: str
    descripcion: str | None = None
    fecha_inicio: datetime
    fecha_fin: datetime
    asociado_id: int

class ActividadUpdate(BaseModel):
    tipo_actividad: str | None = None
    descripcion: str | None = None
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    asociado_id: int | None = None

class ActividadResponse(BaseModel):
    id: int
    tipo_actividad: str
    descripcion: str | None
    fecha_inicio: datetime
    fecha_fin: datetime
    asociado_id: int
    creador_id: int

    model_config = {"from_attributes": True}