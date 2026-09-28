# Backend 4 — API REST de asignación de actividades

API REST desarrollada como parte de la prueba técnica de Ihungo.

El sistema permite administrar asociados, registrar actividades, realizar autenticación mediante JWT, consultar actividades según permisos y realizar cargas masivas mediante archivos CSV.

## Tecnologías utilizadas

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* SQLAdmin
* Pydantic
* JWT
* pytest
* pytest-cov
* Docker
* Docker Compose
* GitLab CI

## Experiencia con la tecnología

Mi experiencia principal en backend es con **Java y Spring Boot**.

FastAPI no era la tecnología con la que tenía mayor experiencia al comenzar esta prueba. El enunciado permitía elegir entre **Django REST Framework y FastAPI**, por lo que elegí FastAPI para desarrollar la solución.

Durante la prueba tuve que aprender y aplicar conceptos propios de FastAPI, principalmente:

* Definición de rutas.
* Inyección de dependencias.
* Validación con Pydantic.
* Autenticación mediante dependencias.
* Integración con SQLAlchemy.
* Documentación automática mediante OpenAPI.
* Pruebas con TestClient.

Aunque la implementación utiliza FastAPI, los conceptos de backend utilizados son similares a los que he trabajado anteriormente con Java y Spring Boot:

* Arquitectura por capas.
* APIs REST.
* Separación de responsabilidades.
* ORM y acceso a bases de datos.
* Autenticación y autorización.
* Migraciones.
* Pruebas automatizadas.
* Docker.

## ¿Por qué FastAPI?

El enunciado de la prueba permitía elegir entre Django REST Framework y FastAPI.

Elegí FastAPI porque para el alcance de esta prueba permite construir una API REST con una cantidad relativamente pequeña de configuración y proporciona funcionalidades útiles de forma integrada:

* Documentación OpenAPI/Swagger.
* Validación de datos mediante Pydantic.
* Inyección de dependencias.
* Integración con SQLAlchemy.
* `TestClient` para realizar pruebas de los endpoints.

Mi objetivo fue mantener la implementación sencilla y enfocada en los requerimientos de la prueba, en lugar de agregar componentes innecesarios.

## Arquitectura

La aplicación utiliza una separación sencilla por capas:

```text
Endpoint / Route
       ↓
Service
       ↓
Repository
       ↓
Base de datos
```

Las responsabilidades principales son:

* **Routes:** reciben las peticiones HTTP y devuelven las respuestas.
* **Services:** contienen las reglas y lógica de negocio.
* **Repositories:** encapsulan las operaciones relacionadas con la persistencia.
* **Models:** representan las entidades de la base de datos.
* **Schemas:** representan y validan los datos de entrada y salida.

La intención es evitar colocar la lógica de negocio directamente dentro de los endpoints.

## Modelo de datos

El sistema utiliza tres modelos principales.

### Usuario

Representa tanto a administradores como asociados.

Campos principales:

* identificación
* nombre
* apellidos
* email
* contraseña
* ciudad
* rol

Los roles utilizados son:

```text
ADMIN
ASOCIADO
```

### Actividad

Representa una actividad asignada a un asociado.

Campos principales:

* tipo de actividad
* descripción
* fecha y hora de inicio
* fecha y hora de fin
* asociado
* creador

### Solicitud de registro

Permite que una persona solicite su registro.

Campos principales:

* nombre
* email
* estado
* fecha de solicitud

Estados utilizados:

```text
PENDIENTE
APROBADA
RECHAZADA
```

Las migraciones de la base de datos se manejan mediante **Alembic**.

## Autenticación

La API utiliza JWT para la autenticación.

El usuario inicia sesión utilizando su correo electrónico y contraseña.

La API genera:

* Access token.
* Refresh token.

El access token se utiliza para acceder a los endpoints protegidos.

## Endpoints principales

### Autenticación

```http
POST /api/auth/token/
POST /api/auth/token/refresh/
```

### Usuario autenticado

