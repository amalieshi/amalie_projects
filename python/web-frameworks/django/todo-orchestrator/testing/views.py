import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.conf import settings

from .forms import (
    TodoCreateForm, TodoUpdateForm, TodoRetrieveForm, 
    TodoDeleteForm, RawAPIRequestForm
)
from .models import APITestHistory, ServerStatus
from .utils import FastAPIServerManager, APIClient


class TodoManagementView(View):
    """Todo list management view"""
    
    def get(self, request):
        client = APIClient()
        
        # Get all todos, active todos, and completed todos
        all_todos_result = client.get_todos('todos/all')
        active_todos_result = client.get_todos('todos')
        completed_todos_result = client.get_todos('todos/completed')
        
        # Debug logging
        print(f"DEBUG GET: Active todos count: {len(active_todos_result.get('data', [])) if active_todos_result.get('success') else 'FAILED'}")
        print(f"DEBUG GET: Completed todos count: {len(completed_todos_result.get('data', [])) if completed_todos_result.get('success') else 'FAILED'}")
        
        # Check server status
        server_manager = FastAPIServerManager()
        server_status = server_manager.get_server_status()
        
        # Get recent test history for logs tab
        recent_tests = APITestHistory.objects.all().order_by('-timestamp')[:20]
        
        context = {
            'server_status': server_status,
            'fastapi_url': settings.FASTAPI_SERVER_URL,
            'all_todos': all_todos_result.get('data', []) if all_todos_result.get('success') else [],
            'active_todos': active_todos_result.get('data', []) if active_todos_result.get('success') else [],
            'completed_todos': completed_todos_result.get('data', []) if completed_todos_result.get('success') else [],
            'all_todos_success': all_todos_result.get('success', False),
            'active_todos_success': active_todos_result.get('success', False),
            'completed_todos_success': completed_todos_result.get('success', False),
            'recent_tests': recent_tests,
        }
        return render(request, 'testing/todo_management.html', context)
    
    def post(self, request):
        """Handle todo operations like delete and toggle completion"""
        action = request.POST.get('action')
        todo_id = request.POST.get('todo_id')
        
        if not todo_id:
            messages.error(request, "No todo ID provided")
            return redirect('todo_management')
        
        client = APIClient()
        
        if action == 'delete':
            result = client.delete_todo(todo_id)
            if result['success']:
                messages.success(request, f"Todo deleted successfully! Status: {result['status_code']}")
            else:
                messages.error(request, f"Error deleting todo: {result.get('error', 'Unknown error')}")
                
        elif action == 'toggle_complete':
            # First get the current todo to see its completion status
            current_todo = client.get_todo(todo_id)
            if current_todo['success']:
                todo = current_todo['data']
                new_status = not todo['completed']
                
                # Debug logging
                print(f"DEBUG: Todo {todo_id} current status: {todo['completed']}, new status: {new_status}")
                
                result = client.update_todo(todo_id, completed=new_status)
                
                if result['success']:
                    status_text = "completed" if new_status else "marked as incomplete"
                    messages.success(request, f"Todo '{todo['title']}' {status_text} successfully! Status: {result['status_code']}")
                    
                    # Add small delay to ensure database transaction is committed
                    import time
                    time.sleep(0.1)
                else:
                    messages.error(request, f"Error updating todo '{todo['title']}': {result.get('error', 'Unknown error')}")
                    print(f"DEBUG: Update failed - {result}")
            else:
                messages.error(request, f"Error getting todo details for ID {todo_id}: {current_todo.get('error', 'Unknown error')}")
                print(f"DEBUG: Get todo failed - {current_todo}")
                
        elif action == 'edit':
            # Get the form data
            title = request.POST.get('title')
            description = request.POST.get('description')
            completed = request.POST.get('completed') == 'on'
            
            if not title:
                messages.error(request, "Title is required")
                return redirect('todo_management')
            
            # Update the todo
            result = client.update_todo(todo_id, title=title, description=description, completed=completed)
            
            if result['success']:
                messages.success(request, f"Todo '{title}' updated successfully! Status: {result['status_code']}")
            else:
                messages.error(request, f"Error updating todo: {result.get('error', 'Unknown error')}")
                print(f"DEBUG: Edit failed - {result}")
        
        return redirect('todo_management')


class DashboardView(View):
    """Main dashboard view"""
    
    def get(self, request):
        server_manager = FastAPIServerManager()
        server_status = server_manager.get_server_status()
        
        # Get recent test history
        recent_tests = APITestHistory.objects.all()[:10]
        
        context = {
            'server_status': server_status,
            'recent_tests': recent_tests,
            'fastapi_url': settings.FASTAPI_SERVER_URL,
            'swagger_url': f"{settings.FASTAPI_SERVER_URL}/docs",
        }
        return render(request, 'testing/dashboard.html', context)


class ServerControlView(View):
    """Handle server start/stop operations"""
    
    def post(self, request):
        action = request.POST.get('action')
        server_manager = FastAPIServerManager()
        
        if action == 'start':
            result = server_manager.start_server()
        elif action == 'stop':
            result = server_manager.stop_server()
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action'})
            
        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result['message'])
            
        return JsonResponse(result)


