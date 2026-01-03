# Guía de Instalación y Configuración

## Crear Entorno Virtual

### Windows

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

### Linux/Mac

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

## Instalar Dependencias

Una vez activado el entorno virtual, instala las dependencias:

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0

## Estructura del Proyecto

```
.
├── app_simple.py          # Aplicación Flask principal (versión simplificada)
├── app.py                 # Aplicación Flask completa (con interfaz web)
├── requirements.txt       # Dependencias del proyecto
├── tasks.json            # Archivo JSON para almacenar tareas (se crea automáticamente)
├── models/               # Modelos de datos
│   ├── __init__.py
│   └── task.py           # Clase Task
├── managers/             # Gestores de datos
│   ├── __init__.py
│   └── task_manager.py  # Clase TaskManager
└── routes/               # Rutas de la API
    ├── __init__.py
    └── task_routes.py    # Rutas de tareas
```

## Ejecutar la Aplicación

### Versión Simplificada (Solo API REST)

```bash
python app_simple.py
```

Esta versión solo incluye los endpoints REST API y usa TaskManager con archivo JSON.

### Versión Completa (Con Interfaz Web)

```bash
python app.py
```

Esta versión incluye interfaz web, autenticación y base de datos SQLite.

## Verificar Instalación

Una vez ejecutado, puedes probar los endpoints:

```bash
# Obtener todas las tareas
curl http://localhost:5000/tasks

# Crear una tarea
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera tarea",
    "description": "Descripción de la tarea",
    "priority": "media",
    "effort_hours": 5.0,
    "status": "pendiente",
    "assigned_to": "Juan Pérez"
  }'
```

## Desactivar Entorno Virtual

Cuando termines de trabajar:

```bash
deactivate
```

