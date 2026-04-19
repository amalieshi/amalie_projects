# Todo API Orchestrator

## Development and Testing Tool

A comprehensive Django-based testing and orchestration platform designed for developers working with the FastAPI Todo List API. This tool provides advanced debugging, testing, and server management capabilities.

## Purpose

**Target Audience**: Developers, QA Engineers, API Testers  
**Use Case**: Development, testing, debugging, and API validation

## Key Features

### Server Management
- One-click FastAPI server control (start/stop)
- Real-time server status monitoring
- Process management with PID tracking
- Automatic server health checks

### Advanced API Testing
- Complete API testing suite for all endpoints
- Interactive forms for crafting custom requests
- Raw JSON request builder for advanced testing
- Response inspection with formatted display
- Request/response logging with detailed history

### Todo Management with Debugging
- Full CRUD operations with comprehensive debugging
- Real-time todo status updates
- Edit functionality with modal interfaces
- Completion tracking with detailed logging
- Error handling and troubleshooting tools

### Developer Dashboard
- API request logs with execution times
- Server performance metrics
- Swagger UI integration for API documentation
- Tabbed interface for organized workflow

## Technical Features

- Bootstrap 5 responsive interface
- Real-time status updates every 30 seconds
- Comprehensive error handling with detailed messages
- Debug logging throughout the application stack
- Request history with collapsible data views
- CSRF protection on all forms

## Getting Started

### Prerequisites
- Python 3.8+
- FastAPI Todo List API server
- Virtual environment activated

### Installation & Setup
```bash
# Navigate to project
cd todo-orchestrator

# Install dependencies from pyproject.toml
pip install -e .

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver 8001
```

### Usage
1. **Access the dashboard** at http://localhost:8001
2. **Start the FastAPI server** using the server controls
3. **Test API endpoints** using the testing interface
4. **Manage todos** with full debugging capabilities
5. **Monitor API logs** in the dedicated logs tab

## Dependencies

- **FastAPI Server**: Must be running on port 8000
- **Django 6.0.4**: Web framework
- **Bootstrap 5**: UI framework
- **Requests**: HTTP client for API communication
- **psutil**: System process management

## Default Ports

- **Todo Orchestrator**: http://localhost:8001
- **FastAPI Server**: http://localhost:8000 (managed by orchestrator)

---

**Note**: This is a development tool. For user-facing todo management, see the [todo-display](../todo-display/) project.