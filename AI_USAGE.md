## Backend 2 — Refactorización de código

ChatGPT fue utilizado como apoyo para:

- Proponer una estructura para separar responsabilidades.
- Comprender el uso de `Protocol` para desacoplar el proveedor de análisis de sentimiento.
- Orientar la configuración mediante variables de entorno y argumentos CLI.
- Implementar y entender el uso de `argparse`.
- Orientar el manejo de errores y reintentos con backoff.
- Orientar la escritura de pruebas con `pytest` utilizando dobles de prueba.
- Interpretar errores de `ruff`, `mypy` y problemas de cobertura.
- Revisar los resultados de las pruebas y corregir los errores encontrados.

### Aprendizaje durante el ejercicio

Este ejercicio fue también una oportunidad para familiarizarme por primera vez con la escritura y ejecución de pruebas automatizadas utilizando pytest. Durante el desarrollo utilicé ChatGPT como apoyo para comprender conceptos como dobles de prueba, monkeypatch, cobertura de código y la interpretación de errores de las herramientas de calidad.

Las pruebas fueron ejecutadas y verificadas localmente, y los errores encontrados durante su ejecución fueron corregidos antes de finalizar el ejercicio.

### Decisiones y correcciones

El código fue ejecutado y validado localmente durante el desarrollo.

Se realizaron correcciones a partir de los resultados reales obtenidos con las herramientas de calidad. Por ejemplo, durante la ejecución de `mypy` se detectaron problemas relacionados con:

- La identificación del paquete `sentiment_analysis`.
- Los tipos de la dependencia `openpyxl`.
- La ausencia de type stubs de `paralleldots`.
- Un posible camino de ejecución sin `return` en el proveedor de sentimiento.

Estos problemas fueron revisados y corregidos antes de finalizar el ejercicio.

También se verificó que las pruebas no realizaran llamadas al servicio real de análisis de sentimiento.

### Validaciones realizadas

El ejercicio fue validado mediante:

- `pytest`
- `pytest-cov`
- `ruff`
- `mypy`

### Backend 4

Antes de realizar esta prueba **no conocía el enfoque TDD (Test-Driven Development)**. Durante el desarrollo descubrí este concepto y lo utilicé como parte del proceso de implementación.

Consulté con IA qué significa TDD y cómo podía aplicarlo a las reglas de negocio de esta API.

Entendí el ciclo básico como:

```text
RED → GREEN → REFACTOR
```

Es decir:

1. **RED:** escribir primero una prueba que represente el comportamiento esperado y comprobar que falla.
2. **GREEN:** implementar la solución mínima necesaria para que la prueba pase.
3. **REFACTOR:** mejorar la implementación manteniendo las pruebas pasando.

No apliqué TDD de forma estricta a absolutamente todo el proyecto, porque descubrí esta metodología durante el desarrollo y el tiempo de la prueba era limitado.

Sin embargo, sí la utilicé especialmente en funcionalidades donde existían reglas de negocio importantes, como:

* Permisos de asociados sobre actividades.
* Modificación de actividades futuras.
* Restricción de modificación de actividades pasadas.
* Eliminación de actividades.
* Carga masiva de asociados.
* Carga masiva de actividades.
* Manejo de actividades solapadas.

Por ejemplo, para los permisos de actividades primero definí pruebas que representaban situaciones como:

```text
Un asociado puede modificar una actividad futura.
Un asociado no puede modificar una actividad pasada.
Un asociado puede eliminar una actividad futura.
Un asociado no puede eliminar una actividad pasada.
Un asociado no puede consultar actividades de otro asociado.
```

Inicialmente algunas de estas pruebas fallaron porque la implementación todavía no cumplía las reglas. Posteriormente modifiqué la lógica de servicios y endpoints hasta conseguir que todas las pruebas pasaran.

También utilicé este proceso para la carga masiva: primero se definieron pruebas para comprobar que las filas válidas fueran procesadas y que una fila inválida no impidiera procesar las demás.

### Lo que aprendí sobre TDD

La principal utilidad que encontré en TDD fue que permite convertir los requerimientos en comportamientos verificables antes de centrarse completamente en la implementación.

Antes de conocer este enfoque, normalmente pensaba primero en escribir el código y después en crear las pruebas. Durante esta prueba entendí que, para reglas de negocio, escribir primero el comportamiento esperado puede ayudar a detectar errores de lógica y a definir mejor qué debe hacer el sistema.

Todavía no considero que tenga dominio de TDD. Fue un concepto que aprendí durante esta prueba y que quiero seguir practicando en futuros proyectos.

### Uso de IA durante el aprendizaje de TDD

La IA se utilizó como apoyo para:

* Entender qué es TDD.
* Comprender el ciclo RED → GREEN → REFACTOR.
* Identificar qué comportamientos podían convertirse en pruebas.
* Revisar la estructura de algunos tests.
* Interpretar los fallos obtenidos al ejecutar las pruebas.

Las pruebas fueron ejecutadas localmente y los resultados se utilizaron para corregir la implementación.
