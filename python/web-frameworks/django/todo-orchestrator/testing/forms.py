from django import forms
from django.core.exceptions import ValidationError
import json


class TodoCreateForm(forms.Form):
    """Form for creating a new todo"""
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter todo title'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter todo description (optional)'
        })
    )


class TodoUpdateForm(forms.Form):
    """Form for updating an existing todo"""
    todo_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter todo ID'
        })
    )
    title = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new title (optional)'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter new description (optional)'
        })
    )
    completed = forms.ChoiceField(
        required=False,
        choices=[('', 'No change'), ('true', 'Completed'), ('false', 'Not completed')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        completed = cleaned_data.get('completed')
        
        if not any([title, description, completed]):
            raise ValidationError("At least one field (title, description, or completed) must be provided for update.")
        
        return cleaned_data


class TodoRetrieveForm(forms.Form):
    """Form for retrieving specific todo by ID"""
    todo_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter todo ID'
        })
    )


class TodoDeleteForm(forms.Form):
    """Form for deleting a todo by ID"""
    todo_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter todo ID to delete'
        })
    )
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="I confirm I want to delete this todo"
    )


class RawAPIRequestForm(forms.Form):
    """Form for making raw API requests with custom JSON payload"""
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ]
    
    method = forms.ChoiceField(
        choices=METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    endpoint = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter endpoint path (e.g., /todos, /todos/1)'
        })
    )
    json_payload = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Enter JSON payload (for POST/PUT requests)'
        })
    )

    def clean_json_payload(self):
        payload = self.cleaned_data.get('json_payload', '')
        if payload.strip():
            try:
                json.loads(payload)
                return payload
            except json.JSONDecodeError as e:
                raise ValidationError(f"Invalid JSON format: {str(e)}")
        return payload

    def clean_endpoint(self):
        endpoint = self.cleaned_data.get('endpoint', '')
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        return endpoint