```http
GET /api/usuarios/me/
```

Permite consultar la información del usuario que realizó la autenticación.

### Registro público

```http
POST /api/registro/
```

Permite enviar una solicitud pública de registro.

### Asociados

```http
GET /api/asociados/
POST /api/asociados/
```

### Actividades

```http
GET /api/actividades/?desde=&hasta=
POST /api/actividades/
PATCH /api/actividades/{id}/
DELETE /api/actividades/{id}/
```

### Carga masiva

```http
POST /api/carga-masiva/asociados/
POST /api/carga-masiva/actividades/
```

La implementación utiliza archivos CSV.

### Health check

```http
GET /api/health/
```

Respuesta:

```json
{
  "status": "ok"
}
```

## Reglas de negocio

### Validación de fechas

La fecha de finalización debe ser posterior a la fecha de inicio:

```text
fecha_fin > fecha_inicio
```

### Solapamiento de actividades

Un asociado no puede tener dos actividades que se crucen en el mismo horario.

La validación se realiza antes de crear o modificar una actividad.

### Permisos

Los administradores pueden gestionar las actividades.

Los asociados solamente pueden modificar o eliminar actividades propias que todavía no hayan pasado.

Las actividades pasadas quedan disponibles únicamente para consulta.

### Visibilidad

Un usuario que no sea administrador solamente puede visualizar actividades:

* creadas por él, o
* relacionadas con él como asociado.

## Panel administrativo

Se utiliza **SQLAdmin** para proporcionar un panel administrativo.

Desde el panel se pueden administrar:

* Usuarios.
* Actividades.
* Solicitudes de registro.

Las solicitudes de registro pueden ser gestionadas desde el panel cambiando su estado.

## Carga masiva

La API permite cargar asociados y actividades mediante archivos CSV.

El procesamiento se realiza fila por fila.

Si una fila contiene un error, esa fila se registra como error y el procesamiento continúa con las siguientes filas válidas.

Ejemplo de respuesta:

```json
{
  "procesadas": 3,
  "creadas": 2,
  "errores": [
    {
      "fila": 3,
      "error": "El asociado ya existe."
    }
  ]
}
```

## CSV de asociados

Ejemplo:

```csv
identificacion,nombre,apellidos,email,ciudad,password
1001,Juan,Perez,juan@example.com,Cartagena,123456
1002,Ana,Gomez,ana@example.com,Barranquilla,123456
```

## CSV de actividades

Ejemplo:

```csv
tipo_actividad,descripcion,fecha_inicio,fecha_fin,asociado_id
Capacitación,Capacitación inicial,2026-09-28T08:00:00,2026-09-28T10:00:00,2
Reunión,Reunión de seguimiento,2026-09-28T14:00:00,2026-09-28T15:00:00,2
```

## Ejecución con Docker

La forma recomendada de ejecutar el proyecto es utilizando Docker Compose.

Desde la carpeta `backend/4-api`:

```bash
docker compose up --build
```

Esto levanta:

* PostgreSQL.
* La API FastAPI.
* Las migraciones de Alembic.

La API estará disponible en:

```text
http://localhost:8000
```

La documentación interactiva estará disponible en:

```text
http://localhost:8000/docs
```

También se puede consultar:

```text
http://localhost:8000/redoc
```

Para detener los servicios:

```bash
docker compose down
```

## Variables de entorno

Se proporciona un archivo `.env.example`.

Ejemplo:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ihungo
SECRET_KEY=change-this-secret-key
```

El archivo `.env` se encuentra incluido en `.gitignore y no se versiona.

Cuando la aplicación se ejecuta mediante Docker Compose, la API utiliza el servicio de PostgreSQL definido en `docker-compose.yml`.

## Ejecución de pruebas

Las pruebas automatizadas utilizan pytest.

Desde `backend/4-api`:

```bash
pytest -v
```

Para ejecutar las pruebas con cobertura:

```bash
pytest --cov=app --cov-report=term-missing
```

