import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi_todo_list.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome to the Todo List API!" in data["message"]


def test_get_empty_todos():
    """Test getting todos when none exist"""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo():
    """Test creating a new todo"""
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test todo"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    return data["id"]


def test_get_todos_after_create():
    """Test getting todos after creating one"""
    # Create a todo first
    todo_data = {"title": "Another Test Todo", "description": "Another test"}
    create_response = client.post("/todos", json=todo_data)
    assert create_response.status_code == 201

    # Get all todos
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(todo["title"] == "Another Test Todo" for todo in data)


def test_update_todo():
    """Test updating a todo"""
    # Create a todo first
    todo_data = {"title": "Update Test Todo", "description": "To be updated"}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Update the todo
    update_data = {"title": "Updated Todo", "completed": True}
    response = client.put(f"/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["completed"] is True
    assert data["completed_at"] is not None


def test_delete_todo():
    """Test deleting a todo"""
    # Create a todo first
    todo_data = {"title": "Delete Test Todo", "description": "To be deleted"}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Delete the todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]

    # Verify it's deleted
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404


def test_get_completed_todos():
    """Test getting only completed todos"""
    # Create and complete a todo
    todo_data = {"title": "Completed Todo", "description": "This will be completed"}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Mark as completed
    client.put(f"/todos/{todo_id}", json={"completed": True})

    # Get completed todos
    response = client.get("/todos/completed")
    assert response.status_code == 200
    completed_todos = response.json()
    assert any(todo["id"] == todo_id for todo in completed_todos)


def test_app_import():
    """Test that the app can be imported"""
    from fastapi_todo_list import app

    assert app is not None


def test_app_metadata():
    """Test app metadata"""
    assert app.title == "Todo List API"
    assert app.version == "1.0.0"
