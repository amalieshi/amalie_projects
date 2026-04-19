from django.urls import path
from .views import (
    DashboardView, ServerControlView, APITestView, TodoManagementView,
    CreateTodoView, UpdateTodoView, RetrieveTodoView, DeleteTodoView,
    RawAPIRequestView, test_history_api, server_status_api,
    clear_test_history, swagger_redirect
)

urlpatterns = [
    # Main pages
    path('', DashboardView.as_view(), name='dashboard'),
    path('test/', APITestView.as_view(), name='api_test'),
    path('todos/', TodoManagementView.as_view(), name='todo_management'),
    
    # Server control
    path('server/control/', ServerControlView.as_view(), name='server_control'),
    path('swagger/', swagger_redirect, name='swagger_redirect'),
    
    # API testing endpoints
    path('api/create/', CreateTodoView.as_view(), name='create_todo'),
    path('api/update/', UpdateTodoView.as_view(), name='update_todo'),
    path('api/retrieve/', RetrieveTodoView.as_view(), name='retrieve_todo'),
    path('api/delete/', DeleteTodoView.as_view(), name='delete_todo'),
    path('api/raw/', RawAPIRequestView.as_view(), name='raw_api_request'),
    
    # JSON API endpoints
    path('api/history/', test_history_api, name='test_history_api'),
    path('api/status/', server_status_api, name='server_status_api'),
    path('api/clear-history/', clear_test_history, name='clear_test_history'),
]