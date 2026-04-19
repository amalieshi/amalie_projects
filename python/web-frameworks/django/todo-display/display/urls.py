"""
URL configuration for display app
"""

from django.urls import path
from . import views

app_name = 'display'

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo_list'),
]