from datetime import datetime

from pydantic import BaseModel, EmailStr

class RegistroCreate(BaseModel):
    nombre: str
    email: EmailStr

class RegistroResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    estado: str
    fecha_solicitud: datetime
    model_config = {"from_attributes": True}