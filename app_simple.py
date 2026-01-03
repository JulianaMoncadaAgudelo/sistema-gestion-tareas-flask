"""
Aplicación Flask principal para gestión de tareas.
Usa TaskManager y archivo JSON para almacenar tareas.
"""

from flask import Flask, send_from_directory
from routes.task_routes import task_bp
import os

# Crear aplicación Flask
app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui-cambiar-en-produccion'

# Registrar las rutas de tareas
app.register_blueprint(task_bp)

@app.route('/')
def index():
    """Ruta raíz - Sirve la interfaz web"""
    return send_from_directory('static', 'index.html')

@app.route('/api')
def api_info():
    """Información de la API"""
    return {
        'message': 'API de Gestión de Tareas',
        'endpoints': {
            'GET /tasks': 'Obtener todas las tareas',
            'GET /tasks/<id>': 'Obtener una tarea específica',
            'POST /tasks': 'Crear una nueva tarea',
            'PUT /tasks/<id>': 'Actualizar una tarea',
            'DELETE /tasks/<id>': 'Eliminar una tarea'
        }
    }

if __name__ == '__main__':
    # Inicializar archivo JSON si no existe
    from managers.task_manager import TaskManager
    TaskManager.load_tasks()  # Esto crea el archivo si no existe
    
    print("=" * 60)
    print("API de Gestión de Tareas iniciada")
    print("=" * 60)
    print("\n🌐 Interfaz Web:")
    print("   http://localhost:5000/")
    print("\n📡 Endpoints API:")
    print("   GET    /tasks       - Obtener todas las tareas")
    print("   GET    /tasks/<id>  - Obtener una tarea específica")
    print("   POST   /tasks       - Crear una nueva tarea")
    print("   PUT    /tasks/<id>  - Actualizar una tarea")
    print("   DELETE /tasks/<id>  - Eliminar una tarea")
    print("\n✅ Servidor ejecutándose en http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

