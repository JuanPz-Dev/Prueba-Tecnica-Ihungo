# Backend 2 — Refactor

## Descripción

Refactorización de un script encargado de procesar un archivo Excel, analizar el sentimiento de los textos mediante un proveedor externo y registrar los resultados en el archivo de salida.

El refactor busca mejorar la separación de responsabilidades, configuración, manejo de errores, testabilidad y mantenibilidad del código.

## Requisitos

- Python 3.13+
- Entorno virtual recomendado

## Instalación

Crear el entorno virtual:

python -m venv .venv

Activarlo en Windows PowerShell:

.venv\Scripts\Activate.ps1

Instalar las dependencias del proyecto:

pip install -r requirements.txt


## Configuración

La clave de acceso al proveedor de análisis de sentimientos se configura mediante la variable de entorno:

PARALLELDOTS_API_KEY

En Windows PowerShell:

$env:PARALLELDOTS_API_KEY="tu-api-key"

> **Importante:** no se deben incluir claves, tokens o credenciales directamente en el código ni subirlas al repositorio.

## Ejecución

La aplicación recibe mediante argumentos de línea de comandos:

- `--input`: archivo Excel de entrada.
- `--output`: archivo Excel de salida.
- `--sheet`: nombre de la hoja que se