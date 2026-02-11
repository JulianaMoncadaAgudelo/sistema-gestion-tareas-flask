# Task Management System

A full-stack web application built with Flask that provides comprehensive task management capabilities with user authentication, role-based access control, and a RESTful API. The system allows teams to create, assign, track, and manage tasks efficiently through an intuitive web interface.

## Overview

This project demonstrates proficiency in building complete web applications with modern architectural patterns. The application implements security best practices, follows RESTful API design principles, and uses object-oriented programming patterns throughout.

### Project Versions

The project includes two distinct implementations:

#### 1. Simplified Version (JSON-based API)
- **File**: `app_simple.py`
- **Storage**: JSON file (`tasks.json`)
- **Architecture**: Clean separation with Task and TaskManager classes
- **Purpose**: Demonstrates API design and OOP principles
- **Features**: Full REST API without authentication layer

#### 2. Full-Featured Version (Complete Web Application)
- **File**: `app.py`
- **Storage**: SQLite database with SQLAlchemy ORM
- **Architecture**: MVC pattern with Blueprint organization
- **Purpose**: Production-ready web application
- **Features**: Web interface, user authentication, role-based access control, and API endpoints

## Key Features

### User Management
- Secure user registration and authentication system
- Password hashing using Werkzeug security utilities
- Role-based access control (Administrator and Regular User roles)
- Session management with Flask-Login
- First registered user automatically receives administrator privileges

### Task Management
- Complete CRUD operations for tasks
- Task assignment to team members
- Four-stage workflow: Pending, In Progress, Under Review, Completed
- Priority levels: Low, Medium, High, Blocking
- Effort estimation tracking (decimal hours)
- Task filtering based on user role and assignment
- Real-time status updates via AJAX

### Dashboard and Analytics
- Comprehensive dashboard with task statistics
- Visual organization by status and priority
- Task summary metrics (total, pending, in progress, under review, completed)
- Responsive design for mobile and desktop viewing

### RESTful API
- Full REST API implementation for programmatic access
- JSON-based data exchange
- CRUD endpoints for task operations
- Authentication-protected endpoints
- Permission-based access control

## Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0.0**: Web framework for routing and request handling
- **Flask-SQLAlchemy**: ORM for database operations (full version)
- **Flask-Login**: User session management and authentication (full version)
- **SQLite**: Lightweight relational database (full version)
- **JSON**: File-based storage (simplified version)
- **Werkzeug**: Password hashing and security utilities

### Frontend
- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with responsive design
- **JavaScript (Vanilla)**: Client-side interactivity and AJAX requests
- **Jinja2**: Server-side templating engine

### Architecture
- **MVC Pattern**: Separation of concerns with models, views, and controllers
- **Blueprint Pattern**: Modular route organization
- **Object-Oriented Design**: Task and TaskManager classes with clear responsibilities
- **Repository Pattern**: TaskManager class abstracts data persistence logic

## Core Components

### Task Class (`models/task.py`)

The `Task` class represents a task entity with all required attributes.

**Attributes:**
- `id`: Primary key identifier
- `title`: Task title (required)
- `description`: Detailed task description (text)
- `priority`: Priority level (baja, media, alta, bloqueante)
- `effort_hours`: Estimated effort in decimal hours
- `status`: Current status (pendiente, en_progreso, en_revision, completada)
- `assigned_to`: Name of the team member assigned (string)
- `fecha_creacion`: Creation timestamp

**Key Methods:**

```python
# Convert Task object to dictionary
task_dict = task.to_dict()

# Create Task object from dictionary
task = Task.from_dict(data)

# Validate task data
is_valid, error_message = task.validate()
```

### TaskManager Class (`managers/task_manager.py`)

The `TaskManager` class handles all data persistence operations for the simplified version, managing the JSON file storage.

**Static Methods:**

```python
# Load all tasks from tasks.json
tasks = TaskManager.load_tasks()  # Returns: List[Task]

# Save tasks to tasks.json
TaskManager.save_tasks(tasks)  # Returns: bool

# Get next available ID
next_id = TaskManager.get_next_id()  # Returns: int

# Get task by ID
task = TaskManager.get_task_by_id(task_id)  # Returns: Task or None

# Add new task
success = TaskManager.add_task(task)  # Returns: bool

# Update existing task
success = TaskManager.update_task(task_id, updated_task)  # Returns: bool

# Delete task
success = TaskManager.delete_task(task_id)  # Returns: bool
```

### Route Organization (`routes/task_routes.py`)

All task-related API endpoints are organized in a Flask Blueprint. Each route calls the appropriate TaskManager method, demonstrating separation of concerns.

**Blueprint Registration:**
```python
from routes.task_routes import task_bp
app.register_blueprint(task_bp)
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sistema-gestion-tareas-flask.git
cd sistema-gestion-tareas-flask
```

2. Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Additional required packages for the full version:
```bash
pip install Flask-SQLAlchemy Flask-Login
```

