import os
import logging
import re
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class DisplayConfig(AppConfig):
    name = 'display'
    
    def _extract_django_port(self):
        """Extract the Django server port from command line arguments"""
        import sys
        
        # Default Django development server port
        default_port = 8000
        
        # Look for runserver command with port specification
        if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
            for i, arg in enumerate(sys.argv):
                if arg == 'runserver' and i + 1 < len(sys.argv):
                    next_arg = sys.argv[i + 1]
                    
                    # Handle formats like "8001", "127.0.0.1:8001", "localhost:8001"
                    port_match = re.search(r':(\d+)$', next_arg)
                    if port_match:
                        return int(port_match.group(1))
                    elif next_arg.isdigit():
                        return int(next_arg)
        
        return default_port
    
    def ready(self):
        """Called when Django app is ready - handle port conflicts and auto-start FastAPI server"""
        # Only start services when running the Django dev server, not for management commands
        django_command = os.environ.get('_', '')
        if 'runserver' in django_command or 'manage.py runserver' in ' '.join(os.sys.argv if hasattr(os, 'sys') else []):
            # Check if we're running the development server
            import sys
            if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
                try:
                    # Step 1: Handle Django port conflicts
                    django_port = self._extract_django_port()
                    logger.info(f"Django server will use port {django_port}")
                    
                    # Only handle port conflicts for non-default ports or when explicitly requested
                    if django_port != 8000:
                        from .server_manager import handle_django_port_conflicts
                        django_result = handle_django_port_conflicts(django_port)
                        if django_result['success']:
                            logger.info(f"Django port {django_port} is ready: {django_result['message']}")
                        else:
                            logger.warning(f"Django port conflict handling failed: {django_result['message']}")
                    
                    # Step 2: Handle FastAPI server startup
                    from .server_manager import FastAPIServerManager
                    server_manager = FastAPIServerManager()
                    result = server_manager.start_server_if_needed()
                    if result['success']:
                        logger.info("FastAPI server auto-start completed")
                    else:
                        logger.warning(f"FastAPI server auto-start failed: {result['message']}")
                        
                except Exception as e:
                    logger.error(f"Error during server startup management: {str(e)}")
        else:
            logger.debug("Skipping server auto-start for management command")
