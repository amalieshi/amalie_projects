#!/usr/bin/env python3
"""
Simple test script to demonstrate the Todo List API functionality.
Make sure the FastAPI server is running before executing this script.

Run the server with:
    python -m src.fastapi_todo_list.main
    OR
    todo-api (if installed as package)
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def print_response(response, title):
    """Helper function to print formatted response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    if response.status_code < 400:
        print("Response:")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print(f"Error: {response.text}")


def test_todo_api():
    """Test all the todo API endpoints"""

    print("Starting Todo List API Test...")

    # 1. Get welcome message
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "1. Welcome Message")

    # 2. Create some todos
    todos_to_create = [
        {"title": "Buy groceries", "description": "Milk, bread, and eggs"},
        {"title": "Walk the dog", "description": "30 minute walk in the park"},
        {"title": "Read a book", "description": "Finish chapter 5"},
        {"title": "Call mom", "description": "Check how she's doing"},
        {"title": "Workout", "description": "45 minutes at the gym"},
    ]

    created_todos = []
    for todo in todos_to_create:
        response = requests.post(f"{BASE_URL}/todos", json=todo)
        print_response(response, f"2. Create Todo: {todo['title']}")
        if response.status_code == 201:
            created_todos.append(response.json())

    # 3. Get all active todos
    response = requests.get(f"{BASE_URL}/todos")
    print_response(response, "3. Get Active Todos")

    # 4. Mark some todos as completed
    if len(created_todos) >= 2:
        # Complete the first two todos
        for i in range(2):
            todo_id = created_todos[i]["id"]
            response = requests.put(
                f"{BASE_URL}/todos/{todo_id}", json={"completed": True}
            )
            print_response(response, f"4. Mark Todo {todo_id} as Completed")

    # 5. Get completed todos
    response = requests.get(f"{BASE_URL}/todos/completed")
    print_response(response, "5. Get Completed Todos")

    # 6. Get active todos (should show remaining incomplete ones)
    response = requests.get(f"{BASE_URL}/todos")
    print_response(response, "6. Get Active Todos (After Completions)")

    # 7. Update a todo's title and description
    if len(created_todos) >= 3:
        todo_id = created_todos[2]["id"]
        response = requests.put(
            f"{BASE_URL}/todos/{todo_id}",
            json={"title": "Read two books", "description": "Finish chapters 5 and 6"},
        )
        print_response(response, f"7. Update Todo {todo_id}")

    # 8. Get all todos (completed and active)
    response = requests.get(f"{BASE_URL}/todos/all")
    print_response(response, "8. Get All Todos")

    # 9. Delete a todo
    if len(created_todos) >= 1:
        todo_id = created_todos[-1]["id"]
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
        print_response(response, f"9. Delete Todo {todo_id}")

    # 10. Final state - get all todos
    response = requests.get(f"{BASE_URL}/todos/all")
    print_response(response, "10. Final State - All Todos")

    print(f"\n{'='*50}")
    print("Todo List API Test Completed!")
    print(f"{'='*50}")


if __name__ == "__main__":
    try:
        test_todo_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the FastAPI server is running on http://localhost:8000")
        print("Run: python -m src.fastapi_todo_list.main")
        print("OR: todo-api (if installed as package)")
    except Exception as e:
        print(f"An error occurred: {e}")
