# Sistema de Gestión de Tareas con Flask

Sistema completo de gestión de tareas que permite crear, asignar y gestionar tareas entre usuarios.

## 📋 Versiones del Proyecto

Este proyecto incluye dos versiones:

### 1. Versión Simplificada (API REST con JSON)

- **Archivo:** `app_simple.py`
- **Almacenamiento:** Archivo JSON (`tasks.json`)
- **Estructura:** Clases Task y TaskManager
- **Ver:** `README_ESTRUCTURA.md` para detalles de cumplimiento de requisitos

### 2. Versión Completa (Con Interfaz Web)

- **Archivo:** `app.py`
- **Almacenamiento:** Base de datos SQLite
- **Características:** Interfaz web, autenticación, usuarios, dashboard

## Características

- ✅ Autenticación de usuarios (registro e inicio de sesión)
- ✅ Gestión de usuarios (solo administradores)
- ✅ Creación, edición y eliminación de tareas
- ✅ Asignación de tareas a usuarios
- ✅ Estados de tareas: Pendiente, En Progreso, En Revisión, Completada
- ✅ Prioridades: Baja, Media, Alta, Bloqueante
- ✅ Horas estimadas (effort_hours) - número decimal
- ✅ Asignación por nombre de miembro del equipo (string)
- ✅ Dashboard con estadísticas
- ✅ Interfaz web moderna y responsive

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

## Configuración

1. **Ejecutar la aplicación:**

```bash
python app.py
```

2. **Acceder a la aplicación:**
   - Abre tu navegador en: `http://localhost:5000`
   - El primer usuario registrado será automáticamente administrador

## Uso

### Registro e Inicio de Sesión

1. **Registro:**

   - Ve a la página de registro
   - Completa el formulario con tu nombre, email y contraseña
   - El primer usuario será administrador automáticamente

2. **Inicio de Sesión:**
   - Usa tu email y contraseña para iniciar sesión

### Gestión de Tareas

1. **Crear Tarea:**

   - Haz clic en "Nueva Tarea" en el menú
   - Completa el formulario:
     - **title** (Título) - requerido
     - **description** (Descripción) - texto largo opcional
     - **priority** (Prioridad) - Baja, Media, Alta, Bloqueante
     - **effort_hours** (Horas Estimadas) - número decimal opcional
     - **status** (Estado) - Pendiente, En Progreso, En Revisión, Completada
     - **assigned_to** (Asignar a) - nombre del miembro del equipo (string)

2. **Editar Tarea:**

   - Haz clic en el icono de editar en cualquier tarea
   - Modifica los campos necesarios
   - Guarda los cambios

3. **Cambiar Estado:**

   - Usa el selector de estado en cada tarjeta de tarea
   - Los estados disponibles son: Pendiente, En Progreso, En Revisión, Completada

4. **Eliminar Tarea:**
   - Haz clic en el icono de eliminar
   - Confirma la eliminación

### Gestión de Usuarios (Solo Administradores)

1. **Ver Usuarios:**

   - Accede al menú "Usuarios"
   - Verás una lista de todos los usuarios registrados

2. **Crear Usuario:**
   - Haz clic en "Nuevo Usuario"
   - Completa el formulario
   - Marca la casilla "Administrador" si deseas dar permisos de admin

## Estructura del Proyecto

