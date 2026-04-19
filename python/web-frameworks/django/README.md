# Django Web Applications

This directory contains multiple Django web applications for different purposes, each with its own `pyproject.toml` for dependency management.

## Project Structure

```
django/
├── todo-orchestrator/          # Developer testing & management tool
│   ├── pyproject.toml         # Dependencies & project config
│   ├── manage.py              # Django management
│   ├── todo_orchestrator/     # Main Django project
│   └── testing/               # Django app
├── todo-display/               # User-focused todo interface  
│   ├── pyproject.toml         # Dependencies & project config
│   ├── manage.py              # Django management
│   ├── todo_display/          # Main Django project
│   └── display/               # Django app
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Projects

### 1. todo-orchestrator (Developer Tool)
**Purpose**: Full-featured Django app for testing and managing the FastAPI Todo List API
- Server management (start/stop FastAPI)
- API testing interface with request logging
- Todo CRUD operations with debugging
- Real-time todo management with completion tracking
- Edit functionality for existing todos

**Port**: 8001 (by default)
**Dependencies**: FastAPI server running on port 8000

### 2. todo-display (User Interface)
**Purpose**: Lightweight Django app for displaying todos in read-only mode
- Clean, simple interface for viewing todos
- Beautiful, responsive design
- Filter and search functionality
- One-click todo completion
- Mobile-optimized user experience

**Port**: 8002 (by default)
**Dependencies**: FastAPI server running on port 8000

## Getting Started

### Prerequisites
- Python 3.9+
- Virtual environment activated
- FastAPI Todo List API server available

### Running Projects

**Todo Orchestrator (Developers):**
```bash
cd todo-orchestrator
pip install -e .                # Install from pyproject.toml
python manage.py migrate         # Set up database
python manage.py runserver 8001  # Start on port 8001
```

**Todo Display (End Users):**
```bash
cd todo-display  
pip install -e .                # Install from pyproject.toml
python manage.py migrate         # Set up database
python manage.py runserver 8002  # Start on port 8002
```

### Dependency Management

Each project uses modern **pyproject.toml** for dependency management:
- **No requirements.txt files** - everything is in pyproject.toml
- **Install with**: `pip install -e .` (editable install)
- **Dev dependencies**: `pip install -e .[dev]` (if available)

## Adding New Django Projects

To add a new Django project:

1. **Create the project:**
   ```bash
   cd /path/to/django/
   django-admin startproject your_project_name
   ```

2. **Follow the naming convention:**
   - Use descriptive, hyphenated names
   - Examples: `user-management`, `blog-cms`, `analytics-dashboard`

3. **Create pyproject.toml** with dependencies and project metadata

4. **Use unique ports** (8001, 8002, 8003, etc.)

5. **Update this README** with project details

## Development Tips

- Each project is **completely independent** - separate dependencies, databases, settings
- Use **different ports** to run multiple projects simultaneously  
- **pyproject.toml is sufficient** - no need for requirements.txt
- Consider **environment variables** for configuration differences between projects

## Dependencies

Both projects depend on:
- **FastAPI Server**: http://localhost:8000 (managed/consumed by Django apps)
- **Django 6.0+**: Web framework
- **Bootstrap 5**: UI framework
- **Requests**: HTTP client for API communication
   ```bash
   cd python/web-frameworks/django
   ```

2. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

   Or install with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

   Or install with FastAPI server dependencies (recommended):
   ```bash
   pip install -e ".[fastapi-server]"
   ```

   Or install with both development and FastAPI server dependencies:
   ```bash
   pip install -e ".[dev,fastapi-server]"
   ```

## Usage

### Starting the Django Application

1. **Initialize the database**:
   ```bash
   cd src/todo_orchestrator
   python manage.py migrate
   ```

2. **Create a superuser (optional)**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the application**:
   Open your browser and go to `http://localhost:8080`

### Using the Orchestrator

1. **Dashboard**: The main page provides an overview and quick access to all features
2. **Server Controls**: Use the "Start FastAPI Server" and "Stop FastAPI Server" buttons to manage the todo API
3. **Swagger UI**: Click "Open Swagger UI" to access the interactive API documentation
4. **API Testing**: Navigate to the "Test API" tab to:
   - Create new todos
   - Retrieve todos (all, active, completed, or specific)
   - Update existing todos
   - Delete todos

### API Endpoints Supported

The orchestrator supports testing all FastAPI todo endpoints:

- `GET /` - Welcome message and endpoint overview
- `GET /todos` - Get all active todos
- `GET /todos/completed` - Get completed todos
- `GET /todos/all` - Get all todos
- `GET /todos/{id}` - Get specific todo by ID
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update an existing todo
- `DELETE /todos/{id}` - Delete a todo

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
isort src/
flake8 src/
```

### Type Checking

```bash
mypy src/
```

## Configuration

The Django application runs on port 8080 by default to avoid conflicts with the FastAPI server (port 8000). You can modify this in the Django settings or by specifying a different port:

```bash
python manage.py runserver 0.0.0.0:8080
```

## Dependencies

### Main Dependencies
- **Django**: Web framework for the orchestration interface
- **requests**: HTTP library for making API calls to FastAPI
- **psutil**: System process management for server control
- **django-cors-headers**: CORS handling for API interactions
- **django-bootstrap5**: Bootstrap integration for UI

### Development Dependencies
- **pytest**: Testing framework
- **pytest-django**: Django integration for pytest
- **black**: Code formatter
- **flake8**: Linting tool
- **isort**: Import sorting
- **mypy**: Type checking

### FastAPI Server Dependencies
These dependencies are required to run the FastAPI Todo List server that this orchestrator manages:
- **fastapi**: Modern, fast web framework for building APIs
- **uvicorn**: Lightning-fast ASGI server
- **sqlalchemy**: Python SQL toolkit and Object-Relational Mapping (ORM)
- **pydantic**: Data validation using Python type annotations
- **python-dateutil**: Extensions to the standard Python datetime module

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [FastAPI Todo List API](../fastapi/todo-api/) - The API this orchestrator is designed to test