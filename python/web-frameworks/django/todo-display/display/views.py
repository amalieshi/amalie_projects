from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.conf import settings
from .utils import TodoAPIClient


class TodoListView(View):
    """Main view for displaying todos to users"""
    
    def get(self, request):
        """Display todos with optional filtering"""
        client = TodoAPIClient()
        
        # Get filter parameter
        filter_type = request.GET.get('filter', 'all')
        search_query = request.GET.get('search', '').strip()
        
        # Check server connectivity
        server_online = client.check_server_status()
        
        if not server_online:
            context = {
                'server_online': False,
                'fastapi_url': settings.FASTAPI_SERVER_URL,
                'filter_type': filter_type,
                'search_query': search_query,
            }
            return render(request, 'display/todo_list.html', context)
        
        # Fetch todos based on filter
        if filter_type == 'active':
            result = client.get_active_todos()
        elif filter_type == 'completed':
            result = client.get_completed_todos()
        else:  # 'all'
            result = client.get_all_todos()
        
        # Handle API errors
        if not result['success']:
            messages.error(request, f"Unable to load todos: {result['error']}")
            todos = []
            todos_count = 0
        else:
            todos = result['data']
            
            # Apply search filter if provided
            if search_query:
                todos = [
                    todo for todo in todos 
                    if search_query.lower() in todo.get('title', '').lower() or 
                       search_query.lower() in todo.get('description', '').lower()
                ]
            
            todos_count = len(todos)
        
        # Get counts for filter badges
        all_count = active_count = completed_count = 0
        if server_online:
            all_result = client.get_all_todos()
            active_result = client.get_active_todos()
            completed_result = client.get_completed_todos()
            
            if all_result['success']:
                all_count = all_result['count']
            if active_result['success']:
                active_count = active_result['count']
            if completed_result['success']:
                completed_count = completed_result['count']
        
        context = {
            'todos': todos,
            'todos_count': todos_count,
            'server_online': server_online,
            'fastapi_url': settings.FASTAPI_SERVER_URL,
            'filter_type': filter_type,
            'search_query': search_query,
            'all_count': all_count,
            'active_count': active_count,
            'completed_count': completed_count,
        }
        
        return render(request, 'display/todo_list.html', context)
    
    def post(self, request):
        """Handle todo completion toggle"""
        action = request.POST.get('action')
        todo_id = request.POST.get('todo_id')
        
        if action == 'toggle_complete' and todo_id:
            client = TodoAPIClient()
            result = client.toggle_todo_completion(todo_id)
            
            if result['success']:
                action_text = result['action']
                messages.success(request, f"Todo {action_text} successfully!")
            else:
                messages.error(request, f"Error updating todo: {result['error']}")
        
        # Preserve current filter and search in redirect
        redirect_url = '.'
        params = []
        if request.POST.get('current_filter'):
            params.append(f"filter={request.POST.get('current_filter')}")
        if request.POST.get('current_search'):
            params.append(f"search={request.POST.get('current_search')}")
        
        if params:
            redirect_url += '?' + '&'.join(params)
        
        return redirect(redirect_url)
