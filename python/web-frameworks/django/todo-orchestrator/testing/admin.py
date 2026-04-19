from django.contrib import admin
from .models import APITestHistory, ServerStatus


@admin.register(APITestHistory)
class APITestHistoryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'method', 'endpoint', 'status_code', 'success', 'execution_time')
    list_filter = ('method', 'success', 'timestamp')
    search_fields = ('endpoint',)
    readonly_fields = ('timestamp', 'execution_time')
    ordering = ('-timestamp',)

    fieldsets = (
        ('Request Information', {
            'fields': ('timestamp', 'method', 'endpoint', 'request_data')
        }),
        ('Response Information', {
            'fields': ('status_code', 'success', 'response_data', 'execution_time')
        }),
    )


@admin.register(ServerStatus)
class ServerStatusAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_running', 'pid', 'start_time', 'last_checked')
    readonly_fields = ('last_checked',)
    
    fieldsets = (
        ('Server Information', {
            'fields': ('is_running', 'pid', 'port')
        }),
        ('Timestamps', {
            'fields': ('start_time', 'last_checked')
        }),
    )