
Python Web-Frameworks Projects  
==============================

This section showcases all python web-frameworks projects with their documentation and source code.

.. admonition:: Navigation Tip
   :class: tip

   Click on any project card to view its complete documentation, or use the dropdown to preview key information.



**Projects in this Category**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1
   :caption: Python Web-Frameworks Projects
   :hidden:

   python_web-frameworks_django_django_todo_display
   python_web-frameworks_django_django_todo_orchestrator
   python_web-frameworks_fastapi_fastapi_todo_api


.. grid:: 1 2 2 2
   :gutter: 3
   :margin: 2

   .. grid-item-card:: Django Web Applications
      :link: python_web-frameworks_django
      :link-type: doc
      :class-card: project-card
      :text-align: left

      This directory contains multiple Django web applications for different purposes, each with its own `pyproject.toml` for dependency management.
   
   :bdg-secondary:`Django`
   :bdg-secondary:`FastAPI`
   :bdg-secondary:`PyTest`
   :bdg-secondary:`Python`
      
      +++
      
      .. button-link:: python_web-frameworks_django
         :color: primary
         :outline:
         :expand:
         
         View Details →

   .. grid-item-card:: FastAPI Web Applications
      :link: python_web-frameworks_fastapi
      :link-type: doc
      :class-card: project-card
      :text-align: left

      This directory contains FastAPI web applications showcasing modern Python web API development, each with its own `pyproject.toml` for dependency management.
   
   :bdg-secondary:`Django`
   :bdg-secondary:`FastAPI`
   :bdg-secondary:`PyTest`
   :bdg-secondary:`Python`
   :bdg-secondary:`SQLite`
      
      +++
      
      .. button-link:: python_web-frameworks_fastapi
         :color: primary
         :outline:
         :expand:
         
         View Details →

   .. grid-item-card:: Todo Display
      :link: python_web-frameworks_django_django_todo_display
      :link-type: doc
      :class-card: project-card
      :text-align: left

      **📂 Project Path**: `python/web-frameworks/django/todo-display/`
   
   :bdg-secondary:`Django`
   :bdg-secondary:`FastAPI`
   :bdg-secondary:`Python`
   :bdg-secondary:`Testing`
      
      +++
      
      .. button-link:: python_web-frameworks_django_django_todo_display
         :color: primary
         :outline:
         :expand:
         
         View Details →

   .. grid-item-card:: Todo API Orchestrator
      :link: python_web-frameworks_django_django_todo_orchestrator
      :link-type: doc
      :class-card: project-card
      :text-align: left

      **📂 Project Path**: `python/web-frameworks/django/todo-orchestrator/`
   
   :bdg-secondary:`Django`
   :bdg-secondary:`FastAPI`
   :bdg-secondary:`Python`
   :bdg-secondary:`Testing`
      
      +++
      
      .. button-link:: python_web-frameworks_django_django_todo_orchestrator
         :color: primary
         :outline:
         :expand:
         
         View Details →

   .. grid-item-card:: Todo API
      :link: python_web-frameworks_fastapi_fastapi_todo_api
      :link-type: doc
      :class-card: project-card
      :text-align: left

      **📂 Project Path**: `python/web-frameworks/fastapi/todo-api/`
   
   :bdg-secondary:`FastAPI`
   :bdg-secondary:`PyTest`
   :bdg-secondary:`Python`
   :bdg-secondary:`SQLite`
      
      +++
      
      .. button-link:: python_web-frameworks_fastapi_fastapi_todo_api
         :color: primary
         :outline:
         :expand:
         
         View Details →



**Quick Preview**
^^^^^^^^^^^^^^^^^^

.. tab-set::


   .. tab-item:: Django Web Applications

      This directory contains multiple Django web applications for different purposes, each with its own `pyproject.toml` for dependency management.
      
      **Technologies:** Django, FastAPI, PyTest, Python
      
      .. dropdown:: Quick Preview
         :color: info
         :icon: book

         This directory contains multiple Django web applications for different purposes, each with its own `pyproject.toml` for dependency management.

Project Structure
-----------------


.. code-block:: text

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

Projects
--------


1. todo-orchestrator (Developer Tool)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Purpose**: Full-featured Django app for testing and managing the FastAPI Todo List API
- Server management (start/stop FastAPI)
- API testing interface with request logging
- Todo CRUD operations with debugging
- Real-time todo management with completion tracking
- Edit functionality for existing todos
**Port**: 8001 (by default)
**Dependencies**: FastAPI server running on port 8000

2. todo-display (User Interface)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Purpose**: Lightweight Django app for displaying todos in read-only mode
- Clean, simple interface for viewing todos
- Beautiful, responsive design
- Filter and search functionality
- One-click todo completion
- Mobile-optimized user experience
**Port**: 8002 (by default)
**Dependencies**: FastAPI server running on port 8000

Getting Started
---------------


Prerequisites
^^^^^^^^^^^^^

- Python 3.9+
         
         :doc:`View Full Documentation → <python_web-frameworks_django>`


   .. tab-item:: FastAPI Web Applications

      This directory contains FastAPI web applications showcasing modern Python web API development, each with its own `pyproject.toml` for dependency management.
      
      **Technologies:** Django, FastAPI, PyTest, Python, SQLite
      
      .. dropdown:: Quick Preview
         :color: info
         :icon: book

         This directory contains FastAPI web applications showcasing modern Python web API development, each with its own `pyproject.toml` for dependency management.

Project Structure
-----------------


.. code-block:: text

   fastapi/
   ├── todo-api/                   # Todo List API service
   │   ├── pyproject.toml         # Dependencies & project config
   │   ├── src/fastapi_todo_list/ # Main FastAPI application
   │   ├── tests/                 # Test suite
   │   ├── build_package.py       # Package building utilities
   │   └── README.md              # Project documentation
   ├── LICENSE                     # MIT License
   └── README.md                   # This file

Projects
--------


1. todo-api (Main API Service)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Purpose**: A robust FastAPI-based todo list API with full CRUD operations
- FastAPI with automatic OpenAPI documentation
- SQLAlchemy ORM with SQLite database
- Pydantic models for data validation
- Comprehensive CRUD operations with timestamps
- Full test coverage with pytest
- Automatic completion timestamp tracking

Technologies Used
-----------------

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database for development
- **Uvicorn**: ASGI web server implementation
- **Pytest**: Testing framework

Quick Start
-----------

Each project can be run independently with its own dependencies:

.. code-block:: text

   cd todo-api
   pip install -e .
   uvicorn src.fastapi_todo_list.main:app --reload
Visit `http://localhost:8000/docs` for interactive API documentation.

Development Notes
-----------------

- All projects use modern `pyproject.toml` configuration
- Code follows FastAPI best practices and patterns
         
         :doc:`View Full Documentation → <python_web-frameworks_fastapi>`

