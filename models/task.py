"""
Clase Task: representa una tarea con los datos del interfaz.
"""

from datetime import datetime
from decimal import Decimal


class Task:
    """Clase que representa una tarea"""
    
    def __init__(self, id=None, title=None, description=None, priority='media', 
                 effort_hours=None, status='pendiente', assigned_to=None):
        """
        Inicializa una tarea
        
        Args:
            id: Identificador único (primary key)
            title: Título de la tarea
            description: Texto largo que describe completamente la tarea
            priority: Prioridad (baja, media, alta, bloqueante)
            effort_hours: Número decimal, horas estimadas para completar la tarea
            status: Estado (pendiente, en_progreso, en_revision, completada)
            assigned_to: String, persona del equipo a la que se asigna
        """
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.effort_hours = float(effort_hours) if effort_hours is not None else None
        self.status = status
        self.assigned_to = assigned_to
        self.fecha_creacion = datetime.now().isoformat() if not hasattr(self, 'fecha_creacion') else self.fecha_creacion
    
    def to_dict(self):
        """
        Convierte el objeto Task a diccionario.
        
        Returns:
            dict: Diccionario con los datos de la tarea
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'effort_hours': self.effort_hours,
            'status': self.status,
            'assigned_to': self.assigned_to,
            'fecha_creacion': self.fecha_creacion
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea un Task desde un diccionario.
        
        Args:
            data: Diccionario con los datos de la tarea
            
        Returns:
            Task: Objeto Task creado desde el diccionario
        """
        task = cls(
            id=data.get('id'),
            title=data.get('title'),
            description=data.get('description'),
            priority=data.get('priority', 'media'),
            effort_hours=data.get('effort_hours'),
            status=data.get('status', 'pendiente'),
            assigned_to=data.get('assigned_to')
        )
        # Si hay fecha_creacion en el diccionario, usarla; si no, mantener la generada en __init__
        if 'fecha_creacion' in data and data['fecha_creacion']:
            task.fecha_creacion = data['fecha_creacion']
        return task
    
    def validate(self):
        """
        Valida que los datos de la tarea sean correctos.
        
        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        if not self.title:
            return False, "El campo 'title' es requerido"
        
        valid_priorities = ['baja', 'media', 'alta', 'bloqueante']
        if self.priority not in valid_priorities:
            return False, f"Prioridad inválida. Debe ser una de: {', '.join(valid_priorities)}"
        
        valid_statuses = ['pendiente', 'en_progreso', 'en_revision', 'completada']
        if self.status not in valid_statuses:
            return False, f"Status inválido. Debe ser uno de: {', '.join(valid_statuses)}"
        
        if self.effort_hours is not None and self.effort_hours < 0:
            return False, "effort_hours debe ser un número positivo"
        
        return True, ""

