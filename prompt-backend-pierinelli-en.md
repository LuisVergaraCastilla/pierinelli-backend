# Prompt para desarrollo de backend — App Pierinelli

## Contexto del proyecto

Necesito que desarrolles el **backend** de una aplicación móvil para la empresa **Pierinelli**, dedicada a la venta de planchas. El backend debe exponer una **API REST** que será consumida por un frontend en **React Native** (no necesitas programar el frontend, solo el backend).

**Stack requerido:**
- **Django** + **Django REST Framework (DRF)**
- Base de datos: **PostgreSQL**
- Autenticación: **JWT** (usar `djangorestframework-simplejwt`)
- Manejo de imágenes: soporte para subir y servir archivos (usar `Pillow` + `MEDIA_ROOT`/`MEDIA_URL` de Django, o dejar preparado para integrarlo con un storage externo tipo Cloudinary/S3 si se prefiere)

⚠️ **Importante — Idioma del código:** todo el código (nombres de modelos, campos, variables, funciones, endpoints, nombres de apps/archivos, mensajes de log internos, etc.) debe estar en **inglés**, siguiendo buenas prácticas de nomenclatura en desarrollo de software. Los comentarios en el código y el `README` pueden estar en español si lo prefieres, pero el código en sí (identificadores) siempre en inglés.

El proyecto debe mantenerse **simple y funcional**, sin sobre-ingeniería. Es un MVP académico/profesional que debe verse limpio, ordenado y bien documentado, no una app enterprise compleja.

---

## 1. Estructura de apps de Django (en inglés)

```
users/
products/
sales/
```

---

## 2. Modelos de datos

### User (app `users`) — extender `AbstractUser` o crear modelo custom
- `id`
- `first_name` (string)
- `last_name` (string)
- `email` (string, único, se usa como username para login)
- `password` (hasheado, manejo estándar de Django)
- `role` (choices: `admin`, `worker`)
- `created_at` (datetime, auto)

### Product (app `products`) — representa cada "plancha"
- `id`
- `name` (string)
- `description` (text)
- `height` (float)
- `width` (float)
- `area` (float — calcular automáticamente como `height * width` al guardar, no depender de que el frontend lo mande)
- `price` (decimal)
- `stock` (integer, no negativo)
- `image` (ImageField — para soportar la foto tomada con la cámara desde el frontend)
- `created_at` (datetime, auto)
- `updated_at` (datetime, auto)

### Sale (app `sales`)
- `id`
- `product` (FK a Product)
- `worker` (FK a User)
- `quantity` (integer, > 0)
- `unit_price` (decimal — copiar el precio vigente del producto al momento de la venta, no referenciarlo dinámicamente)
- `total_price` (decimal — calculado: `quantity * unit_price`)
- `sold_at` (datetime, auto)

---

## 3. Endpoints requeridos (rutas en inglés)

### Authentication
- `POST /api/auth/login/` → recibe `email` y `password`, retorna JWT (access + refresh) y datos básicos del usuario (`first_name`, `role`).
- `POST /api/auth/refresh/` → renovar token.

### Users (solo rol `admin`)
- `GET /api/users/` → listar todos los usuarios
- `POST /api/users/` → crear usuario (admin o worker)
- `GET /api/users/{id}/` → detalle
- `PUT /api/users/{id}/` → editar
- `DELETE /api/users/{id}/` → eliminar

### Products
- `GET /api/products/` → listar (accesible por admin y worker)
- `POST /api/products/` → crear (solo admin, debe aceptar `multipart/form-data` para incluir imagen)
- `GET /api/products/{id}/` → detalle
- `PUT /api/products/{id}/` → editar (solo admin)
- `DELETE /api/products/{id}/` → eliminar (solo admin)

### Sales
- `POST /api/sales/` → registrar venta (rol `worker`).
  - Debe validar que `quantity` solicitada no supere el `stock` disponible.
  - Debe descontar automáticamente el stock del producto al confirmarse.
  - Debe asociar automáticamente al `worker` autenticado (no se manda en el body, se obtiene del token JWT).
  - La respuesta debe incluir un campo indicador (`low_stock: true/false`, con un umbral configurable, ej. `stock <= 3`) para que el frontend pueda disparar una notificación local si corresponde.