The `requirements.txt` file includes:
- Flask==3.0.0
- requests==2.31.0 (for API testing)

## Running the Application

### Option 1: Simplified API Version (Recommended for Learning)

The simplified version uses JSON file storage and focuses on API design:

```bash
python app_simple.py
```

- No authentication required
- Data stored in `tasks.json` (created automatically)
- Perfect for testing API endpoints
- Clean implementation of OOP principles
- Available at `http://localhost:5000`

### Option 2: Full Web Application

The complete version includes web interface and database:

```bash
python app.py
```

- User authentication required
- SQLite database (`tareas.db` created automatically)
- Full web interface with dashboard
- Role-based access control
- Available at `http://localhost:5000`

**First Run Setup:**
- Database is automatically initialized
- Register first user (becomes admin automatically)
- Start creating and managing tasks

## Usage Examples

### Testing the Simplified API (No Authentication)

The simplified version (`app_simple.py`) provides unauthenticated API access, perfect for testing and learning.

#### 1. Create a Task
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar API",
    "description": "Crear endpoints REST",
    "priority": "alta",
    "effort_hours": 8.5,
    "status": "pendiente",
    "assigned_to": "Juan Pérez"
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Implementar API",
  "description": "Crear endpoints REST",
  "priority": "alta",
  "effort_hours": 8.5,
  "status": "pendiente",
  "assigned_to": "Juan Pérez",
  "fecha_creacion": "2024-01-15T10:30:00"
}
```

#### 2. Get All Tasks
```bash
curl http://localhost:5000/tasks
```

**Response (200):**
```json
{
  "total": 1,
  "tasks": [
    {
      "id": 1,
      "title": "Implementar API",
      "description": "Crear endpoints REST",
      "priority": "alta",
      "effort_hours": 8.5,
      "status": "pendiente",
      "assigned_to": "Juan Pérez",
      "fecha_creacion": "2024-01-15T10:30:00"
    }
  ]
}
```

#### 3. Get Specific Task
```bash
curl http://localhost:5000/tasks/1
```

#### 4. Update a Task
```bash
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tarea actualizada",
    "status": "en_progreso"
  }'
```

#### 5. Delete a Task
```bash
curl -X DELETE http://localhost:5000/tasks/1
```

**Response (200):**
```json
{
  "message": "Tarea eliminada exitosamente",
  "id": 1
}
```

### Using the Full Web Application

#### Web Interface Usage

1. **Register a New User**
   - Navigate to `http://localhost:5000/register`
   - Fill in name, email, and password
   - First user registered becomes an administrator automatically

2. **Create a Task**
   - Log in to the dashboard
   - Click "Nueva Tarea" (New Task)
   - Fill in task details:
     - Title (required)
     - Description
     - Priority: Low, Medium, High, or Blocking
     - Effort hours (decimal, e.g., 8.5)
     - Status: Pending, In Progress, Under Review, or Completed
     - Assign to team member (by name)

3. **Manage Tasks**
   - View all tasks on the dashboard
   - Update task status directly from cards
   - Edit task details by clicking the edit icon
   - Delete tasks using the delete button

#### API Usage (Authentication Required)

The full version requires authentication via Flask-Login session cookies. All endpoints require login.

### Valid Values

**Priority Levels:**
- `baja` (Low)
- `media` (Medium)
- `alta` (High)
- `bloqueante` (Blocking)

**Status Options:**
- `pendiente` (Pending)
- `en_progreso` (In Progress)
- `en_revision` (Under Review)
- `completada` (Completed)

## Project Structure

```
sistema-gestion-tareas-flask/
│
├── app.py                      # Full application with web interface and API
├── app_simple.py              # Simplified JSON-based API version
├── requirements.txt           # Python dependencies
├── SETUP.md                   # Detailed setup instructions
├── INTERFAZ.md                # Interface documentation
│
├── tasks.json                 # JSON data storage (created automatically)
├── tareas.db                  # SQLite database (created automatically)
│
├── models/                    # Data models
│   ├── __init__.py
│   └── task.py               # Task class with to_dict() and from_dict()
│
├── managers/                  # Business logic layer
│   ├── __init__.py
│   └── task_manager.py       # TaskManager with load_tasks() and save_tasks()
│
├── routes/                    # API route blueprints
│   ├── __init__.py
│   └── task_routes.py        # REST endpoints using TaskManager
│
├── templates/                 # HTML templates (Jinja2)
│   ├── base.html             # Base template with common layout
│   ├── login.html            # User login page
│   ├── register.html         # User registration page
│   ├── dashboard.html        # Main dashboard view
│   ├── nueva_tarea.html      # Create new task form
│   ├── editar_tarea.html     # Edit task form
│   ├── usuarios.html         # User management (admin only)
│   └── nuevo_usuario.html    # Create new user form (admin only)
│
├── static/                    # Static assets
│   ├── css/
│   │   └── style.css         # Application styles
│   ├── js/
│   │   └── main.js           # Client-side JavaScript
│   ├── app.js                # Additional JavaScript
│   ├── style.css             # Additional styles
│   └── index.html            # Static landing page
│
├── demo_api.py               # API testing script (full version)
├── demo_api_simple.py        # API testing script (simple version)
└── test_api.py               # Unit tests for API endpoints
```

