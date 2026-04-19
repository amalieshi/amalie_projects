#!/usr/bin/env python3
"""
Setup script for Todo API Orchestrator Django project.
This script helps initialize the Django project quickly.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(f"Success: {cmd}")
        if result.stdout.strip():
            print(f"  Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed: {cmd}")
        print(f"  Error: {e.stderr.strip()}")
        return False


def main():
    """Main setup routine"""
    print("Todo API Orchestrator Setup")
    print("=" * 40)
    
    # Get the project directory
    project_dir = Path(__file__).parent
    django_dir = project_dir / "src" / "todo_orchestrator"
    
    print(f"Project directory: {project_dir}")
    print(f"Django directory: {django_dir}")
    
    if not django_dir.exists():
        print("Django project directory not found!")
        return False
    
    # Change to Django directory for management commands
    os.chdir(django_dir)
    
    print("\nSetup Steps:")
    print("1. Installing Django orchestrator with FastAPI server dependencies...")
    
    # Install the orchestrator with FastAPI server dependencies
    if not run_command("python -m pip install -e .[fastapi-server]", project_dir):
        print("Failed to install Django orchestrator with dependencies")
        return False
    
    print("\n2. Running Django migrations...")
    
    # Run migrations
    if not run_command("python manage.py makemigrations"):
        print("Warning: Could not create migrations (this might be expected)")
    
    if not run_command("python manage.py migrate"):
        print("Failed to run migrations")
        return False
    
    print("\n3. Collecting static files...")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput"):
        print("Warning: Could not collect static files")
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Navigate to the Django project directory:")
    print(f"   cd {django_dir}")
    print("\n2. Start the Django development server:")
    print("   python manage.py runserver 0.0.0.0:8080")
    print("\n3. Open your browser and go to:")
    print("   http://localhost:8080")
    print("\n4. Use the dashboard to start the FastAPI server and begin testing!")
    
    # Optional: Create superuser
    print("\nOptional: Create a Django superuser for admin access")
    create_superuser = input("Would you like to create a superuser now? (y/N): ").strip().lower()
    if create_superuser in ['y', 'yes']:
        run_command("python manage.py createsuperuser")
        print("\nYou can access the admin interface at: http://localhost:8080/admin/")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)