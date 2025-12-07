# Resumen de Cambios y Mejoras del Proyecto

Este documento detalla las correcciones, mejoras y funcionalidades implementadas en el proyecto "Intranet La Ganga", abarcando desde la configuración del entorno hasta la lógica de la aplicación en el backend y frontend.

---

## 1. Entorno y Configuración

Se realizaron cambios críticos para asegurar un entorno de desarrollo estable y funcional, tanto de forma local como con Docker.

### 1.1. Configuración de Docker para Transacciones en MongoDB

*   **Problema:** El código de la aplicación requería el uso de transacciones en MongoDB para operaciones complejas (como la creación de departamentos con links asociados). Sin embargo, la configuración por defecto de MongoDB en Docker (`image: mongo:latest`) no soporta transacciones, lo que provocaba un error `pymongo.errors.OperationFailure`.
*   **Solución:** Se modificó el archivo `docker-compose.yml` para configurar la instancia de MongoDB como un **"replica set"** de un solo miembro.
    *   Se añadió un `command` al servicio `mongodb` para iniciarlo con la opción `--replSet rs0`.
    *   Se creó un nuevo servicio `mongo-setup` que se ejecuta una sola vez para inicializar el replica set con el comando `rs.initiate()`.
    *   Se actualizó la variable de entorno `MONGO_DATABASE_URL` en el archivo `.env` para incluir el parámetro `?replicaSet=rs0`, permitiendo que la aplicación se conecte correctamente.

### 1.2. Gestión de Dependencias de Python

*   **Problema:** La aplicación sufría de errores extraños y aparentemente ilógicos (`AttributeError`, `NameError: name 'unicode' is not defined`), causados por un archivo `requirements.txt` que contenía dependencias conflictivas o versiones antiguas no compatibles con Python 3.
*   **Solución:** Se reemplazó el contenido de `Backend/requirements.txt` por una lista limpia de dependencias de alto nivel (`fastapi`, `passlib`, `python-slugify`, etc.), permitiendo que `pip` resolviera e instalara las versiones correctas y compatibles de todas las sub-dependencias, eliminando los conflictos.

### 1.3. Configuración de Red (Local vs. Docker)

*   **Problema:** La aplicación fallaba al hacer peticiones `fetch` dependiendo del contexto (servidor de Astro a servidor de backend, navegador a backend). Los errores incluían `ECONNREFUSED ::1:8000` y `Failed to parse URL`.
*   **Solución:** Se estandarizó el uso de variables de entorno para las URLs del backend.
    *   Se estableció `URLBACK=http://backend:8000` para la comunicación interna de Docker (usada en el renderizado de Astro en el servidor).
    *   Se estableció `PUBLIC_BACKEND_URL=http://127.0.0.1:8000` para ser usada por el código que se ejecuta en el navegador del cliente y para construir las URLs de las imágenes que se guardan en la base de datos.
    *   Se reemplazó el uso de `localhost` por `127.0.0.1` para evitar problemas de resolución de nombres entre IPv4 y IPv6.

---

## 2. Backend (API)

Se corrigieron múltiples bugs y se implementaron nuevas funcionalidades para asegurar la integridad de los datos y el comportamiento esperado.

### 2.1. Lógica de Transacciones en `Dep_mongo.py`

*   **Funcionalidad:** Para cumplir con los requisitos de la presentación de base de datos, se mantuvo la lógica de transacciones en el endpoint de creación de departamentos (`crear_departamento`).
*   **Implementación:** Se utiliza `async with await client.start_session() as session:` y `async with session.start_transaction():` para envolver las operaciones de escritura en la base de datos.
    *   Primero, se inserta el documento del nuevo departamento en la colección `dep`.
    *   Si se proporciona un link, se inserta el documento del link en la colección `linkdep`.
*   **Garantía:** Este bloque transaccional asegura que ambas operaciones (crear departamento y crear su link inicial) se completen con éxito. Si alguna de las dos falla, ambas se revierten (`rollback`), manteniendo la base de datos en un estado consistente.

### 2.2. Solución al Problema del `id` Indefinido (Undefined)