class APITestView(View):
    """Main API testing interface"""
    
    def get(self, request):
        # Initialize all forms
        forms = {
            'create_form': TodoCreateForm(),
            'update_form': TodoUpdateForm(),
            'retrieve_form': TodoRetrieveForm(),
            'delete_form': TodoDeleteForm(),
            'raw_form': RawAPIRequestForm(),
        }
        
        # Get recent test history
        recent_tests = APITestHistory.objects.all()[:20]
        
        context = {
            **forms,
            'recent_tests': recent_tests,
            'fastapi_url': settings.FASTAPI_SERVER_URL,
        }
        
        return render(request, 'testing/api_test.html', context)


class CreateTodoView(View):
    """Handle todo creation"""
    
    def post(self, request):
        form = TodoCreateForm(request.POST)
        if form.is_valid():
            client = APIClient()
            result = client.create_todo(
                title=form.cleaned_data['title'],
                description=form.cleaned_data.get('description')
            )
            
            if result['success']:
                messages.success(request, f"Todo created successfully! Status: {result['status_code']}")
            else:
                messages.error(request, f"Error creating todo: {result.get('error', 'Unknown error')}")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
                
        return redirect('api_test')


class UpdateTodoView(View):
    """Handle todo updates"""
    
    def post(self, request):
        form = TodoUpdateForm(request.POST)
        if form.is_valid():
            client = APIClient()
            result = client.update_todo(
                todo_id=form.cleaned_data['todo_id'],
                title=form.cleaned_data.get('title') or None,
                description=form.cleaned_data.get('description') or None,
                completed=form.cleaned_data.get('completed') or None
            )
            
            if result['success']:
                messages.success(request, f"Todo updated successfully! Status: {result['status_code']}")
            else:
                messages.error(request, f"Error updating todo: {result.get('error', 'Unknown error')}")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
                
        return redirect('api_test')


class RetrieveTodoView(View):
    """Handle todo retrieval"""
    
    def post(self, request):
        action = request.POST.get('action', 'specific')
        client = APIClient()
        
        if action == 'specific':
            form = TodoRetrieveForm(request.POST)
            if form.is_valid():
                result = client.get_todo(form.cleaned_data['todo_id'])
            else:
                for field, errors in form.errors.items():
                    messages.error(request, f"{field}: {', '.join(errors)}")
                return redirect('api_test')
        elif action == 'all':
            result = client.get_todos('todos')
        elif action == 'completed':
            result = client.get_todos('todos/completed')
        elif action == 'active':
            result = client.get_todos('todos')
        elif action == 'all_todos':
            result = client.get_todos('todos/all')
        else:
            messages.error(request, "Invalid retrieval action")
            return redirect('api_test')
            
        if result['success']:
            messages.success(request, f"Data retrieved successfully! Status: {result['status_code']}")
        else:
            messages.error(request, f"Error retrieving data: {result.get('error', 'Unknown error')}")
            
        return redirect('api_test')


class DeleteTodoView(View):
    """Handle todo deletion"""
    
    def post(self, request):
        form = TodoDeleteForm(request.POST)
        if form.is_valid():
            client = APIClient()
            result = client.delete_todo(form.cleaned_data['todo_id'])
            
            if result['success']:
                messages.success(request, f"Todo deleted successfully! Status: {result['status_code']}")
            else:
                messages.error(request, f"Error deleting todo: {result.get('error', 'Unknown error')}")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
                
        return redirect('api_test')


class RawAPIRequestView(View):
    """Handle raw API requests"""
    
    def post(self, request):
        form = RawAPIRequestForm(request.POST)
        if form.is_valid():
            client = APIClient()
            
            # Parse JSON payload if provided
            json_data = None
            if form.cleaned_data.get('json_payload'):
                try:
                    json_data = json.loads(form.cleaned_data['json_payload'])
                except json.JSONDecodeError as e:
                    messages.error(request, f"Invalid JSON payload: {str(e)}")
                    return redirect('api_test')
            
            result = client.make_request(
                method=form.cleaned_data['method'],
                endpoint=form.cleaned_data['endpoint'],
                data=json_data
            )
            
            if result['success']:
                messages.success(request, f"Request completed! Status: {result['status_code']}")
            else:
                messages.error(request, f"Request failed: {result.get('error', 'Unknown error')}")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
                
        return redirect('api_test')


@require_http_methods(["GET"])
def test_history_api(request):
    """API endpoint to get test history as JSON"""
    limit = int(request.GET.get('limit', 20))
    tests = APITestHistory.objects.all()[:limit]
    
    data = []
    for test in tests:
        data.append({
            'id': test.id,
            'timestamp': test.timestamp.isoformat(),
            'method': test.method,
            'endpoint': test.endpoint,
            'status_code': test.status_code,
            'success': test.success,
            'execution_time': test.execution_time,
            'request_data': test.request_data,
            'response_data': test.response_data,
        })
    
    return JsonResponse({'tests': data})


@require_http_methods(["GET"])
def server_status_api(request):
    """API endpoint to get current server status"""
    server_manager = FastAPIServerManager()
    status = server_manager.get_server_status()
    return JsonResponse(status)


@require_http_methods(["POST"])
@csrf_exempt
def clear_test_history(request):
    """Clear all test history"""
    try:
        count = APITestHistory.objects.count()
        APITestHistory.objects.all().delete()
        messages.success(request, f"Cleared {count} test history entries")
        return JsonResponse({'success': True, 'message': f'Cleared {count} entries'})
    except Exception as e:
        messages.error(request, f"Error clearing history: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)})


def swagger_redirect(request):
    """Redirect to FastAPI Swagger UI"""
    swagger_url = f"{settings.FASTAPI_SERVER_URL}/docs"
    return HttpResponseRedirect(swagger_url)