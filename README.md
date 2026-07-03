# Backend de la Aplicación Pierinelli

Este es el backend para la aplicación móvil de Pierinelli. Está construido con Django y Django REST Framework, y provee una API REST para gestionar usuarios, productos y ventas.

## 1. Requisitos

- Python 3.8+
- Un entorno virtual de Python

## 2. Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd pierinelli-backend
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Aún no se ha creado un archivo `requirements.txt`, pero este sería el paso a seguir. Por ahora, las dependencias se pueden instalar manualmente con `pip install django djangorestframework ...`)*

## 3. Configuración

El proyecto está configurado para usar una base de datos SQLite (`db.sqlite3`) por defecto, lo cual es ideal para desarrollo. No se requieren configuraciones de variables de entorno adicionales para un entorno de desarrollo básico.

La `SECRET_KEY` de Django se encuentra en `pierinelli_backend/settings.py`. Para un entorno de producción, esta clave debería ser secreta y cargada desde variables de entorno.

## 4. Uso

1.  **Aplica las migraciones:**
    Para crear las tablas en la base de datos, ejecuta:
    ```bash
    python3 manage.py migrate
    ```

2.  **Puebla la base de datos con datos de prueba:**
    El proyecto incluye un comando para generar datos de prueba (un usuario admin, un usuario trabajador y algunos productos).
    ```bash
    python3 manage.py seed_data
    ```
    Esto creará los siguientes usuarios:
    - **Admin:** `admin@pierinelli.com` (password: `adminpassword`)
    - **Trabajador:** `worker@pierinelli.com` (password: `workerpassword`)

3.  **Inicia el servidor de desarrollo:**
    ```bash
    python3 manage.py runserver
    ```
    El servidor estará corriendo en `http://127.0.0.1:8000/`.

## 5. Endpoints de la API

La documentación completa de la API está disponible a través de Swagger UI una vez que el servidor está en marcha.

- **Swagger UI:** `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **Schema (OpenAPI):** `http://127.0.0.1:8000/api/schema/`

### Autenticación
- `POST /api/auth/login/`: Obtiene un token JWT (access y refresh).
- `POST /api/auth/refresh/`: Refresca un token de acceso.

### Usuarios (Solo Admin)
- `GET, POST /api/users/`
- `GET, PUT, DELETE /api/users/{id}/`

### Productos (Lectura para todos, escritura para Admin)
- `GET, POST /api/products/`
- `GET, PUT, DELETE /api/products/{id}/`

### Ventas
- `POST /api/sales/` (Solo Trabajador)
- `GET /api/sales/` (Solo Admin)

## 6. Logging

Los logs de la aplicación se guardan en el archivo `logs/app.log` y también se imprimen en la consola.
