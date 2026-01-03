"""
Clase TaskManager: gestiona el uso de tareas con el archivo JSON.
"""

import json
import os
from typing import List
from models.task import Task


class TaskManager:
    """Clase para gestionar tareas usando archivo JSON"""
    
    JSON_FILE = 'tasks.json'
    
    @staticmethod
    def load_tasks():
        """
        Carga tareas desde tasks.json y las convierte en objetos Task.
        
        Returns:
            List[Task]: Lista de objetos Task
        """
        if not os.path.exists(TaskManager.JSON_FILE):
            # Si el archivo no existe, crear uno vacío
            TaskManager.save_tasks([])
            return []
        
        try:
            with open(TaskManager.JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            tasks = []
            for task_data in data:
                task = Task.from_dict(task_data)
                tasks.append(task)
            
            return tasks
        except json.JSONDecodeError:
            # Si el archivo está corrupto, devolver lista vacía
            return []
        except Exception as e:
            print(f"Error al cargar tareas: {e}")
            return []
    
    @staticmethod
    def save_tasks(tasks: List[Task]):
        """
        Guarda la lista de Task en el archivo JSON.
        
        Args:
            tasks: Lista de objetos Task a guardar
        """
        try:
            # Convertir todas las tareas a diccionarios
            tasks_data = [task.to_dict() for task in tasks]
            
            # Guardar en el archivo JSON
            with open(TaskManager.JSON_FILE, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error al guardar tareas: {e}")
            return False
    
    @staticmethod
    def get_next_id():
        """
        Obtiene el siguiente ID disponible para una nueva tarea.
        
        Returns:
            int: Siguiente ID disponible
        """
        tasks = TaskManager.load_tasks()
        if not tasks:
            return 1
        
        max_id = max(task.id for task in tasks if task.id is not None)
        return max_id + 1
    
    @staticmethod
    def get_task_by_id(task_id: int):
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id: ID de la tarea
            
        Returns:
            Task o None: La tarea encontrada o None si no existe
        """
        tasks = TaskManager.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    @staticmethod
    def add_task(task: Task):
        """
        Agrega una nueva tarea.
        
        Args:
            task: Objeto Task a agregar
            
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        tasks = TaskManager.load_tasks()
        
        # Asignar ID si no tiene
        if task.id is None:
            task.id = TaskManager.get_next_id()
        
        tasks.append(task)
        return TaskManager.save_tasks(tasks)
    
    @staticmethod
    def update_task(task_id: int, updated_task: Task):
        """
        Actualiza una tarea existente.
        
        Args:
            task_id: ID de la tarea a actualizar
            updated_task: Objeto Task con los datos actualizados
            
        Returns:
            bool: True si se actualizó correctamente, False si no se encontró
        """
        tasks = TaskManager.load_tasks()
        
        for i, task in enumerate(tasks):
            if task.id == task_id:
                updated_task.id = task_id  # Mantener el ID original
                if not hasattr(updated_task, 'fecha_creacion') or not updated_task.fecha_creacion:
                    updated_task.fecha_creacion = task.fecha_creacion  # Mantener fecha de creación
                tasks[i] = updated_task
                return TaskManager.save_tasks(tasks)
        
        return False
    
    @staticmethod
    def delete_task(task_id: int):
        """
        Elimina una tarea.
        
        Args:
            task_id: ID de la tarea a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró
        """
        tasks = TaskManager.load_tasks()
        
        tasks = [task for task in tasks if task.id != task_id]
        
        if len(tasks) < len(TaskManager.load_tasks()):
            return TaskManager.save_tasks(tasks)
        
        return False

