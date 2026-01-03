"""
Script de prueba para verificar que los endpoints funcionan correctamente.
Ejecutar después de iniciar el servidor con: python app_simple.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_create_task():
    """Prueba crear una tarea"""
    print("\n1. Creando una tarea...")
    data = {
        "title": "Tarea de prueba",
        "description": "Esta es una tarea de prueba",
        "priority": "alta",
        "effort_hours": 5.5,
        "status": "pendiente",
        "assigned_to": "Juan Pérez"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json().get('id')

def test_get_all_tasks():
    """Prueba obtener todas las tareas"""
    print("\n2. Obteniendo todas las tareas...")
    response = requests.get(f"{BASE_URL}/tasks")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_get_task(task_id):
    """Prueba obtener una tarea específica"""
    print(f"\n3. Obteniendo tarea con ID {task_id}...")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_update_task(task_id):
    """Prueba actualizar una tarea"""
    print(f"\n4. Actualizando tarea con ID {task_id}...")
    data = {
        "title": "Tarea actualizada",
        "status": "en_progreso",
        "priority": "media"
    }
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_delete_task(task_id):
    """Prueba eliminar una tarea"""
    print(f"\n5. Eliminando tarea con ID {task_id}...")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS DE API - Gestión de Tareas")
    print("=" * 60)
    print("\nAsegúrate de que el servidor esté ejecutándose:")
    print("  python app_simple.py")
    print("\nPresiona Enter para continuar...")
    input()
    
    try:
        # Crear una tarea
        task_id = test_create_task()
        
        # Obtener todas las tareas
        test_get_all_tasks()
        
        # Obtener una tarea específica
        test_get_task(task_id)
        
        # Actualizar la tarea
        test_update_task(task_id)
        
        # Eliminar la tarea
        test_delete_task(task_id)
        
        print("\n" + "=" * 60)
        print("✅ Todas las pruebas completadas")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor.")
        print("   Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {e}")

