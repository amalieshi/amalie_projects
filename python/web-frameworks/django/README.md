# Todo API Orchestrator

A Django-based testing orchestration tool for the FastAPI Todo List API. This web application provides a user-friendly interface to manage, test, and interact with the FastAPI Todo List API.

## Features

- **Server Management**: Start and stop the FastAPI server with one-click buttons
- **Swagger UI Integration**: Direct access to the API's Swagger documentation
- **API Testing Interface**: Interactive forms to test all API endpoints
- **Real-time Response Display**: View API responses in a formatted, readable manner
- **Request History**: Keep track of previous API requests and responses

## Project Structure

```
django/
├── src/
│   └── todo_orchestrator/
│       ├── manage.py              # Django management script
│       ├── todo_orchestrator/     # Main Django project
│       │   ├── __init__.py
│       │   ├── settings.py        # Django settings
│       │   ├── urls.py           # Main URL configuration
│       │   └── wsgi.py           # WSGI configuration
│       └── testing/               # Testing orchestration app
│           ├── __init__.py
│           ├── admin.py
│           ├── apps.py
│           ├── models.py          # Data models for test history
│           ├── views.py           # Views for orchestration interface
│           ├── urls.py            # App URL configuration
│           ├── forms.py           # Forms for API testing
│           ├── utils.py           # Utility functions for server management
│           ├── templates/         # HTML templates
│           │   └── testing/
│           │       ├── base.html
│           │       ├── dashboard.html
│           │       └── api_test.html
│           └── static/            # CSS and JavaScript files
│               └── testing/
│                   ├── css/
│                   └── js/
├── pyproject.toml                 # Project configuration
├── README.md                      # This file
└── LICENSE                        # MIT License
```

## Installation

1. **Navigate to the project directory**:
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

- [FastAPI Todo List API](../fastapi/) - The API this orchestrator is designed to test