Durante el desarrollo se obtuvo una cobertura del:

```text
88%
```

El requisito solicitado para la prueba es una cobertura mínima del 80%.

## Pruebas y TDD

Para las principales reglas de negocio se utilizó un enfoque orientado a pruebas.

Se crearon pruebas para:

* Creación de actividades.
* Consulta de actividades.
* Actualización de actividades.
* Eliminación de actividades.
* Permisos de asociados.
* Actividades pasadas.
* Solapamiento de horarios.
* Creación de asociados.
* Correos duplicados.
* Autenticación.
* Registro público.
* Cargas masivas.

El historial de Git muestra commits separados para pruebas e implementación.

## Principios SOLID

La implementación intenta aplicar los principios SOLID de acuerdo con el tamaño y alcance de la prueba.

### Single Responsibility

Las responsabilidades están separadas entre diferentes módulos:

* `routes`: comunicación HTTP.
* `services`: lógica de negocio.
* `repositories`: persistencia.
* `schemas`: validación y representación de datos.

### Open/Closed

La separación entre servicios y repositorios permite modificar parte de la implementación sin colocar la lógica de persistencia directamente en los endpoints.

### Liskov Substitution

No se utilizan jerarquías complejas de clases. Para esta prueba se prefirió mantener una estructura sencilla y evitar herencia innecesaria.

### Interface Segregation

No se crearon interfaces artificiales únicamente para cumplir este principio. Se mantuvieron módulos pequeños y responsabilidades separadas.

### Dependency Inversion

Se utiliza la inyección de dependencias proporcionada por FastAPI para elementos como:

* Sesión de base de datos.
* Usuario autenticado.

## Integración continua

El repositorio incluye un archivo `.gitlab-ci.yml` en la raíz del proyecto.

El pipeline tiene tres etapas:

```text
lint
  ↓
test
  ↓
build
```

### Lint

Se utiliza Ruff para revisar el código.

### Tests

Se ejecutan las pruebas automatizadas y se comprueba que la cobertura sea como mínimo del 80%.

### Build

Se construye la imagen Docker del backend.

El pipeline está configurado para ejecutarse cuando se realizan cambios en el repositorio.

## Decisiones y limitaciones

Esta implementación busca cumplir los requerimientos de la prueba manteniendo una arquitectura que pueda entenderse y mantenerse fácilmente.

No se intentó implementar una arquitectura empresarial completa ni agregar componentes que no fueran necesarios para los requerimientos.

Por ejemplo, se utiliza una única tabla `usuarios` para representar administradores y asociados mediante un campo `rol`.

La carga masiva implementada utiliza CSV. La estructura actual podría extenderse posteriormente para soportar otros formatos.

## Aprendizajes durante la prueba

Esta prueba también tuvo como objetivo aprender una tecnología de backend diferente a la utilizada habitualmente.

Mi experiencia previa está principalmente relacionada con **Java y Spring Boot**, por lo que durante el desarrollo tuve que familiarizarme con:

* FastAPI.
* Pydantic.
* SQLAlchemy.
* SQLAdmin.
* Dependencias de FastAPI.
* Alembic.
* Manejo de archivos mediante `UploadFile`.

Los conceptos de arquitectura, APIs REST, autenticación, persistencia, pruebas y Docker fueron aplicados tomando como referencia conocimientos previos de desarrollo backend.

## Estado del proyecto

Actualmente la implementación incluye:

* API REST con FastAPI.
* PostgreSQL.
* SQLAlchemy.
* Alembic.
* JWT con access y refresh token.
* Roles de administrador y asociado.
* Gestión de actividades.
* Gestión de asociados.
* Registro público.
* Panel administrativo.
* Carga masiva mediante CSV.
* Validación de fechas.
* Validación de solapamiento.
* Control de permisos.
* Pruebas automatizadas.
* Cobertura superior al 80%.
* Docker.
* Docker Compose.
* GitLab CI.
* Documentación OpenAPI.