## Technical Implementation Details

### Requirements Compliance

This project demonstrates adherence to software engineering best practices:

**1. Virtual Environment and Dependencies**
- Virtual environment setup instructions provided
- `requirements.txt` with pinned versions
- Clear installation steps for reproducibility

**2. Task Class Implementation**
- Complete data model with all required fields
- `to_dict()` method for serialization
- `from_dict()` class method for deserialization
- `validate()` method for data integrity

**3. TaskManager Class**
- Static methods for stateless operations
- `load_tasks()`: Loads from JSON and returns List[Task]
- `save_tasks(tasks)`: Persists Task objects to JSON
- Additional helper methods for CRUD operations

**4. Separated Route Architecture**
- Dedicated `routes/task_routes.py` file
- Blueprint pattern for modular organization
- All routes delegate to TaskManager methods
- Clear separation of concerns

**5. Complete REST API**
- GET `/tasks` - List all tasks
- GET `/tasks/<id>` - Get specific task
- POST `/tasks` - Create new task
- PUT `/tasks/<id>` - Update existing task
- DELETE `/tasks/<id>` - Remove task

## Database Schema

### User Model
- `id`: Integer, Primary Key
- `nombre`: String (100 characters), User's full name
- `email`: String (100 characters), Unique, Email address
- `password_hash`: String (255 characters), Hashed password
- `es_admin`: Boolean, Administrator flag
- `fecha_creacion`: DateTime, Registration timestamp

### Task Model
- `id`: Integer, Primary Key
- `title`: String (200 characters), Task title
- `description`: Text, Detailed task description
- `priority`: String (20 characters), Priority level
- `effort_hours`: Numeric (10, 2), Estimated hours
- `status`: String (20 characters), Current status
- `assigned_to`: String (100 characters), Assigned team member name
- `creador_id`: Integer, Foreign Key to User
- `fecha_creacion`: DateTime, Creation timestamp

## Security Features

- **Password Security**: All passwords are hashed using Werkzeug's security utilities before storage
- **Session Management**: Secure session handling with Flask-Login
- **CSRF Protection**: Built-in Flask CSRF protection for forms
- **Authorization**: Role-based access control for administrative functions
- **Permission Checks**: Users can only modify tasks they created or are assigned to (unless admin)
- **SQL Injection Prevention**: SQLAlchemy ORM provides parameterized queries

## Development Notes

### Configuration
- Secret key is defined in `app.py` - change in production
- Database URI is configurable via `SQLALCHEMY_DATABASE_URI`
- Debug mode is enabled by default - disable in production

### Testing and Demos

The project includes automated testing scripts:

```bash
# Test simplified version (no authentication needed)
python demo_api_simple.py

# Test full version (requires running server and authentication)
python demo_api.py

# Run unit tests
python test_api.py
```

**Demo Scripts Functionality:**
- Automated testing of all CRUD operations
- Creates sample tasks with various priorities and statuses
- Tests error handling and validation
- Verifies JSON serialization and deserialization

## Future Improvements

### Enhanced Features
- Email notifications for task assignments and status changes
- File attachment support for tasks
- Task comments and activity history
- Advanced filtering and search functionality
- Task dependencies and subtasks
- Calendar view and deadline tracking
- Export functionality (PDF, CSV)

### Technical Enhancements
- Migration to PostgreSQL for production deployment
- JWT-based API authentication for stateless requests
- Comprehensive test suite with unit and integration tests
- Docker containerization for easy deployment
- CI/CD pipeline integration
- API documentation with Swagger/OpenAPI
- Rate limiting and request throttling
- Caching layer for improved performance
- Real-time updates using WebSockets

### User Experience
- Dark mode support
- Drag-and-drop task organization
- Bulk operations for tasks
- Customizable dashboard widgets
- Advanced analytics and reporting
- Mobile application (React Native or Flutter)

## Deployment Considerations

For production deployment:

1. Change the `SECRET_KEY` to a strong, random value
2. Use environment variables for sensitive configuration
3. Switch to a production-grade database (PostgreSQL, MySQL)
4. Enable HTTPS/SSL
5. Configure proper logging and error handling
6. Set up database backups
7. Use a production WSGI server (Gunicorn, uWSGI)
8. Implement rate limiting and request validation
9. Set up monitoring and alerting

## Contributing

This project is part of a portfolio demonstrating full-stack web development capabilities. Contributions, issues, and feature requests are welcome.

## License

This project is available for educational and portfolio purposes.

## Contact

For questions or collaboration opportunities, please reach out through GitHub.