- `GET /api/sales/` → listar historial de ventas (solo admin), debe incluir: producto, cantidad, precio, fecha/hora y trabajador que la realizó (usar `select_related` para optimizar la consulta).

---

## 4. Permisos y roles (código en inglés)

Implementar permisos personalizados de DRF (`permissions.BasePermission`) con nombres como:
- `IsAdmin`: solo usuarios con `role == "admin"` pueden acceder.
- `IsWorker`: solo usuarios con `role == "worker"` pueden acceder (para el endpoint de crear venta).
- Endpoints de solo lectura de productos (`GET`) deben estar disponibles para ambos roles autenticados.

Todos los endpoints (excepto login) deben requerir autenticación JWT (`IsAuthenticated`).

---

## 5. Validaciones y manejo de errores (requisito importante)

El proyecto será evaluado también por buenas prácticas básicas, así que es importante que implementes:

- **Validaciones de negocio:**
  - No permitir crear/editar un producto con `stock < 0` o `price <= 0`.
  - No permitir registrar una venta con `quantity > stock` disponible (retornar error 400 con mensaje claro, ej: `"Insufficient stock. Available: X"`).
  - Validar que el `email` de usuario sea único y tenga formato válido.
  - Campos obligatorios no vacíos en todos los serializers.

- **Manejo de errores consistente:**
  - Usar los mecanismos de DRF (`serializers.ValidationError`, respuestas 400/401/403/404) de forma consistente en toda la API.
  - Las respuestas de error deben tener un formato uniforme, por ejemplo:
    ```json
    { "error": true, "message": "Error description" }
    ```

- **Logging básico:**
  - Configurar el `LOGGING` de Django para registrar en consola y/o archivo (`logs/app.log`):
    - Errores no controlados (excepciones 500).
    - Eventos clave: login exitoso/fallido, creación de venta, creación/eliminación de producto o usuario.
  - Los mensajes de log deben redactarse en inglés (ej. `"Sale created successfully"`, `"Login failed for user"`).
  - No es necesario un sistema complejo, solo `logging` estándar de Python bien configurado.

---

## 6. Consideraciones adicionales

- **CORS:** habilitar `django-cors-headers` para que React Native pueda consumir la API sin problemas durante desarrollo.
- **Documentación de la API:** generar documentación automática con `drf-spectacular` o `drf-yasg` (Swagger/OpenAPI), para que el equipo de frontend pueda probar los endpoints fácilmente.
- **Seed/datos de prueba:** incluir un comando de management (ej. `python manage.py seed_data`) o fixture que cree un usuario admin y un par de productos de ejemplo, para poder probar la app sin partir de cero.
- **README:** puede estar en español, con instrucciones claras de instalación, variables de entorno necesarias (`.env`), migraciones y cómo levantar el servidor localmente.

---

## 7. Fuera de alcance (no lo implementes)

- No es necesario implementar el envío de notificaciones push reales desde el backend (Firebase Cloud Messaging, etc.). La notificación de "stock bajo" se maneja como **notificación local en el frontend**, el backend solo necesita informar el dato (`low_stock`) en la respuesta de la venta.
- No es necesario implementar recuperación de contraseña, registro público de usuarios, ni verificación de correo — los usuarios los crea únicamente el admin.
- No es necesario un frontend web ni panel de administración custom (el Django Admin por defecto es suficiente si quieres dejarlo habilitado para pruebas internas).

---

## Resumen de la Historia de Usuario a implementar

Como **administrador**, quiero gestionar usuarios, productos (planchas, incluyendo su foto) y ver el historial de ventas, para controlar el inventario y el desempeño del negocio.

Como **trabajador**, quiero ver el catálogo de productos y registrar ventas, para atender clientes y descontar stock automáticamente.

El sistema debe validar el rol de cada usuario mediante JWT en cada request, controlar errores de forma clara, registrar eventos relevantes en inglés, y dejar la API lista y documentada para ser consumida por una app en React Native.
