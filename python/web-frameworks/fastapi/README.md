# FastAPI Todo List Package

A simple and efficient todo list API built with FastAPI, featuring full CRUD operations with timestamps for creation, updates, and completion tracking. Packaged for easy distribution and deployment to feeds.

## Features

- ✅ **Add todo items** with title and optional description
- ✅ **Mark items as completed** with automatic completion timestamps
- ✅ **Remove items** from the list
- ✅ **View active todos** with creation and modification dates
- ✅ **View completed todos** with completion dates
- ✅ **Update existing todos** (title, description, status)

## Project Structure

```
fastapi/
├── pyproject.toml                    # Project metadata and dependencies
├── README.md                        # Project documentation
├── test_api.py                      # API testing script
├── tests/                           # Test suite
└── src/
    └── fastapi_todo_list/
        ├── __init__.py             # Package initialization
        ├── main.py                 # FastAPI application and API endpoints
        ├── database.py             # Database setup and models
        ├── schemas.py              # Pydantic models for request/response
        ├── crud.py                 # Database operations
        └── config.py               # Configuration settings
```

## 🚀 Automated CI/CD

This repository includes automated workflows for building, testing, and publishing the FastAPI Todo List package.

### 🔄 Workflows

#### 1. **Continuous Integration** (`ci-fastapi-todo.yml`)
- **Triggers:** Push/PR to main branches, changes in `python/web-frameworks/fastapi/`
- **Actions:** 
  - Tests on Python 3.8-3.12 across Ubuntu/Windows/macOS
  - Code linting with flake8
  - Security scanning with safety & pip-audit
  - Package build verification

#### 2. **Build, Tag & Publish** (`publish-fastapi-todo.yml`)
- **Triggers:** Push to main/master branch, manual dispatch
- **Actions:**
  - Version detection from `pyproject.toml`
  - Automatic Git tagging
  - Package building and testing
  - PyPI publication
  - GitHub Release creation
  - Artifact upload

### 🔐 Required Secrets & Configuration

#### For PyPI Publishing

##### Option A: Trusted Publishing (Recommended)
1. **Configure PyPI Trusted Publishing:**
   - Go to [PyPI](https://pypi.org/) → Account Settings → Publishing
   - Add publisher: `amalieshi/amalie_projects` 
   - Workflow: `publish-fastapi-todo.yml`
   - Environment: `pypi`

##### Option B: API Token
1. **Create PyPI API Token:**
   - Go to [PyPI](https://pypi.org/) → Account Settings → API Tokens
   - Create token for `todolist_fastapi` project
   
2. **Add GitHub Secret:**
   ```
   Repository Settings → Secrets → Actions → New repository secret
   Name: PYPI_API_TOKEN
   Value: pypi-your-token-here
   ```

3. **Update workflow** (uncomment line in `publish-fastapi-todo.yml`):
   ```yaml
   password: ${{ secrets.PYPI_API_TOKEN }}
   ```

#### For GitHub Releases
- **No configuration needed** - uses `GITHUB_TOKEN` automatically

### 🚀 How It Works

#### Automatic Publishing
1. **Edit version** in `python/web-frameworks/fastapi/pyproject.toml`
2. **Commit & push** to main branch
3. **Workflow automatically:**
   - Detects version change
   - Creates Git tag (e.g., `v1.0.1`)
   - Builds package
   - Publishes to PyPI
   - Creates GitHub Release

#### Manual Publishing
1. **Go to:** `Actions` → `Build, Tag, and Publish FastAPI Todo Package`
2. **Click:** `Run workflow`
3. **Choose:** Force publish option if needed

### 📋 Version Management

The workflows automatically read the version from:
```toml
# python/web-frameworks/fastapi/pyproject.toml
[project]
version = "1.0.1"  # ← Update this to trigger new release
```

#### Version Bump Examples:
```bash
# Patch release (1.0.0 → 1.0.1)
sed -i 's/version = "1\.0\.0"/version = "1.0.1"/' python/web-frameworks/fastapi/pyproject.toml

# Minor release (1.0.1 → 1.1.0)  
sed -i 's/version = "1\.0\.1"/version = "1.1.0"/' python/web-frameworks/fastapi/pyproject.toml

# Major release (1.1.0 → 2.0.0)
sed -i 's/version = "1\.1\.0"/version = "2.0.0"/' python/web-frameworks/fastapi/pyproject.toml
```

### 🎯 Workflow Status

#### ✅ What's Configured
- Automated testing on multiple Python versions
- Cross-platform compatibility testing (Linux/Windows/macOS)
- Security scanning
- Automatic Git tagging
- PyPI publishing (with trusted publishing)
- GitHub Release creation
- Package artifact uploads

#### 🔄 Manual Steps Required
1. **Set up PyPI trusted publishing** (one-time setup)
2. **Update version in pyproject.toml** (per release)
3. **Commit and push** (triggers automatic publishing)

### 📊 Monitoring

- **Check workflow status:** `Actions` tab in GitHub
- **View releases:** `Releases` tab in GitHub  
- **Monitor PyPI:** https://pypi.org/project/todolist_fastapi/
- **View logs:** Click on any workflow run for detailed logs

### 🛠️ Troubleshooting

#### Common Issues:
1. **Version already exists** → Bump version in pyproject.toml
2. **PyPI authentication fails** → Check trusted publishing or API token
3. **Tests fail** → Fix code and re-push
4. **Security warnings** → Update vulnerable dependencies

#### Debug Commands:
```bash
# Test locally before pushing
cd python/web-frameworks/fastapi
python -m pytest tests/
python -m build
twine check dist/*
```

## Installation & Setup

### Development Installation
1. **Clone and install in development mode:**
   ```bash
   cd todolist-fastapi
   pip install -e .
   ```

2. **Install with development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

### Package Installation from Feed
1. **Install from PyPI or private feed:**
   ```bash
   pip install todolist_fastapi
   ```

2. **Run using the installed command:**
   ```bash
   todo-api
   ```

### Direct Development Run
1. **Run from source:**
   ```bash
   python -m src.fastapi_todo_list.main
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn src.fastapi_todo_list.main:app --reload --host 0.0.0.0 --port 8000
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