*   **Problema:** Múltiples endpoints (`/cards`, `/noticias`, etc.) devolvían una lista de objetos donde el campo `id` no existía, a pesar de que el `_id` sí venía de la base de datos. Esto causaba que los botones de "Editar" y "Eliminar" en el frontend no funcionaran.
*   **Causa:** Un conflicto entre la serialización manual de los datos y el uso del decorador `response_model` en FastAPI, que no estaba convirtiendo correctamente el `_id` a `id`.
*   **Solución:** Se eliminó el `response_model` de los endpoints afectados y se construyó la respuesta JSON manualmente, asegurando la creación explícita del campo `id`:
    ```python
    # Ejemplo en obtener_departamentos_cards
    lista_departamentos = []
    async for dep in cursor:
        lista_departamentos.append({
            "id": str(dep["_id"]),  # Conversión manual de _id a id
            "titulo": dep.get("titulo"),
            # ... otros campos
        })
    return lista_departamentos
    ```

### 2.3. Implementación de Sistema de Logs

*   **Objetivo:** Registrar las acciones de creación, edición y eliminación para las entidades principales (departamentos, noticias, links).
*   **Implementación:**
    1.  **Modelo:** Se revisó y ajustó el modelo `Log` en `modelLog_mongo.py` para que los IDs se manejaran como `string`, manteniendo la consistencia con los "hacks" temporales.
    2.  **Utilidad:** Se creó un archivo `Backend/utils/logger.py` con una función asíncrona `create_log_entry`. Esta función recibe los detalles de la acción y crea un nuevo documento en la colección `logs`.
    3.  **Integración:** Se importó y llamó a `create_log_entry` desde todos los endpoints relevantes después de una operación de escritura exitosa.
        *   **Nota:** En los endpoints donde se quitó la seguridad por el bug de JWT (`editar-dep`, etc.), el usuario se registra como `"Anónimo"`.

### 2.4. Implementación de Endpoints Faltantes

*   **Problema:** La funcionalidad de edición de departamentos estaba incompleta porque no existían los endpoints en el backend.
*   **Solución:** Se implementaron los siguientes endpoints en `Dep_mongo.py`:
    *   `GET /id/{id}`: Para obtener los datos de un departamento específico para la página de edición.
    *   `PUT /editar-dep/{id}/`: Para guardar los cambios de un departamento.
    *   `POST /{depId}/agregar-link`: Para añadir un nuevo link a un departamento.
    *   `DELETE /link/{linkId}`: Para eliminar un link específico.
    *   Todos estos endpoints se implementaron con el "hack" de buscar IDs como `string` para asegurar la funcionalidad para la presentación.

---

## 3. Frontend (Astro)

Se corrigieron varios bugs que impedían el funcionamiento de la interfaz de administración.

*   **Bucle de Redirección:** Se solucionó un bucle infinito entre `/Admin` y `/AdminPanel` al corregir la URL del backend en `AdminPanel.astro`, que apuntaba al puerto incorrecto y causaba un fallo en la verificación de la sesión.
*   **Botones Inactivos:** Se arreglaron los botones de "Eliminar" en `ListaDep.astro` y `ListaNoticias.astro` corrigiendo el puerto de la URL del backend y asegurando que el `id` (ahora un `string`) se pasara correctamente en la función `onclick`.
*   **Error `NaN` en URL:** Se corrigió un bug en `AdminPanel.astro` que intentaba convertir el `id` de MongoDB (un string) a un `Number`, resultando en `NaN` y rompiendo la URL para la página de edición.

---

## 4. Descripción de los Elementos de Base de Datos

La aplicación utiliza una base de datos NoSQL (MongoDB) para persistir la información. Los datos se organizan en **colecciones**, que son el equivalente a las tablas en las bases de datos relacionales.

*   **Colecciones Principales:**
    *   `users`: Almacena la información de los usuarios (nombre, contraseña hasheada, etc.).
    *   `dep`: Contiene la información de los departamentos (título, descripción, imagen, etc.).
    *   `news`: Almacena las noticias publicadas en la intranet.
    *   `link`: Guarda los links de interés generales.
    *   `linkdep`: Contiene los links específicos de cada departamento.
    *   `company`, `about`, `birthday`: Colecciones para almacenar información institucional variada.
    *   `logs`: Nueva colección para registrar las acciones de los usuarios.

