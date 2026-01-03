# Interfaz Web para Gestión de Tareas

Se ha creado una interfaz web sencilla y moderna para interactuar con la API de gestión de tareas.

## 🚀 Cómo Usar

1. **Inicia el servidor:**
   ```bash
   python app_simple.py
   ```

2. **Abre tu navegador en:**
   ```
   http://localhost:5000
   ```

## ✨ Características de la Interfaz

### Funcionalidades Disponibles:

- ✅ **Ver todas las tareas** - Lista todas las tareas con sus detalles
- ✅ **Crear nueva tarea** - Formulario completo con todos los campos
- ✅ **Editar tarea** - Modificar cualquier campo de una tarea existente
- ✅ **Eliminar tarea** - Eliminar tareas con confirmación
- ✅ **Actualizar lista** - Botón para refrescar las tareas

### Campos del Formulario:

- **Título** (requerido) - Título de la tarea
- **Descripción** - Texto largo descriptivo
- **Prioridad** - Baja, Media, Alta, Bloqueante
- **Horas Estimadas** - Número decimal
- **Estado** - Pendiente, En Progreso, En Revisión, Completada
- **Asignado a** - Nombre del miembro del equipo

### Diseño:

- 🎨 Interfaz moderna con gradiente de fondo
- 📱 Diseño responsive (funciona en móviles y tablets)
- 🎯 Fácil de usar e intuitiva
- ⚡ Actualización en tiempo real
- 💬 Mensajes de confirmación y error

## 📁 Archivos de la Interfaz

- `static/index.html` - Página principal HTML
- `static/style.css` - Estilos CSS
- `static/app.js` - Lógica JavaScript que consume la API

## 🔧 Personalización

Puedes modificar los estilos en `static/style.css` para personalizar la apariencia.

Los colores principales están definidos en las clases:
- `.btn-primary` - Botones principales (verde)
- `.btn-secondary` - Botones secundarios (azul)
- `.btn-danger` - Botones de eliminar (rojo)
- `.btn-edit` - Botones de editar (naranja)

## 🌐 API Endpoints Utilizados

La interfaz consume los siguientes endpoints:

- `GET /tasks` - Obtener todas las tareas
- `GET /tasks/<id>` - Obtener una tarea específica
- `POST /tasks` - Crear una nueva tarea
- `PUT /tasks/<id>` - Actualizar una tarea
- `DELETE /tasks/<id>` - Eliminar una tarea

## 📝 Notas

- La interfaz se conecta automáticamente a `http://localhost:5000`
- Si cambias el puerto, actualiza `API_BASE` en `static/app.js`
- Los datos se guardan en `tasks.json` automáticamente

