"""
Archivo de rutas para la gestión de tareas.
Todas las rutas llaman a la clase TaskManager.
"""

from flask import Blueprint, request, jsonify
from managers.task_manager import TaskManager
from models.task import Task

# Crear Blueprint para las rutas de tareas
task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    """
    GET /tasks → devuelve todas las tareas.
    """
    try:
        tasks = TaskManager.load_tasks()
        tasks_dict = [task.to_dict() for task in tasks]
        
        return jsonify({
            'total': len(tasks_dict),
            'tasks': tasks_dict
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    GET /tasks/<id> → devuelve una tarea específica.
    """
    try:
        task = TaskManager.get_task_by_id(task_id)
        
        if task is None:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        return jsonify(task.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    POST /tasks → crea una tarea nueva.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Crear objeto Task desde el diccionario
        task = Task.from_dict(data)
        
        # Validar la tarea
        is_valid, error_message = task.validate()
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Agregar la tarea usando TaskManager
        if TaskManager.add_task(task):
            return jsonify(task.to_dict()), 201
        else:
            return jsonify({'error': 'Error al guardar la tarea'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    PUT /tasks/<id> → modifica una tarea existente.
    """
    try:
        # Verificar que la tarea existe
        existing_task = TaskManager.get_task_by_id(task_id)
        if existing_task is None:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
        
        # Crear objeto Task con los datos actualizados
        updated_task = Task.from_dict(data)
        
        # Validar la tarea
        is_valid, error_message = updated_task.validate()
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Actualizar la tarea usando TaskManager
        if TaskManager.update_task(task_id, updated_task):
            updated_task = TaskManager.get_task_by_id(task_id)
            return jsonify(updated_task.to_dict()), 200
        else:
            return jsonify({'error': 'Error al actualizar la tarea'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    DELETE /tasks/<id> → elimina una tarea.
    """
    try:
        # Verificar que la tarea existe
        existing_task = TaskManager.get_task_by_id(task_id)
        if existing_task is None:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        # Eliminar la tarea usando TaskManager
        if TaskManager.delete_task(task_id):
            return jsonify({
                'message': 'Tarea eliminada exitosamente',
                'id': task_id
            }), 200
        else:
            return jsonify({'error': 'Error al eliminar la tarea'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

