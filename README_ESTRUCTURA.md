# Estructura del Proyecto - Cumplimiento de Requisitos

Este documento verifica que el proyecto cumple con todos los requisitos especificados.

## ✅ 1. Entorno Virtual y Dependencias

### Entorno Virtual

- **Instrucciones:** Ver archivo `SETUP.md` para crear y activar el entorno virtual
- **Comandos:**
  - Windows: `python -m venv venv` → `venv\Scripts\activate`
  - Linux/Mac: `python3 -m venv venv` → `source venv/bin/activate`

### Fichero de Requerimientos

- **Archivo:** `requirements.txt`
- **Contenido:**
  ```
  Flask==3.0.0
  ```
- **Instalación:** `pip install -r requirements.txt`

## ✅ 2. Clase Task

**Archivo:** `models/task.py`

La clase `Task` representa una tarea con los datos del interfaz:

### Campos:

- `id` (primary key)
- `title` (título de la tarea)
- `description` (texto largo)
- `priority` (baja, media, alta, bloqueante)
- `effort_hours` (número decimal)
- `status` (pendiente, en_progreso, en_revision, completada)
- `assigned_to` (string, persona del equipo)

### Métodos Implementados:

#### `to_dict()`

Convierte el objeto Task a diccionario.

```python
task = Task(id=1, title="Tarea 1", ...)
task_dict = task.to_dict()
# Retorna: {'id': 1, 'title': 'Tarea 1', ...}
```

#### `from_dict(data)`

Crea un Task desde un diccionario.

```python
data = {'id': 1, 'title': 'Tarea 1', ...}
task = Task.from_dict(data)
```

## ✅ 3. Clase TaskManager

**Archivo:** `managers/task_manager.py`

La clase `TaskManager` gestiona el uso de tareas con el archivo JSON.

### Métodos Estáticos Implementados:

#### `load_tasks()`

Carga tareas desde `tasks.json` y las convierte en objetos Task.

```python
tasks = TaskManager.load_tasks()
# Retorna: List[Task]
```

#### `save_tasks(tasks)`

Guarda la lista de Task en el archivo JSON.

```python
tasks = [task1, task2, ...]
TaskManager.save_tasks(tasks)
```

### Métodos Adicionales (Ayudantes):

- `get_next_id()` - Obtiene el siguiente ID disponible
- `get_task_by_id(task_id)` - Obtiene una tarea por ID
- `add_task(task)` - Agrega una nueva tarea
- `update_task(task_id, updated_task)` - Actualiza una tarea
- `delete_task(task_id)` - Elimina una tarea

## ✅ 4. Archivo de Rutas

**Archivo:** `routes/task_routes.py`

Archivo separado donde se dan de alta todas las rutas especificadas que llaman a la clase `TaskManager`.

### Rutas Implementadas:

#### `GET /tasks`

Devuelve todas las tareas.

- Llama a: `TaskManager.load_tasks()`
- Retorna: JSON con lista de tareas

#### `GET /tasks/<id>`

Devuelve una tarea específica.

- Llama a: `TaskManager.get_task_by_id(task_id)`
- Retorna: JSON con la tarea o error 404

#### `POST /tasks`

Crea una tarea nueva.

- Llama a: `TaskManager.add_task(task)`
- Retorna: JSON con la tarea creada (201)

#### `PUT /tasks/<id>`

Modifica una tarea existente.

- Llama a: `TaskManager.update_task(task_id, updated_task)`
- Retorna: JSON con la tarea actualizada (200)

#### `DELETE /tasks/<id>`

Elimina una tarea.

- Llama a: `TaskManager.delete_task(task_id)`
- Retorna: JSON con mensaje de confirmación (200)

## ✅ 5. Flask API

**Archivo principal:** `app_simple.py`

Aplicación Flask que registra las rutas del Blueprint `task_bp`.

### Estructura:

```python
from flask import Flask
from routes.task_routes import task_bp

app = Flask(__name__)
app.register_blueprint(task_bp)
```

## 📁 Estructura de Archivos

```
.
├── app_simple.py          # Aplicación Flask (versión API REST)
├── app.py                 # Aplicación Flask completa (con interfaz web)
├── requirements.txt       # Dependencias
├── SETUP.md              # Instrucciones de instalación
├── tasks.json            # Archivo JSON (se crea automáticamente)
├── models/
│   ├── __init__.py
│   └── task.py           # Clase Task
├── managers/
│   ├── __init__.py
│   └── task_manager.py   # Clase TaskManager
└── routes/
    ├── __init__.py
    └── task_routes.py    # Rutas Flask que usan TaskManager
```

## 🧪 Pruebas de los Endpoints

### 1. Crear una tarea

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar API",
    "description": "Crear endpoints REST",
    "priority": "alta",
    "effort_hours": 8.5,
    "status": "pendiente",
    "assigned_to": "Juan Pérez"
  }'
```

### 2. Obtener todas las tareas

```bash
curl http://localhost:5000/tasks
```

### 3. Obtener una tarea específica

```bash
curl http://localhost:5000/tasks/1
```

### 4. Actualizar una tarea

```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tarea actualizada",
    "status": "en_progreso"
  }'
```

### 5. Eliminar una tarea

```bash
curl -X DELETE http://localhost:5000/tasks/1
```

## ✅ Verificación de Cumplimiento

- ✅ Entorno virtual y requirements.txt creados
- ✅ Clase Task con métodos `to_dict()` y `from_dict()`
- ✅ Clase TaskManager con métodos estáticos `load_tasks()` y `save_tasks()`
- ✅ Archivo de rutas separado (`routes/task_routes.py`)
- ✅ Todas las rutas llaman a TaskManager
- ✅ Endpoints Flask API implementados:
  - ✅ GET /tasks
  - ✅ GET /tasks/<id>
  - ✅ POST /tasks
  - ✅ PUT /tasks/<id>
  - ✅ DELETE /tasks/<id>
- ✅ Uso de archivo JSON (`tasks.json`) para almacenamiento
