// Todo API Orchestrator JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Auto-format JSON in textareas
    const jsonTextareas = document.querySelectorAll('textarea[id*="json"], textarea[id*="payload"]');
    jsonTextareas.forEach(textarea => {
        textarea.addEventListener('blur', function() {
            try {
                if (this.value.trim()) {
                    const parsed = JSON.parse(this.value);
                    this.value = JSON.stringify(parsed, null, 2);
                }
            } catch (e) {
                // Invalid JSON, leave as is
            }
        });
    });

    // Copy to clipboard functionality
    window.copyToClipboard = function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function() {
                showToast('Copied to clipboard!', 'success');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showToast('Copied to clipboard!', 'success');
        }
    };

    // Show toast notification
    window.showToast = function(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    };

    // Form validation helper
    window.validateForm = function(formElement) {
        const requiredFields = formElement.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    };

    // JSON validator for raw requests
    const rawJsonTextarea = document.getElementById('id_json_payload');
    if (rawJsonTextarea) {
        rawJsonTextarea.addEventListener('input', function() {
            const feedback = document.getElementById('json-feedback') || createJsonFeedback();
            
            if (!this.value.trim()) {
                feedback.textContent = '';
                this.classList.remove('is-invalid', 'is-valid');
                return;
            }
            
            try {
                JSON.parse(this.value);
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                feedback.textContent = 'Valid JSON';
                feedback.className = 'valid-feedback';
            } catch (e) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
                feedback.textContent = `Invalid JSON: ${e.message}`;
                feedback.className = 'invalid-feedback';
            }
        });
    }

    function createJsonFeedback() {
        const feedback = document.createElement('div');
        feedback.id = 'json-feedback';
        rawJsonTextarea.parentNode.appendChild(feedback);
        return feedback;
    }

    // Auto-save form data to localStorage (for better UX)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const formId = form.getAttribute('action') || 'default';
        
        // Load saved data
        const savedData = localStorage.getItem(`form_${formId}`);
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const field = form.querySelector(`[name="${key}"]`);
                    if (field && field.type !== 'submit' && field.type !== 'hidden') {
                        field.value = data[key];
                    }
                });
            } catch (e) {
                console.log('Error loading saved form data:', e);
            }
        }

        // Save data on input
        form.addEventListener('input', function(e) {
            if (e.target.type === 'submit' || e.target.type === 'hidden') return;
            
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData) {
                if (key !== 'csrfmiddlewaretoken') {
                    data[key] = value;
                }
            }
            localStorage.setItem(`form_${formId}`, JSON.stringify(data));
        });
    });

    // Enhanced server control with loading states
    window.controlServer = function(action) {
        const button = event.target;
        const originalText = button.innerHTML;
        
        // Show loading state
        button.disabled = true;
        button.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>${action}ing...`;
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch('/server/control/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `action=${action}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast(data.message, 'success');
                // Update server status
                setTimeout(() => {
                    if (window.updateServerStatus) {
                        window.updateServerStatus();
                    }
                    location.reload();
                }, 1000);
            } else {
                showToast(`Error: ${data.message}`, 'danger');
            }
        })
        .catch(error => {
            console.error('Error controlling server:', error);
            showToast('Error controlling server', 'danger');
        })
        .finally(() => {
            // Restore button state
            button.disabled = false;
            button.innerHTML = originalText;
        });
    };
});

// Utility function to format JSON
function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}

// Utility function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}