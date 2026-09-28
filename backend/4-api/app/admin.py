from sqladmin import Admin, ModelView

from app.database import engine
from app.models.actividad import Actividad
from app.models.registro import SolicitudRegistro
from app.models.usuario import Usuario

class UsuarioAdmin(ModelView, model=Usuario):
    name = "Usuario"
    name_plural = "Usuarios"

    column_list = [
        Usuario.id,
        Usuario.identificacion,
        Usuario.nombre,
        Usuario.apellidos,
        Usuario.email,
        Usuario.ciudad,
        Usuario.rol,
    ]

class ActividadAdmin(ModelView, model=Actividad):
    name = "Actividad"
    name_plural = "Actividades"

    column_list = [
        Actividad.id,
        Actividad.tipo_actividad,
        Actividad.fecha_inicio,
        Actividad.fecha_fin,
        Actividad.asociado_id,
        Actividad.creador_id,
    ]

class SolicitudRegistroAdmin(ModelView, model=SolicitudRegistro):
    name = "Solicitud de registro"
    name_plural = "Solicitudes de registro"

    column_list = [
        SolicitudRegistro.id,
        SolicitudRegistro.nombre,
        SolicitudRegistro.email,
        SolicitudRegistro.estado,
        SolicitudRegistro.fecha_solicitud,
    ]

def configurar_admin(app):
    admin = Admin(app, engine)

    admin.add_view(UsuarioAdmin)
    admin.add_view(ActividadAdmin)
    admin.add_view(SolicitudRegistroAdmin)