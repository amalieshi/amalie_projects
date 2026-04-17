#!/usr/bin/env python3
"""
Build script for the FastAPI Todo List package.
This script demonstrates how to build and optionally upload the package.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {command}")

    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        if result.stdout:
            print("Output:")
            print(result.stdout)
        print("✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error (exit code {e.returncode}):")
        print(e.stderr)
        return False


def main():
    """Main build process"""
    # Change to the project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)

    print("FastAPI Todo List Package Builder")
    print(f"Working directory: {project_root}")

    # Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    if os.path.exists("dist"):
        import shutil

        shutil.rmtree("dist")
        print("Removed dist/ directory")

    if os.path.exists("build"):
        import shutil

        shutil.rmtree("build")
        print("Removed build/ directory")

    # Install build dependencies
    if not run_command(
        "pip install build twine wheel", "Installing build dependencies"
    ):
        print("Failed to install build dependencies")
        sys.exit(1)

    # Build the package
    if not run_command("python -m build", "Building the package"):
        print("Failed to build package")
        sys.exit(1)

    # List the built files
    print("\n📦 Built files:")
    if os.path.exists("dist"):
        for file in os.listdir("dist"):
            file_path = os.path.join("dist", file)
            size = os.path.getsize(file_path)
            print(f"  - {file} ({size:,} bytes)")

    # Check the package
    if not run_command("twine check dist/*", "Checking package integrity"):
        print("Package check failed")
        sys.exit(1)

    print("\n🎉 Package built successfully!")
    print("\nNext steps:")
    print(
        "1. Test installation: pip install dist/fastapi_todo_list-1.0.0-py3-none-any.whl"
    )
    print("2. Upload to test PyPI: twine upload --repository testpypi dist/*")
    print("3. Upload to PyPI: twine upload dist/*")
    print(
        "4. Upload to private feed: twine upload --repository-url <your-feed-url> dist/*"
    )


if __name__ == "__main__":
    main()
