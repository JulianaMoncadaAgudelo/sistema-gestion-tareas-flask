from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui-cambiar-en-produccion'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'

# Modelos
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='media')  # baja, media, alta, bloqueante
    effort_hours = db.Column(db.Numeric(10, 2), nullable=True)  # número decimal
    status = db.Column(db.String(20), default='pendiente')  # pendiente, en_progreso, en_revision, completada
    assigned_to = db.Column(db.String(100), nullable=True)  # string, persona del equipo
    creador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    creador = db.relationship('Usuario', foreign_keys=[creador_id], backref='tareas_creadas')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rutas de autenticación
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            login_user(usuario)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('register.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('register.html')
        
        usuario = Usuario(nombre=nombre, email=email)
        usuario.set_password(password)
        
        # El primer usuario es admin por defecto
        if Usuario.query.count() == 0:
            usuario.es_admin = True
        
        db.session.add(usuario)
        db.session.commit()
        
        flash('Registro exitoso. Por favor, inicia sesión.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login'))

# Rutas principales
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.es_admin:
        tareas = Tarea.query.order_by(Tarea.fecha_creacion.desc()).all()
    else:
        # Filtrar por assigned_to (string) que coincida con el nombre del usuario
        tareas = Tarea.query.filter(Tarea.assigned_to == current_user.nombre).order_by(Tarea.fecha_creacion.desc()).all()
    
    usuarios = Usuario.query.all() if current_user.es_admin else []
    
    estadisticas = {
        'total': len(tareas),
        'pendientes': len([t for t in tareas if t.status == 'pendiente']),
        'en_progreso': len([t for t in tareas if t.status == 'en_progreso']),
        'en_revision': len([t for t in tareas if t.status == 'en_revision']),
        'completadas': len([t for t in tareas if t.status == 'completada'])
    }
    
    return render_template('dashboard.html', tareas=tareas, usuarios=usuarios, estadisticas=estadisticas)

# Rutas de tareas
@app.route('/tareas/nueva', methods=['GET', 'POST'])
@login_required
def nueva_tarea():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'media')
        effort_hours = request.form.get('effort_hours')
        status = request.form.get('status', 'pendiente')
        assigned_to = request.form.get('assigned_to', '').strip()
        
        tarea = Tarea(
            title=title,
            description=description,
            priority=priority,
            effort_hours=Decimal(effort_hours) if effort_hours else None,
            status=status,
            assigned_to=assigned_to if assigned_to else None,
            creador_id=current_user.id
        )
        
        db.session.add(tarea)
        db.session.commit()
        
        flash('Tarea creada exitosamente', 'success')
        return redirect(url_for('dashboard'))
    
    usuarios = Usuario.query.all() if current_user.es_admin else [current_user]
    return render_template('nueva_tarea.html', usuarios=usuarios)

