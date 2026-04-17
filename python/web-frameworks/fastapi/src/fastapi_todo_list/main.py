from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud
from . import schemas
from .database import get_db

app = FastAPI(
    title="Todo List API",
    description="A simple todo list API with FastAPI",
    version="1.0.0",
)


@app.get("/", summary="Welcome message")
def read_root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to the Todo List API!",
        "endpoints": {
            "GET /todos": "Get all active todos",
            "GET /todos/completed": "Get completed todos",
            "POST /todos": "Create a new todo",
            "PUT /todos/{id}": "Update a todo",
            "DELETE /todos/{id}": "Delete a todo",
        },
    }


@app.get(
    "/todos", response_model=List[schemas.TodoResponse], summary="Get active todos"
)
def get_active_todos(db: Session = Depends(get_db)):
    """
    Get all active (incomplete) todo items.
    Returns todos ordered by creation date (newest first).
    """
    todos = crud.get_todos(db, completed=False)
    return todos


@app.get(
    "/todos/completed",
    response_model=List[schemas.TodoResponse],
    summary="Get completed todos",
)
def get_completed_todos(db: Session = Depends(get_db)):
    """
    Get all completed todo items.
    Returns todos ordered by creation date (newest first).
    """
    todos = crud.get_todos(db, completed=True)
    return todos


@app.get(
    "/todos/all", response_model=List[schemas.TodoResponse], summary="Get all todos"
)
def get_all_todos(db: Session = Depends(get_db)):
    """
    Get all todo items regardless of completion status.
    Returns todos ordered by creation date (newest first).
    """
    todos = crud.get_todos(db)
    return todos


@app.get(
    "/todos/{todo_id}", response_model=schemas.TodoResponse, summary="Get specific todo"
)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo item by ID"""
    todo = crud.get_todo(db, todo_id=todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )
    return todo


@app.post(
    "/todos",
    response_model=schemas.TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new todo",
)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo item.

    - **title**: The title of the todo (required)
    - **description**: Optional description of the todo
    """
    return crud.create_todo(db=db, todo=todo)


@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse, summary="Update todo")
def update_todo(
    todo_id: int, todo_update: schemas.TodoUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing todo item.

    - **title**: Update the title
    - **description**: Update the description
    - **completed**: Mark as completed (true) or incomplete (false)

    When marking as completed, the completion timestamp is automatically set.
    """
    updated_todo = crud.update_todo(db=db, todo_id=todo_id, todo_update=todo_update)
    if updated_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )
    return updated_todo


@app.delete("/todos/{todo_id}", summary="Delete todo")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo item by ID"""
    success = crud.delete_todo(db=db, todo_id=todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )
    return {"message": f"Todo with id {todo_id} has been deleted successfully"}


def main():
    """Entry point for the application"""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
