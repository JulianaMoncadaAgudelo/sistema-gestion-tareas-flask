const API_BASE = 'http://localhost:5000';

// Cargar tareas al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadTasks();
});

// Cargar todas las tareas
async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks`);
        const data = await response.json();
        
        displayTasks(data.tasks || []);
    } catch (error) {
        showMessage('Error al cargar las tareas: ' + error.message, 'error');
    }
}

// Mostrar tareas en el contenedor
function displayTasks(tasks) {
    const container = document.getElementById('tasksContainer');
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>📭 No hay tareas</h3>
                <p>Crea tu primera tarea para comenzar</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = tasks.map(task => `
        <div class="task-card">
            <div class="task-header">
                <div>
                    <div class="task-title">${escapeHtml(task.title)}</div>
                    <div class="task-info">ID: ${task.id} | Creada: ${formatDate(task.fecha_creacion)}</div>
                </div>
            </div>
            
            ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
            
            <div class="task-meta">
                <span class="badge badge-priority-${task.priority}">${capitalize(task.priority)}</span>
                <span class="badge badge-status-${task.status}">${formatStatus(task.status)}</span>
                ${task.effort_hours ? `<span class="badge badge-hours">⏱️ ${task.effort_hours}h</span>` : ''}
            </div>
            
            <div class="task-info">
                ${task.assigned_to ? `👤 Asignado a: <strong>${escapeHtml(task.assigned_to)}</strong>` : '👤 Sin asignar'}
            </div>
            
            <div class="task-actions">
                <button class="btn btn-edit" onclick="editTask(${task.id})">✏️ Editar</button>
                <button class="btn btn-danger" onclick="deleteTask(${task.id})">🗑️ Eliminar</button>
            </div>
        </div>
    `).join('');
}

// Mostrar formulario para crear tarea
function showCreateForm() {
    document.getElementById('formTitle').textContent = 'Nueva Tarea';
    document.getElementById('taskFormElement').reset();
    document.getElementById('taskId').value = '';
    document.getElementById('taskForm').style.display = 'block';
    document.getElementById('taskForm').scrollIntoView({ behavior: 'smooth' });
}

// Ocultar formulario
function hideForm() {
    document.getElementById('taskForm').style.display = 'none';
}

// Editar tarea
async function editTask(id) {
    try {
        const response = await fetch(`${API_BASE}/tasks/${id}`);
        const task = await response.json();
        
        document.getElementById('formTitle').textContent = 'Editar Tarea';
        document.getElementById('taskId').value = task.id;
        document.getElementById('title').value = task.title || '';
        document.getElementById('description').value = task.description || '';
        document.getElementById('priority').value = task.priority || 'media';
        document.getElementById('effort_hours').value = task.effort_hours || '';
        document.getElementById('status').value = task.status || 'pendiente';
        document.getElementById('assigned_to').value = task.assigned_to || '';
        
        document.getElementById('taskForm').style.display = 'block';
        document.getElementById('taskForm').scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showMessage('Error al cargar la tarea: ' + error.message, 'error');
    }
}

// Guardar tarea (crear o actualizar)
async function saveTask(event) {
    event.preventDefault();
    
    const taskId = document.getElementById('taskId').value;
    const taskData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        priority: document.getElementById('priority').value,
        effort_hours: document.getElementById('effort_hours').value ? parseFloat(document.getElementById('effort_hours').value) : null,
        status: document.getElementById('status').value,
        assigned_to: document.getElementById('assigned_to').value || null
    };
    
    try {
        let response;
        if (taskId) {
            // Actualizar tarea existente
            response = await fetch(`${API_BASE}/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(taskData)
            });
        } else {
            // Crear nueva tarea
            response = await fetch(`${API_BASE}/tasks`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(taskData)
            });
        }
        
        if (response.ok) {
            showMessage(taskId ? 'Tarea actualizada exitosamente' : 'Tarea creada exitosamente', 'success');
            hideForm();
            loadTasks();
        } else {
            const error = await response.json();
            showMessage('Error: ' + (error.error || 'No se pudo guardar la tarea'), 'error');
        }
    } catch (error) {
        showMessage('Error al guardar la tarea: ' + error.message, 'error');
    }
}

// Eliminar tarea
async function deleteTask(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar esta tarea?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/tasks/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showMessage('Tarea eliminada exitosamente', 'success');
            loadTasks();
        } else {
            const error = await response.json();
            showMessage('Error: ' + (error.error || 'No se pudo eliminar la tarea'), 'error');
        }
    } catch (error) {
        showMessage('Error al eliminar la tarea: ' + error.message, 'error');
    }
}

// Mostrar mensaje
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

// Utilidades
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1);
}

function formatStatus(status) {
    return status.replace('_', ' ').split(' ').map(capitalize).join(' ');
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

