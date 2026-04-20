"""
API utilities for todo-display application
Simple, user-focused API client without debugging overhead
"""

import requests
from django.conf import settings


class TodoAPIClient:
    """Simple API client for fetching todos from FastAPI server"""

    def __init__(self):
        self.base_url = settings.FASTAPI_SERVER_URL
        self.timeout = 10

    def get_all_todos(self):
        """Get all todos"""
        try:
            response = requests.get(f"{self.base_url}/todos/all", timeout=self.timeout)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "count": len(response.json())}
            else:
                return {"success": False, "error": f"API returned status {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def get_active_todos(self):
        """Get active (incomplete) todos"""
        try:
            response = requests.get(f"{self.base_url}/todos", timeout=self.timeout)
            if response.status_code == 200:
                return {"success": True, "data": response.json(), "count": len(response.json())}
            else:
                return {"success": False, "error": f"API returned status {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def get_completed_todos(self):
        """Get completed todos, sorted by completion date (most recent first)"""
        try:
            response = requests.get(f"{self.base_url}/todos/completed", timeout=self.timeout)
            if response.status_code == 200:
                todos = response.json()
                # Sort by completion date (most recent first)
                todos.sort(key=lambda x: x.get("completed_at", ""), reverse=True)
                return {"success": True, "data": todos, "count": len(todos)}
            else:
                return {"success": False, "error": f"API returned status {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def toggle_todo_completion(self, todo_id):
        """Toggle completion status of a todo"""
        try:
            # First get current todo status
            response = requests.get(f"{self.base_url}/todos/{todo_id}", timeout=self.timeout)
            if response.status_code != 200:
                return {"success": False, "error": "Todo not found"}

            current_todo = response.json()
            new_status = not current_todo["completed"]

            # Update the todo
            update_response = requests.put(
                f"{self.base_url}/todos/{todo_id}",
                json={"completed": new_status},
                timeout=self.timeout,
            )

            if update_response.status_code == 200:
                return {
                    "success": True,
                    "data": update_response.json(),
                    "action": "completed" if new_status else "reactivated",
                }
            else:
                return {
                    "success": False,
                    "error": f"Update failed with status {update_response.status_code}",
                }

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def update_todo(self, todo_id, title, description):
        """Update todo title and description"""
        try:
            response = requests.put(
                f"{self.base_url}/todos/{todo_id}",
                json={"title": title, "description": description},
                timeout=self.timeout,
            )

            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False,
                    "error": f"Update failed with status {response.status_code}",
                }

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def get_todo(self, todo_id):
        """Get a specific todo by ID"""
        try:
            response = requests.get(f"{self.base_url}/todos/{todo_id}", timeout=self.timeout)
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False,
                    "error": f"Todo not found (status {response.status_code})",
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def check_server_status(self):
        """Check if FastAPI server is accessible"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def create_todo(self, title, description=""):
        """Create a new todo"""
        try:
            response = requests.post(
                f"{self.base_url}/todos",
                json={"title": title, "description": description, "completed": False},
                timeout=self.timeout,
            )

            # Accept both 200 and 201 as success (201 Created is the standard for POST)
            if response.status_code in [200, 201]:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False,
                    "error": f"Creation failed with status {response.status_code}",
                }

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}

    def delete_todo(self, todo_id):
        """Delete a todo by ID"""
        try:
            response = requests.delete(f"{self.base_url}/todos/{todo_id}", timeout=self.timeout)

            # Accept 200, 204 (No Content), or 202 (Accepted) as success for DELETE
            if response.status_code in [200, 202, 204]:
                return {"success": True, "message": "Todo deleted successfully"}
            else:
                return {
                    "success": False,
                    "error": f"Delete failed with status {response.status_code}",
                }

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
