from pydantic import BaseModel, EmailStr


class AsociadoCreate(BaseModel):
    identificacion: str
    nombre: str
    apellidos: str
    email: EmailStr
    ciudad: str
    password: str


class AsociadoResponse(BaseModel):
    id: int
    identificacion: str
    nombre: str
    apellidos: str
    email: EmailStr
    ciudad: str
    rol: str

    model_config = {"from_attributes": True}

class UsuarioResponse(BaseModel):
    id: int
    identificacion: str
    nombre: str
    apellidos: str
    email: EmailStr
    ciudad: str
    rol: str

    model_config = {"from_attributes": True}