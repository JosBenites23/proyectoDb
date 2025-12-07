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
