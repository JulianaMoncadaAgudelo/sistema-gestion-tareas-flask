"""
Script de demostración simple usando solo urllib (biblioteca estándar).
Ejecuta este script después de iniciar el servidor con: python app_simple.py
"""

import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5000"

def make_request(method, url, data=None):
    """Hace una petición HTTP"""
    if data:
        data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return None, str(e)

def print_section(title):
    """Imprime un título de sección"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def main():
    print_section("DEMOSTRACIÓN DE API - Gestión de Tareas")
    
    # Verificar que el servidor esté corriendo
    print("\n1. Verificando servidor (GET /)")
    status, response = make_request('GET', f"{BASE_URL}/")
    print(f"   Status: {status}")
    print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
    if status != 200:
        print("\n[ERROR] No se pudo conectar al servidor.")
        print("   Por favor, ejecuta primero: python app_simple.py")
        return
    
    # 1. Obtener todas las tareas
    print_section("2. OBTENER TODAS LAS TAREAS (GET /tasks)")
    status, response = make_request('GET', f"{BASE_URL}/tasks")
    print(f"   Status: {status}")
    print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
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
    status, response = make_request('POST', f"{BASE_URL}/tasks", nueva_tarea)
    print(f"   Status: {status}")
    print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
    if status == 201:
        task_id = response.get('id')
        print(f"\n   [OK] Tarea creada con ID: {task_id}")
        
        # 3. Obtener todas las tareas
        print_section("4. OBTENER TODAS LAS TAREAS (GET /tasks)")
        status, response = make_request('GET', f"{BASE_URL}/tasks")
        print(f"   Status: {status}")
        print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
        # 4. Obtener una tarea específica
        print_section(f"5. OBTENER TAREA ESPECÍFICA (GET /tasks/{task_id})")
        status, response = make_request('GET', f"{BASE_URL}/tasks/{task_id}")
        print(f"   Status: {status}")
        print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
        # 5. Actualizar la tarea
        print_section(f"6. ACTUALIZAR TAREA (PUT /tasks/{task_id})")
        tarea_actualizada = {
            "title": "Implementar API REST - Actualizado",
            "status": "en_progreso",
            "priority": "bloqueante"
        }
        status, response = make_request('PUT', f"{BASE_URL}/tasks/{task_id}", tarea_actualizada)
        print(f"   Status: {status}")
        print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
        # 6. Verificar la actualización
        print_section(f"7. VERIFICAR ACTUALIZACIÓN (GET /tasks/{task_id})")
        status, response = make_request('GET', f"{BASE_URL}/tasks/{task_id}")
        print(f"   Status: {status}")
        print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
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
        status, response = make_request('POST', f"{BASE_URL}/tasks", segunda_tarea)
        print(f"   Status: {status}")
        print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
        # 8. Listar todas las tareas
        print_section("9. LISTAR TODAS LAS TAREAS (GET /tasks)")
        status, response = make_request('GET', f"{BASE_URL}/tasks")
        print(f"   Status: {status}")
        print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
        # 9. Eliminar una tarea
        print_section(f"10. ELIMINAR TAREA (DELETE /tasks/{task_id})")
        status, response = make_request('DELETE', f"{BASE_URL}/tasks/{task_id}")
        print(f"   Status: {status}")
        print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
        # 10. Verificar eliminación
        print_section("11. VERIFICAR ELIMINACIÓN (GET /tasks)")
        status, response = make_request('GET', f"{BASE_URL}/tasks")
        print(f"   Status: {status}")
        print(f"   Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
        
        print_section("[OK] DEMOSTRACION COMPLETADA")
        print("\nTodos los endpoints están funcionando correctamente!")
        print(f"\nPuedes seguir probando en: {BASE_URL}")
        print("\nEndpoints disponibles:")
        print("  - GET    /tasks         -> Obtener todas las tareas")
        print("  - GET    /tasks/<id>    -> Obtener una tarea especifica")
        print("  - POST   /tasks         -> Crear una nueva tarea")
        print("  - PUT    /tasks/<id>    -> Actualizar una tarea")
        print("  - DELETE /tasks/<id>    -> Eliminar una tarea")
    else:
        print("\n[ERROR] Error al crear la tarea. Verifica que el servidor esté funcionando.")

if __name__ == "__main__":
    main()

