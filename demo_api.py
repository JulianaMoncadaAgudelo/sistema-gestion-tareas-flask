"""
Script de demostración para mostrar la API funcionando.
Ejecuta este script después de iniciar el servidor con: python app_simple.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Imprime un título de sección"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_response(response, description):
    """Imprime la respuesta de una petición"""
    print(f"\n{description}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def main():
    print_section("DEMOSTRACIÓN DE API - Gestión de Tareas")
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        print_response(response, "1. Verificando servidor (GET /)")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor.")
        print("   Por favor, ejecuta primero: python app_simple.py")
        print("   Y luego ejecuta este script en otra terminal.")
        return
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return
    
    # 1. Obtener todas las tareas (inicialmente vacío)
    print_section("2. OBTENER TODAS LAS TAREAS (GET /tasks)")
    response = requests.get(f"{BASE_URL}/tasks")
    print_response(response, "GET /tasks")
    
    # 2. Crear una tarea
    print_section("3. CREAR UNA TAREA (POST /tasks)")
    nueva_tarea = {
        "title": "Implementar API REST",
        "description": "Crear endpoints para gestión de tareas usando Flask",
        "priority": "alta",
        "effort_hours": 8.5,
        "status": "pendiente",
        "assigned_to": "Juan Pérez"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=nueva_tarea)
    print_response(response, "POST /tasks")
    
    if response.status_code == 201:
        task_id = response.json().get('id')
        print(f"\n✅ Tarea creada con ID: {task_id}")
        
        # 3. Obtener todas las tareas (ahora con una tarea)
        print_section("4. OBTENER TODAS LAS TAREAS (GET /tasks)")
        response = requests.get(f"{BASE_URL}/tasks")
        print_response(response, "GET /tasks")
        
        # 4. Obtener una tarea específica
        print_section(f"5. OBTENER TAREA ESPECÍFICA (GET /tasks/{task_id})")
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        print_response(response, f"GET /tasks/{task_id}")
        
        # 5. Actualizar la tarea
        print_section(f"6. ACTUALIZAR TAREA (PUT /tasks/{task_id})")
        tarea_actualizada = {
            "title": "Implementar API REST - Actualizado",
            "status": "en_progreso",
            "priority": "bloqueante"
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=tarea_actualizada)
        print_response(response, f"PUT /tasks/{task_id}")
        
        # 6. Verificar la actualización
        print_section(f"7. VERIFICAR ACTUALIZACIÓN (GET /tasks/{task_id})")
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        print_response(response, f"GET /tasks/{task_id}")
        
        # 7. Crear otra tarea
        print_section("8. CREAR SEGUNDA TAREA (POST /tasks)")
        segunda_tarea = {
            "title": "Documentar API",
            "description": "Crear documentación de los endpoints",
            "priority": "media",
            "effort_hours": 3.0,
            "status": "pendiente",
            "assigned_to": "María García"
        }
        response = requests.post(f"{BASE_URL}/tasks", json=segunda_tarea)
        print_response(response, "POST /tasks")
        
        # 8. Listar todas las tareas
        print_section("9. LISTAR TODAS LAS TAREAS (GET /tasks)")
        response = requests.get(f"{BASE_URL}/tasks")
        print_response(response, "GET /tasks")
        
        # 9. Eliminar una tarea
        print_section(f"10. ELIMINAR TAREA (DELETE /tasks/{task_id})")
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        print_response(response, f"DELETE /tasks/{task_id}")
        
        # 10. Verificar eliminación
        print_section("11. VERIFICAR ELIMINACIÓN (GET /tasks)")
        response = requests.get(f"{BASE_URL}/tasks")
        print_response(response, "GET /tasks")
        
        print_section("✅ DEMOSTRACIÓN COMPLETADA")
        print("\nTodos los endpoints están funcionando correctamente!")
        print(f"\nPuedes seguir probando en: {BASE_URL}")
        print("\nEndpoints disponibles:")
        print("  - GET    /tasks       → Obtener todas las tareas")
        print("  - GET    /tasks/<id>    → Obtener una tarea específica")
        print("  - POST   /tasks         → Crear una nueva tarea")
        print("  - PUT    /tasks/<id>    → Actualizar una tarea")
        print("  - DELETE /tasks/<id>    → Eliminar una tarea")
    else:
        print("\n❌ Error al crear la tarea. Verifica que el servidor esté funcionando.")

if __name__ == "__main__":
    main()