*   **Relaciones:**
    *   A diferencia de SQL, MongoDB no impone "foreign keys". La relación se maneja a nivel de aplicación.
    *   **Departamento-Links:** La colección `linkdep` contiene un campo `dep_id` que guarda el `_id` del departamento al que pertenece. Cuando se necesita mostrar un departamento con sus links, la aplicación primero busca el departamento y luego busca en `linkdep` todos los documentos que coincidan con ese `dep_id`.
    *   **Usuario-Contenido:** Colecciones como `news` y `dep` tienen un campo `autor_id` para registrar qué usuario creó el contenido.

*   **Esquemas (Pydantic):** A nivel de aplicación, se usan modelos de Pydantic para definir un esquema y validar los datos antes de interactuar con la base de datos, aportando una capa de estructura y seguridad de tipos.

---

## 5. Comparación: BD Relacional vs. MongoDB en esta Aplicación

La migración de SQL a MongoDB en este proyecto resalta las diferencias clave entre ambos paradigmas.

### Ventajas de MongoDB (NoSQL)

*   **Flexibilidad de Esquema:** Si en el futuro se necesita añadir un nuevo tipo de noticia con campos completamente diferentes, o un departamento con una estructura nueva, no es necesario realizar una migración de esquema compleja como en SQL. Simplemente se inserta el nuevo documento con la nueva estructura.
*   **Escalabilidad Horizontal:** Aunque no se aplica a esta escala, MongoDB está diseñado para escalar horizontalmente (añadir más servidores) de forma más sencilla que muchas bases de datos relacionales tradicionales.
*   **Manejo de Datos Jerárquicos:** Para entidades como "Departamento y sus Links", es natural en MongoDB obtener el departamento y luego sus links, y unirlos en la aplicación en un solo objeto JSON, que es el formato nativo de la web moderna.

### Desventajas de MongoDB y Ventajas de SQL

*   **Transacciones:** Como descubrimos, habilitar transacciones en MongoDB requiere una configuración de entorno más compleja (un "replica set"). En la mayoría de las bases de datos SQL, las transacciones están disponibles por defecto y son un pilar fundamental del sistema.
*   **Integridad de Datos:** Una base de datos relacional habría impedido, por ejemplo, que existiera un `linkdep` sin un departamento válido, gracias a las `FOREIGN KEY CONSTRAINTS`. En MongoDB, esta lógica de "borrado en cascada" o de validación de referencias debe ser implementada manualmente en el código de la aplicación, como se hizo en el endpoint `eliminar_departamento`.
*   **JOINs Complejos:** Mientras que el `$lookup` de MongoDB es potente, realizar uniones complejas entre múltiples colecciones es generalmente más simple y performante en SQL, que está optimizado para ello desde su concepción.

---

## 6. Conclusión y Recomendación

La migración de una base de datos relacional a MongoDB fue un éxito funcional, pero demostró que, aunque conceptualmente directa, presenta desafíos técnicos importantes. La mayor complejidad no provino de la lógica de la base de datos en sí, sino de la configuración del entorno (`Docker`, dependencias de Python) y de la necesidad de adaptar el código de la aplicación a un nuevo paradigma (manejo de IDs como `string` vs `ObjectId`, implementación manual de la integridad referencial).

Como experiencia de aprendizaje, fue extremadamente valiosa, ya que expuso problemas del mundo real que ocurren en proyectos de software.

**Recomendación:**

*   Para una aplicación como esta intranet, donde las estructuras de datos pueden evolucionar (nuevos tipos de noticias, campos personalizados para departamentos), **MongoDB** es una excelente elección por su flexibilidad. Sin embargo, requiere una mayor disciplina por parte del equipo de desarrollo para mantener la consistencia de los datos en la lógica de la aplicación.
*   Si la estructura de la intranet fuera muy rígida, con relaciones complejas y bien definidas que no se espera que cambien, una **base de datos relacional (SQL)** podría haber sido más simple a largo plazo, ya que el propio motor de la base de datos se encargaría de la integridad y las transacciones de forma más nativa.

La elección final depende de las prioridades del proyecto: **flexibilidad y velocidad de desarrollo (MongoDB) vs. integridad de datos estricta y garantizada por el sistema (SQL)**. Para fines académicos y de aprendizaje de nuevos paradigmas, la elección de MongoDB fue muy acertada.