@app.route('/tareas/<int:tarea_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    
    # Verificar permisos
    if not current_user.es_admin and tarea.creador_id != current_user.id:
        flash('No tienes permiso para editar esta tarea', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        tarea.title = request.form.get('title')
        tarea.description = request.form.get('description')
        tarea.priority = request.form.get('priority', 'media')
        effort_hours = request.form.get('effort_hours')
        tarea.effort_hours = Decimal(effort_hours) if effort_hours else None
        tarea.status = request.form.get('status', 'pendiente')
        assigned_to = request.form.get('assigned_to', '').strip()
        tarea.assigned_to = assigned_to if assigned_to else None
        
        db.session.commit()
        flash('Tarea actualizada exitosamente', 'success')
        return redirect(url_for('dashboard'))
    
    usuarios = Usuario.query.all() if current_user.es_admin else [current_user]
    return render_template('editar_tarea.html', tarea=tarea, usuarios=usuarios)

@app.route('/tareas/<int:tarea_id>/eliminar', methods=['POST'])
@login_required
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    
    # Verificar permisos
    if not current_user.es_admin and tarea.creador_id != current_user.id:
        flash('No tienes permiso para eliminar esta tarea', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(tarea)
    db.session.commit()
    flash('Tarea eliminada exitosamente', 'success')
    return redirect(url_for('dashboard'))

@app.route('/tareas/<int:tarea_id>/cambiar_estado', methods=['POST'])
@login_required
def cambiar_estado_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    nuevo_status = request.json.get('status')
    
    if nuevo_status in ['pendiente', 'en_progreso', 'en_revision', 'completada']:
        tarea.status = nuevo_status
        db.session.commit()
        return jsonify({'success': True, 'mensaje': 'Estado actualizado'})
    
    return jsonify({'success': False, 'mensaje': 'Estado inválido'}), 400

# Rutas de usuarios (solo admin)
@app.route('/usuarios')
@login_required
def usuarios():
    if not current_user.es_admin:
        flash('No tienes permiso para acceder a esta página', 'error')
        return redirect(url_for('dashboard'))
    
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_usuario():
    if not current_user.es_admin:
        flash('No tienes permiso para acceder a esta página', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        es_admin = request.form.get('es_admin') == 'on'
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('nuevo_usuario.html')
        
        usuario = Usuario(nombre=nombre, email=email, es_admin=es_admin)
        usuario.set_password(password)
        
        db.session.add(usuario)
        db.session.commit()
        
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('usuarios'))
    
    return render_template('nuevo_usuario.html')

# API REST Endpoints para Tareas
@app.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """Crear una nueva tarea (POST /tasks)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({'error': 'El campo title es requerido'}), 400
        
        tarea = Tarea(
            title=data.get('title'),
            description=data.get('description'),
            priority=data.get('priority', 'media'),
            effort_hours=Decimal(str(data.get('effort_hours'))) if data.get('effort_hours') else None,
            status=data.get('status', 'pendiente'),
            assigned_to=data.get('assigned_to'),
            creador_id=current_user.id
        )
        
        # Validar prioridad
        if tarea.priority not in ['baja', 'media', 'alta', 'bloqueante']:
            return jsonify({'error': 'Prioridad inválida. Debe ser: baja, media, alta, bloqueante'}), 400
        
        # Validar status
        if tarea.status not in ['pendiente', 'en_progreso', 'en_revision', 'completada']:
            return jsonify({'error': 'Status inválido. Debe ser: pendiente, en_progreso, en_revision, completada'}), 400
        
        db.session.add(tarea)
        db.session.commit()
        
        return jsonify({
            'id': tarea.id,
            'title': tarea.title,
            'description': tarea.description,
            'priority': tarea.priority,
            'effort_hours': float(tarea.effort_hours) if tarea.effort_hours else None,
            'status': tarea.status,
            'assigned_to': tarea.assigned_to,
            'fecha_creacion': tarea.fecha_creacion.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/tasks', methods=['GET'])
@login_required
def get_all_tasks():
    """Obtener todas las tareas (GET /tasks)"""
    try:
        # Los administradores ven todas las tareas, los usuarios solo las asignadas a ellos
        if current_user.es_admin:
            tareas = Tarea.query.order_by(Tarea.fecha_creacion.desc()).all()
        else:
            tareas = Tarea.query.filter(
                Tarea.assigned_to == current_user.nombre
            ).order_by(Tarea.fecha_creacion.desc()).all()
        
        tasks_list = []
        for tarea in tareas:
            tasks_list.append({
                'id': tarea.id,
                'title': tarea.title,
                'description': tarea.description,
                'priority': tarea.priority,
                'effort_hours': float(tarea.effort_hours) if tarea.effort_hours else None,
                'status': tarea.status,
                'assigned_to': tarea.assigned_to,
                'fecha_creacion': tarea.fecha_creacion.isoformat()
            })
        
        return jsonify({
            'total': len(tasks_list),
            'tasks': tasks_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    """Obtener una tarea específica (GET /tasks/<id>)"""
    try:
        tarea = Tarea.query.get_or_404(task_id)
        
        # Verificar permisos: admin o usuario asignado o creador
        if not current_user.es_admin and tarea.assigned_to != current_user.nombre and tarea.creador_id != current_user.id:
            return jsonify({'error': 'No tienes permiso para acceder a esta tarea'}), 403
        
        return jsonify({
            'id': tarea.id,
            'title': tarea.title,
            'description': tarea.description,
            'priority': tarea.priority,
            'effort_hours': float(tarea.effort_hours) if tarea.effort_hours else None,
            'status': tarea.status,
            'assigned_to': tarea.assigned_to,
            'fecha_creacion': tarea.fecha_creacion.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Actualizar una tarea (PUT /tasks/<id>)"""
    try:
        tarea = Tarea.query.get_or_404(task_id)
        
        # Verificar permisos: admin o creador
        if not current_user.es_admin and tarea.creador_id != current_user.id:
            return jsonify({'error': 'No tienes permiso para actualizar esta tarea'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
        
        # Actualizar campos si están presentes
        if 'title' in data:
            tarea.title = data['title']
        
        if 'description' in data:
            tarea.description = data['description']
        
        if 'priority' in data:
            if data['priority'] not in ['baja', 'media', 'alta', 'bloqueante']:
                return jsonify({'error': 'Prioridad inválida. Debe ser: baja, media, alta, bloqueante'}), 400
            tarea.priority = data['priority']
        
        if 'effort_hours' in data:
            tarea.effort_hours = Decimal(str(data['effort_hours'])) if data['effort_hours'] else None
        
        if 'status' in data:
            if data['status'] not in ['pendiente', 'en_progreso', 'en_revision', 'completada']:
                return jsonify({'error': 'Status inválido. Debe ser: pendiente, en_progreso, en_revision, completada'}), 400
            tarea.status = data['status']
        
        if 'assigned_to' in data:
            tarea.assigned_to = data['assigned_to'] if data['assigned_to'] else None
        
        db.session.commit()
        
        return jsonify({
            'id': tarea.id,
            'title': tarea.title,
            'description': tarea.description,
            'priority': tarea.priority,
            'effort_hours': float(tarea.effort_hours) if tarea.effort_hours else None,
            'status': tarea.status,
            'assigned_to': tarea.assigned_to,
            'fecha_creacion': tarea.fecha_creacion.isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Eliminar una tarea (DELETE /tasks/<id>)"""
    try:
        tarea = Tarea.query.get_or_404(task_id)
        
        # Verificar permisos: admin o creador
        if not current_user.es_admin and tarea.creador_id != current_user.id:
            return jsonify({'error': 'No tienes permiso para eliminar esta tarea'}), 403
        
        db.session.delete(tarea)
        db.session.commit()
        
        return jsonify({
            'message': 'Tarea eliminada exitosamente',
            'id': task_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Inicializar base de datos
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)

