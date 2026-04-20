# Todo API

**📂 Project Path**: `python/web-frameworks/fastapi/todo-api/`  
**🔗 GitHub Repository**: [https://github.com/AmalieShi/amalie_projects](https://github.com/AmalieShi/amalie_projects)

A robust FastAPI-based todo list API with comprehensive CRUD operations, automatic timestamp tracking, and complete data validation.

## Features

- Add todo items with title and optional description
- Mark items as completed with automatic completion timestamps
- Remove items from the list
- View active todos with creation and modification dates
- View completed todos with completion dates
- Update existing todos (title, description, status)

## Project Structure

```
todo-api/
├── pyproject.toml                    # Project metadata and dependencies
├── README.md                         # Project documentation
├── test_api.py                       # API testing script
├── tests/                            # Test suite
└── src/
    └── fastapi_todo_list/
        ├── __init__.py              # Package initialization
        ├── main.py                  # FastAPI application and API endpoints
        ├── database.py              # Database setup and models
        ├── schemas.py               # Pydantic models for request/response
        ├── crud.py                  # Database operations
        └── config.py                # Configuration settings
```

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations  
- **SQLite**: Lightweight database for development
- **Uvicorn**: ASGI web server implementation
- **Pytest**: Testing framework

## Installation and Setup

1. Install the package in development mode:
   ```bash
   pip install -e .
   ```

2. Run the application:
   ```bash
   uvicorn src.fastapi_todo_list.main:app --reload
   ```

3. Access the API documentation:
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /` - Welcome message with endpoint overview
- `GET /todos` - Get all active todos
- `GET /todos/completed` - Get completed todos  
- `GET /todos/all` - Get all todos
- `GET /todos/{id}` - Get specific todo
- `POST /todos` - Create new todo
- `PUT /todos/{id}` - Update existing todo
- `DELETE /todos/{id}` - Delete todo

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run API tests:
```bash
python test_api.py
```

2. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Overview
- `GET /` - Welcome message with endpoint overview

### Todo Operations
- `GET /todos` - Get all active (incomplete) todos
- `GET /todos/completed` - Get all completed todos  
- `GET /todos/all` - Get all todos regardless of status
- `GET /todos/{id}` - Get a specific todo by ID
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update an existing todo
- `DELETE /todos/{id}` - Delete a todo

## Building & Distribution

### Build the Package
```bash
# Install build tools
pip install build twine

# Build the package
python -m build
```

This creates distribution files in the `dist/` directory:
- `fastapi_todo_list-1.0.0-py3-none-any.whl` (wheel)
- `fastapi_todo_list-1.0.0.tar.gz` (source distribution)

### Publish to Feed

#### **Option 1: PyPI (Public Registry)**
```bash
# Test PyPI (recommended first)
twine upload --repository testpypi dist/*

# Production PyPI  
twine upload dist/*
```

#### **Option 2: GitHub Packages**
```bash
# Configure GitHub token first
# Then upload to GitHub Packages
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

#### **Option 3: GitHub Releases**
```bash
# Manual upload to: https://github.com/amalieshi/amalie_projects/releases
# Or use GitHub CLI:
gh release create v1.0.0 dist/* --title "FastAPI Todo List v1.0.0"
```

#### **Option 4: Private Feed/Repository**
```bash
# Azure DevOps, JFrog Artifactory, Nexus, etc.
twine upload --repository-url https://your-private-feed-url dist/*
```

**Your GitHub Repository Feed URLs:**
- **Releases**: `https://github.com/amalieshi/amalie_projects/releases`
- **Repository**: `https://github.com/amalieshi/amalie_projects.git`  
- **Package Directory**: `python/web-frameworks/fastapi/`

### Development Tools
The project includes configuration for development tools:

```bash
# Code formatting with black
black src/

# Type checking with mypy
mypy src/

# Linting with flake8
flake8 src/

# Run tests
pytest
```

## Usage Examples

### Create a new todo
```bash
curl -X POST "http://localhost:8000/todos" \
     -H "Content-Type: application/json" \
     -d '{"title": "Buy groceries", "description": "Milk, bread, and eggs"}'
```

### Get all active todos
```bash
curl "http://localhost:8000/todos"
```

### Mark a todo as completed
```bash
curl -X PUT "http://localhost:8000/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
```

### Get completed todos
```bash
curl "http://localhost:8000/todos/completed"
```

### Delete a todo
```bash
curl -X DELETE "http://localhost:8000/todos/1"
```

## Data Model

Each todo item contains:
- `id`: Unique identifier (auto-generated)
- `title`: Todo title (required)
- `description`: Optional description
- `completed`: Boolean completion status
- `created_at`: Creation timestamp
- `updated_at`: Last modification timestamp
- `completed_at`: Completion timestamp (null if not completed)

## Database

The application uses SQLite with SQLAlchemy ORM for data persistence. The database file (`todos.db`) is created automatically when the application starts.

## Interactive Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test all endpoints directly from your browser.

## Development

To extend the application:
1. Add new database models in `database.py`
2. Create corresponding Pydantic schemas in `schemas.py`
3. Implement CRUD operations in `crud.py`
4. Add new endpoints in `main.py`

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type hints
- **SQLite**: Lightweight database engine
- **Uvicorn**: ASGI server for running the application