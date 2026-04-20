import os
import sys
import subprocess
import psutil
import requests
import time
import json
from pathlib import Path
from django.conf import settings
from django.utils import timezone
from .models import ServerStatus, APITestHistory


class FastAPIServerManager:
    """Manager class for controlling the FastAPI server"""

    def __init__(self):
        self.server_url = settings.FASTAPI_SERVER_URL
        self.port = 8002  # Use different port to avoid conflict with todo-display
        self.fastapi_path = self._get_fastapi_path()

    def _get_fastapi_path(self):
        """Get the absolute path to the FastAPI project"""
        # Path: todo-orchestrator -> django -> web-frameworks -> fastapi -> todo-api
        current_dir = Path(__file__).parent.parent  # todo-orchestrator folder
        django_dir = current_dir.parent  # django folder
        web_frameworks_dir = django_dir.parent  # web-frameworks folder
        fastapi_dir = (
            web_frameworks_dir / "fastapi" / "todo-api"
        )  # fastapi/todo-api folder
        return fastapi_dir

    def is_server_running(self):
        """Check if the FastAPI server is responding"""
        try:
            response = requests.get(f"{self.server_url}/", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_server_pid(self):
        """Get the PID of the running FastAPI server if it exists"""
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = proc.info["cmdline"]
                if cmdline and any(
                    "uvicorn" in arg or "fastapi_todo_list" in arg for arg in cmdline
                ):
                    if any(str(self.port) in arg for arg in cmdline):
                        return proc.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return None

    def start_server(self):
        """Start the FastAPI server"""
        if self.is_server_running():
            return {"success": False, "message": "Server is already running"}

        try:
            # Determine if we're in production (Render) or development
            is_production = os.environ.get("RENDER", False)

            # Build command based on environment
            if is_production:
                # Production mode - no reload, localhost binding
                cmd = [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "src.fastapi_todo_list.main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(self.port),
                    "--workers",
                    "1",
                ]
            else:
                # Development mode - with reload, localhost binding
                cmd = [
                    sys.executable,
                    "-m",
                    "uvicorn",
                    "src.fastapi_todo_list.main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    str(self.port),
                    "--reload",
                ]

            # Check if FastAPI project directory exists
            if not self.fastapi_path.exists():
                return {
                    "success": False,
                    "message": f"FastAPI project not found at {self.fastapi_path}",
                }

            process = subprocess.Popen(
                cmd,
                cwd=str(self.fastapi_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Wait a moment for server to start
            time.sleep(3)

            # Check if server is responding
            if self.is_server_running():
                self._update_server_status(True, process.pid)
                return {
                    "success": True,
                    "message": f"Server started successfully on port {self.port}",
                    "pid": process.pid,
                }
            else:
                return {
                    "success": False,
                    "message": "Server failed to start or is not responding",
                }

        except Exception as e:
            return {"success": False, "message": f"Error starting server: {str(e)}"}

    def stop_server(self):
        """Stop the FastAPI server"""
        pid = self.get_server_pid()
        if not pid:
            return {"success": False, "message": "No running server found"}

        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=10)  # Wait up to 10 seconds for graceful shutdown

            self._update_server_status(False, None)
            return {
                "success": True,
                "message": f"Server stopped successfully (PID: {pid})",
            }

        except psutil.TimeoutExpired:
            try:
                process.kill()  # Force kill if graceful shutdown fails
                self._update_server_status(False, None)
                return {
                    "success": True,
                    "message": f"Server force-stopped (PID: {pid})",
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Error force-stopping server: {str(e)}",
                }
        except Exception as e:
            return {"success": False, "message": f"Error stopping server: {str(e)}"}

    def _update_server_status(self, is_running, pid):
        """Update server status in database"""
        status, created = ServerStatus.objects.get_or_create(
            defaults={
                "is_running": is_running,
                "pid": pid,
                "port": self.port,
                "start_time": timezone.now() if is_running else None,
            }
        )
        if not created:
            status.is_running = is_running
            status.pid = pid
            if is_running:
                status.start_time = timezone.now()
            status.save()

    def get_server_status(self):
        """Get current server status"""
        is_running = self.is_server_running()
        pid = self.get_server_pid()

        # Update database status to match reality
        self._update_server_status(is_running, pid)

        try:
            status = ServerStatus.objects.get()
        except ServerStatus.DoesNotExist:
            status = ServerStatus.objects.create(
                is_running=is_running, pid=pid, port=self.port
            )

        return {
            "is_running": is_running,
            "pid": pid,
            "port": self.port,
            "start_time": status.start_time,
            "server_url": self.server_url,
        }


class APIClient:
    """Client for making requests to the FastAPI server"""

    def __init__(self):
        self.base_url = settings.FASTAPI_SERVER_URL
        self.timeout = 10

    def _log_request(self, method, endpoint, request_data, response, execution_time):
        """Log API request/response to database"""
        try:
            status_code = response.status_code if response else 0
            success = 200 <= status_code < 300
            response_data = (
                response.json() if response and hasattr(response, "json") else None
            )

            APITestHistory.objects.create(
                method=method.upper(),
                endpoint=endpoint,
                request_data=request_data,
                status_code=status_code,
                response_data=response_data,
                success=success,
                execution_time=execution_time,
            )
        except Exception as e:
            print(f"Error logging request: {e}")

    def make_request(self, method, endpoint, data=None):
        """Make an API request and log the results"""
        url = f"{self.base_url.rstrip('/')}{endpoint}"

        start_time = time.time()
        response = None

        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=self.timeout)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, timeout=self.timeout)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, timeout=self.timeout)
            elif method.upper() == "DELETE":
                response = requests.delete(url, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            execution_time = time.time() - start_time
            self._log_request(method, endpoint, data, response, execution_time)

            return {
                "success": 200 <= response.status_code < 300,
                "status_code": response.status_code,
                "data": (
                    response.json()
                    if response.headers.get("content-type", "").startswith(
                        "application/json"
                    )
                    else response.text
                ),
                "execution_time": execution_time,
            }

        except requests.RequestException as e:
            execution_time = time.time() - start_time
            self._log_request(method, endpoint, data, None, execution_time)
            return {
                "success": False,
                "status_code": 0,
                "error": str(e),
                "execution_time": execution_time,
            }

    def test_connection(self):
        """Test if the API server is accessible"""
        return self.make_request("GET", "/")

    # Convenience methods for specific endpoints
    def get_todos(self, endpoint="todos"):
        """Get todos from various endpoints"""
        return self.make_request("GET", f"/{endpoint}")

    def get_todo(self, todo_id):
        """Get specific todo by ID"""
        return self.make_request("GET", f"/todos/{todo_id}")

    def create_todo(self, title, description=None):
        """Create a new todo"""
        data = {"title": title}
        if description:
            data["description"] = description
        return self.make_request("POST", "/todos", data)

    def update_todo(self, todo_id, title=None, description=None, completed=None):
        """Update an existing todo"""
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if completed is not None:
            # Handle boolean conversion more explicitly
            if isinstance(completed, str):
                data["completed"] = completed.lower() == "true"
            elif isinstance(completed, bool):
                data["completed"] = completed
            else:
                data["completed"] = bool(completed)

            # Debug logging
            print(
                f"DEBUG: Updating todo {todo_id} with completed={data['completed']} (type: {type(data['completed'])})"
            )

        return self.make_request("PUT", f"/todos/{todo_id}", data)

    def delete_todo(self, todo_id):
        """Delete a todo by ID"""
        return self.make_request("DELETE", f"/todos/{todo_id}")
