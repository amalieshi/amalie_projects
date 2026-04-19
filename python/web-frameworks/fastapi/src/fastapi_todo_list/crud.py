from sqlalchemy.orm import Session
from .database import TodoItem
from .schemas import TodoCreate, TodoUpdate
from datetime import datetime
from typing import List, Optional


def get_todos(db: Session, completed: Optional[bool] = None) -> List[TodoItem]:
    """Get all todos, optionally filtered by completion status"""
    query = db.query(TodoItem)
    if completed is not None:
        query = query.filter(TodoItem.completed == completed)
    result = query.order_by(TodoItem.created_at.desc()).all()
    
    # Debug logging
    if completed is True:
        print(f"DEBUG CRUD: get_todos(completed=True) returned {len(result)} items")
    elif completed is False:
        print(f"DEBUG CRUD: get_todos(completed=False) returned {len(result)} items")
    else:
        print(f"DEBUG CRUD: get_todos(all) returned {len(result)} items")
    
    return result


def get_active_todos(db: Session) -> List[TodoItem]:
    """Get all active (incomplete) todos"""
    result = db.query(TodoItem).filter(TodoItem.completed == False).order_by(TodoItem.created_at.desc()).all()
    print(f"DEBUG CRUD: get_active_todos() returned {len(result)} items")
    return result


def get_completed_todos(db: Session) -> List[TodoItem]:  
    """Get all completed todos"""
    result = db.query(TodoItem).filter(TodoItem.completed == True).order_by(TodoItem.created_at.desc()).all()
    print(f"DEBUG CRUD: get_completed_todos() returned {len(result)} items")
    return result


def get_todo(db: Session, todo_id: int) -> Optional[TodoItem]:
    """Get a specific todo by ID"""
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()


def create_todo(db: Session, todo: TodoCreate) -> TodoItem:
    """Create a new todo item"""
    db_todo = TodoItem(
        title=todo.title,
        description=todo.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(
    db: Session, todo_id: int, todo_update: TodoUpdate
) -> Optional[TodoItem]:
    """Update an existing todo item"""
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not db_todo:
        print(f"DEBUG CRUD: Todo {todo_id} not found for update")
        return None

    update_data = todo_update.dict(exclude_unset=True)
    print(f"DEBUG CRUD: Updating todo {todo_id} with data: {update_data}")

    # If marking as completed, set completed_at timestamp
    if "completed" in update_data:
        if update_data["completed"]:
            update_data["completed_at"] = datetime.utcnow()
            print(f"DEBUG CRUD: Marking todo {todo_id} as completed")
        else:
            update_data["completed_at"] = None
            print(f"DEBUG CRUD: Marking todo {todo_id} as incomplete")

    update_data["updated_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    
    print(f"DEBUG CRUD: Todo {todo_id} updated successfully, completed={db_todo.completed}")
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    """Delete a todo item"""
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if not db_todo:
        return False

    db.delete(db_todo)
    db.commit()
    return True
