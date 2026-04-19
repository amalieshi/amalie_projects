from django.db import models
from django.utils import timezone
import json


class APITestHistory(models.Model):
    """Model to store API test request/response history"""
    
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ]
    
    timestamp = models.DateTimeField(default=timezone.now)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    endpoint = models.CharField(max_length=200)
    request_data = models.JSONField(blank=True, null=True)
    status_code = models.IntegerField()
    response_data = models.JSONField(blank=True, null=True)
    success = models.BooleanField()
    execution_time = models.FloatField(help_text="Execution time in seconds")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "API Test History"
        verbose_name_plural = "API Test Histories"

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"

    def get_formatted_request_data(self):
        """Return formatted JSON string of request data"""
        if self.request_data:
            return json.dumps(self.request_data, indent=2)
        return ""

    def get_formatted_response_data(self):
        """Return formatted JSON string of response data"""
        if self.response_data:
            return json.dumps(self.response_data, indent=2)
        return ""


class ServerStatus(models.Model):
    """Model to track FastAPI server status"""
    
    is_running = models.BooleanField(default=False)
    pid = models.IntegerField(null=True, blank=True, help_text="Process ID of running server")
    start_time = models.DateTimeField(null=True, blank=True)
    port = models.IntegerField(default=8000)
    last_checked = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Server Status"
        verbose_name_plural = "Server Status"

    def __str__(self):
        status = "Running" if self.is_running else "Stopped"
        return f"FastAPI Server - {status} (Port: {self.port})"