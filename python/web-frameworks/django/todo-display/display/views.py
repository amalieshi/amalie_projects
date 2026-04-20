from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.conf import settings
import time
from .utils import TodoAPIClient


class TodoListView(View):
    """Main view for displaying todos to users"""

    def get(self, request):
        """Display todos with optional filtering"""
        client = TodoAPIClient()

        # Get parameters
        filter_type = request.GET.get("filter", "all")
        search_query = request.GET.get("search", "").strip()
        view_type = request.GET.get("view", "cards")  # 'cards' or 'list'

        # Check server connectivity
        server_online = client.check_server_status()

        if not server_online:
            context = {
                "server_online": False,
                "fastapi_url": settings.FASTAPI_SERVER_URL,
                "filter_type": filter_type,
                "search_query": search_query,
                "view_type": view_type,
            }
            return render(request, "display/todo_list.html", context)

        # Fetch todos based on filter
        if filter_type == "active":
            result = client.get_active_todos()
        elif filter_type == "completed":
            result = client.get_completed_todos()
        else:  # 'all'
            result = client.get_all_todos()

        # Handle API errors
        if not result["success"]:
            messages.error(request, f"Unable to load todos: {result['error']}")
            todos = []
            todos_count = 0
        else:
            todos = result["data"]

            # Apply search filter if provided
            if search_query:
                todos = [
                    todo
                    for todo in todos
                    if search_query.lower() in todo.get("title", "").lower()
                    or search_query.lower() in todo.get("description", "").lower()
                ]

            todos_count = len(todos)

        # Get counts for filter badges
        all_count = active_count = completed_count = 0
        if server_online:
            all_result = client.get_all_todos()
            active_result = client.get_active_todos()
            completed_result = client.get_completed_todos()

            if all_result["success"]:
                all_count = all_result["count"]
            if active_result["success"]:
                active_count = active_result["count"]
            if completed_result["success"]:
                completed_count = completed_result["count"]

        context = {
            "todos": todos,
            "todos_count": todos_count,
            "server_online": server_online,
            "fastapi_url": settings.FASTAPI_SERVER_URL,
            "filter_type": filter_type,
            "search_query": search_query,
            "view_type": view_type,
            "all_count": all_count,
            "active_count": active_count,
            "completed_count": completed_count,
        }

        return render(request, "display/todo_list.html", context)

    def post(self, request):
        """Handle todo operations: create, toggle completion, edit, and delete"""
        action = request.POST.get("action")
        todo_id = request.POST.get("todo_id")

        if action == "create_todo":
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()

            if not title:
                messages.error(request, "Title is required")
            else:
                client = TodoAPIClient()
                result = client.create_todo(title, description)

                if result["success"]:
                    messages.success(request, "Todo created successfully!")
                else:
                    messages.error(request, f"Error creating todo: {result['error']}")

        elif action == "toggle_complete" and todo_id:
            client = TodoAPIClient()
            result = client.toggle_todo_completion(todo_id)

            if result["success"]:
                action_text = result["action"]
                messages.success(request, f"Todo {action_text} successfully!")
            else:
                messages.error(request, f"Error updating todo: {result['error']}")

        elif action == "update_todo" and todo_id:
            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()

            if not title:
                messages.error(request, "Title is required")
            else:
                client = TodoAPIClient()
                result = client.update_todo(todo_id, title, description)

                if result["success"]:
                    messages.success(request, "Todo updated successfully!")
                else:
                    messages.error(request, f"Error updating todo: {result['error']}")

        elif action == "delete_todo" and todo_id:
            client = TodoAPIClient()
            result = client.delete_todo(todo_id)

            if result["success"]:
                messages.success(request, "Todo deleted successfully!")
            else:
                messages.error(request, f"Error deleting todo: {result['error']}")

        # Preserve current parameters in redirect
        redirect_url = "."
        params = []
        if request.POST.get("current_filter"):
            params.append(f"filter={request.POST.get('current_filter')}")
        if request.POST.get("current_search"):
            params.append(f"search={request.POST.get('current_search')}")
        if request.POST.get("current_view"):
            params.append(f"view={request.POST.get('current_view')}")

        if params:
            redirect_url += "?" + "&".join(params)

        return redirect(redirect_url)


class HealthCheckView(View):
    """Health check endpoint for deployment monitoring"""

    def get(self, request):
        """Return health status of Django and FastAPI"""
        from django.http import JsonResponse
        import os

        # Basic Django health
        health_status = {
            "django": "healthy",
            "timestamp": time.time(),
            "environment": "production" if os.environ.get("RENDER") else "development",
        }

        # Check FastAPI connectivity
        client = TodoAPIClient()
        fastapi_healthy = client.check_server_status()

        health_status["fastapi"] = "healthy" if fastapi_healthy else "unhealthy"
        health_status["fastapi_url"] = settings.FASTAPI_SERVER_URL

        # Overall health
        overall_healthy = fastapi_healthy
        health_status["status"] = "healthy" if overall_healthy else "degraded"

        status_code = 200 if overall_healthy else 503
        return JsonResponse(health_status, status=status_code)

        return redirect(redirect_url)