```
.
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias del proyecto
├── tareas.db             # Base de datos SQLite (se crea automáticamente)
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── nueva_tarea.html
│   ├── editar_tarea.html
│   ├── usuarios.html
│   └── nuevo_usuario.html
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Modelos de Datos

### Usuario

- `id`: Identificador único
- `nombre`: Nombre del usuario
- `email`: Email único
- `password_hash`: Contraseña encriptada
- `es_admin`: Si es administrador
- `fecha_creacion`: Fecha de registro

### Tarea (Task)

- `id`: Identificador único (primary key)
- `title`: Título de la tarea
- `description`: Texto largo que describe completamente la tarea
- `priority`: Prioridad - Baja, Media, Alta, Bloqueante
- `effort_hours`: Número decimal, horas estimadas para completar la tarea
- `status`: Estado - Pendiente, En Progreso, En Revisión, Completada
- `assigned_to`: String, persona del equipo a la que se asigna
- `creador_id`: Usuario que creó la tarea
- `fecha_creacion`: Fecha de creación

## Seguridad

- Las contraseñas se almacenan con hash usando Werkzeug
- Autenticación basada en sesiones con Flask-Login
- Protección CSRF (incluida en Flask)
- Validación de permisos para acciones administrativas

## API REST Endpoints

La aplicación incluye endpoints REST API para la gestión de tareas. Todos los endpoints requieren autenticación (login).

### Endpoints Disponibles

#### 1. Crear una tarea

**POST** `/tasks`

**Body (JSON):**

```json
{
  "title": "Título de la tarea",
  "description": "Descripción detallada",
  "priority": "media",
  "effort_hours": 8.5,
  "status": "pendiente",
  "assigned_to": "Nombre del miembro del equipo"
}
```

**Respuesta (201):**

```json
{
  "id": 1,
  "title": "Título de la tarea",
  "description": "Descripción detallada",
  "priority": "media",
  "effort_hours": 8.5,
  "status": "pendiente",
  "assigned_to": "Nombre del miembro del equipo",
  "fecha_creacion": "2024-01-01T12:00:00"
}
```

#### 2. Leer todas las tareas

**GET** `/tasks`

**Respuesta (200):**

```json
{
  "total": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Tarea 1",
      "description": "Descripción",
      "priority": "media",
      "effort_hours": 8.5,
      "status": "pendiente",
      "assigned_to": "Usuario",
      "fecha_creacion": "2024-01-01T12:00:00"
    }
  ]
}
```

**Nota:** Los administradores ven todas las tareas. Los usuarios regulares solo ven las tareas asignadas a ellos.

#### 3. Leer una tarea específica

**GET** `/tasks/<id>`

**Respuesta (200):**

```json
{
  "id": 1,
  "title": "Título de la tarea",
  "description": "Descripción detallada",
  "priority": "media",
  "effort_hours": 8.5,
  "status": "pendiente",
  "assigned_to": "Nombre del miembro del equipo",
  "fecha_creacion": "2024-01-01T12:00:00"
}
```

#### 4. Actualizar una tarea

**PUT** `/tasks/<id>`

**Body (JSON) - Campos opcionales:**

```json
{
  "title": "Nuevo título",
  "description": "Nueva descripción",
  "priority": "alta",
  "effort_hours": 10.0,
  "status": "en_progreso",
  "assigned_to": "Nuevo miembro"
}
```

**Respuesta (200):** Devuelve la tarea actualizada en el mismo formato que GET.

#### 5. Eliminar una tarea

**DELETE** `/tasks/<id>`

**Respuesta (200):**

```json
{
  "message": "Tarea eliminada exitosamente",
  "id": 1
}
```

### Valores Válidos

- **priority:** `baja`, `media`, `alta`, `bloqueante`
- **status:** `pendiente`, `en_progreso`, `en_revision`, `completada`
- **effort_hours:** Número decimal (ej: 8.5, 10.0)
- **assigned_to:** String con el nombre del miembro del equipo (opcional)

### Permisos

- **Crear tarea:** Cualquier usuario autenticado
- **Ver tareas:** Administradores ven todas, usuarios solo las asignadas a ellos
- **Actualizar/Eliminar:** Solo administradores o el creador de la tarea

### Ejemplo de Uso con cURL

```bash
# Crear una tarea
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<tu-sesion>" \
  -d '{
    "title": "Nueva tarea",
    "description": "Descripción",
    "priority": "alta",
    "effort_hours": 5.0,
    "status": "pendiente",
    "assigned_to": "Juan"
  }'

# Obtener todas las tareas
curl -X GET http://localhost:5000/tasks \
  -H "Cookie: session=<tu-sesion>"

# Obtener una tarea específica
curl -X GET http://localhost:5000/tasks/1 \
  -H "Cookie: session=<tu-sesion>"

# Actualizar una tarea
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<tu-sesion>" \
  -d '{
    "status": "completada"
  }'

# Eliminar una tarea
curl -X DELETE http://localhost:5000/tasks/1 \
  -H "Cookie: session=<tu-sesion>"
```

## Notas

- La base de datos SQLite se crea automáticamente al ejecutar la aplicación por primera vez
- En producción, cambia la `SECRET_KEY` en `app.py`
- Considera usar PostgreSQL o MySQL para producción
- El primer usuario registrado será automáticamente administrador
- Los endpoints API requieren autenticación mediante sesión de Flask-Login

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo.
