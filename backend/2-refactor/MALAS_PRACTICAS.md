# Backend 2 - Refactorización de código

### 1. Credencial incluida en el código
En el codigo hay:
`key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'`
La api key no deberia formar parte del codigo fuente

**Práctica vulnerada:** Manejo seguro de credenciales y configuración.

**Impacto:** Existe riesgo de exponer credenciales si el repositorio se comparte o se publica.

**Mejora propuesta:** Utilizar variables de entorno para almacenar la API Key y evitar que la credencial quede directamente dentro del código fuente.

### 2. Acoplamiento directo con ParallelDots

En los import vemos:

`import paralleldots` y en el codigo
`paralleldots.set_api_key(self.key)`
`output_sentiment = paralleldots.sentiment(...)`

No esta mal, pero es mala practica porque la clase  Analytics depende directamente de la libreria paralleldots

**Práctica vulnerada:** Alto acoplamiento entre la lógica de procesamiento y un proveedor externo.

**Impacto:** Si en el futuro se quiere cambiar ParallelDots por otro proveedor de análisis de sentimiento, sería necesario modificar la lógica de Analytics tambien.

**Mejora propuesta:** Crear una interfaz mediante Protocol que defina el comportamiento necesario para analizar un texto. ParallelDots implementaría esa interfaz, permitiendo cambiar de proveedor sin modificar la lógica principal del procesamiento.

### 3. Demasiadas responsabilidades

La clase Analytics realiza varias tareas diferentes. Se encarga de comprobar el archivo, configurar el proveedor, abrir el Excel, leer los datos, llamar al servicio de sentimiento, escribir los resultados y guardar el archivo.

En la clase:
`class Analytics:`
y principalmente en el método:
`def process_file(self):`

**Práctica vulnerada:** No se estaria aplicando la practica Principio de Responsabilidad Única de los principios SOLID

**Impacto:** La clase se vuelve más difícil de mantener, modificar y probar, porque cualquier cambio relacionado con alguna de estas tareas puede afectar al resto.

**Mejora propuesta:** Separar las responsabilidades en diferentes componentes. Por ejemplo, tener un componente para procesar el Excel, otro para comunicarse con el proveedor de sentimiento y otro para manejar los argumentos de ejecución.

### 4. Uso de print() en lugar de logging

Ubicación En:

`print(sheet.cell(row, 3).value)` También en: `print('Not existe file.')` y: `print("Select a file.")`

Se utiliza print() para mostrar información de ejecución y reportar situaciones de error o advertencia. Esto dificulta el manejo y seguimiento de los eventos de la aplicación, ya que los mensajes no tienen niveles de severidad ni pueden gestionarse o almacenarse de forma adecuada.

**Práctica vulnerada:** Uso inadecuado de la salida estándar para registrar eventos de la aplicación.

**Impacto:** No permite manejar de manera adecuada los diferentes niveles de información, advertencias y errores. También dificulta el seguimiento de lo que ocurre cuando la aplicación se ejecuta en otro entorno.

**Mejora propuesta:** Utilizar el módulo logging de Python para registrar información, advertencias y errores.

### 5. Uso de una espera

En el codigo se visualiza esta linea `time.sleep(10)` es una mala practica porque el programa realiza una espera fija de 10 segundos después de cada solicitud al servicio de análisis de sentimiento.

**Práctica vulnerada:** Manejo inadecuado de esperas y reintentos ante servicios externos.

**Impacto:** El programa siempre espera 10 segundos, incluso cuando la solicitud fue exitosa. Además, esta espera no diferencia entre una operación normal y un error temporal o un límite de tasa del proveedor.

**Mejora propuesta:** Implementar un mecanismo de reintentos con backoff. De esta manera, solamente se espera cuando ocurre un error recuperable o un límite de tasa, y el tiempo entre reintentos puede aumentar progresivamente.

### 6. Falta de manejo de errores

`output_sentiment = paralleldots.sentiment(str(sheetcell(row, 3).value))`

La llamada al servicio externo no tiene un manejo específico de excepciones.El código solamente comprueba posteriormente si existe la clave sentiment.

`if 'sentiment' in output_sentiment`

**Práctica vulnerada:** Falta de manejo adecuado de errores en una dependencia externa.

**Impacto:** Un error de conexión, una excepción de la librería o un problema temporal del proveedor puede interrumpir el procesamiento del archivo.

**Mejora propuesta:** Agregar manejo de excepciones y reintentos para errores recuperables.

### 7. Uso de sys.argv para manejar los argumentos
En: `if __name__ == '__main__':if len(sys.argv) > 1:`

El programa utiliza directamente sys.argv para recibir los argumentos de ejecución. Esto solamente permite manejar los argumentos mediante posiciones y no proporciona una descripción clara de qué representa cada uno.

**Práctica vulnerada:** Manejo poco estructurado de los argumentos de línea de comandos.

**Impacto:** La ejecución del programa es menos clara y resulta más difícil agregar nuevas opciones de configuración.

**Mejora propuesta:** Utilizar argparse para definir argumentos con nombres y descripciones. El programa deberá permitir configurar el archivo de entrada, archivo de salida, hoja y columna de texto.

### 8. Columnas del Excel definidas directamente en el código

`sheet.cell(row, 3).value`  y 
`sheet.cell(1, 4).value = 'NEGATIVO'`
`sheet.cell(1, 5).value = 'NEUTRAL'` 
`sheet.cell(1, 6).value = 'POSITIVO'`

El programa tiene posiciones de columnas definidas directamente en el código.
La columna 3 se utiliza como columna de texto y las columnas 4, 5 y 6 se utilizan para los resultados.

**Práctica vulnerada:** Configuración rígida dentro del código.

**Impacto:** El programa depende de una estructura específica del archivo Excel. Si la columna del texto cambia, es necesario modificar el código.

**Mejora propuesta:** Permitir que la columna de texto sea configurada mediante un argumento de línea de comandos. También se debe permitir seleccionar la hoja del Excel y definir el archivo de salida.

### 9. El rango de filas está definido directamente en el código
En: `for row in range(2, 4):`
El programa solamente procesa las filas 2 y 3, aunque anteriormente obtiene el número máximo de filas mediante:
`max_row = sheet.max_row`
El valor de max_row incluso se obtiene pero posteriormente no se utiliza en el metodo.

**Práctica vulnerada:** Código rígido y variable sin utilizar.

**Impacto:** El programa no procesa todas las filas disponibles del Excel y su comportamiento depende de un rango escrito directamente en el código.

**Mejora propuesta:** Utilizar el número real de filas del archivo para determinar qué registros procesar y eliminar variables que no sean necesarias.

### 10. Configuración del proveedor repetida innecesariamente
En process_file(): `paralleldots.set_api_key(self.key)` se ejecuta antes de procesar las filas. Después, dentro del for, vuelve a ejecutarse: `paralleldots.set_api_key(self.key)`

La API Key se configura nuevamente para cada fila procesada.

**Práctica vulnerada:** Código repetitivo y configuración innecesaria dentro del ciclo.

**Impacto:** Se realizan operaciones que no son necesarias para cada registro y se mezcla la configuración del proveedor con el procesamiento de cada fila.

**Mejora propuesta:** Encapsular la configuración del proveedor en una clase independiente y realizarla una sola vez al crear el proveedor de sentimiento.