#!/usr/bin/env python3
"""
Documentation build and management scripts for the Sphinx project.
This script replaces the traditional Makefile for cross-platform compatibility.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
SOURCE_DIR = PROJECT_ROOT / "source"
BUILD_DIR = PROJECT_ROOT / "build"
HTML_DIR = BUILD_DIR / "html"

# Import the project discovery module
try:
    from generate_project_docs import main as generate_projects
except ImportError:
    generate_projects = None


def run_command(cmd, check=True, **kwargs):
    """Run a command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=check, **kwargs)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        if check:
            sys.exit(e.returncode)
        return e


def clean():
    """Clean build directories."""
    print("Cleaning build directories...")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    print("Build directories cleaned")


def install_deps(dev=False, all_deps=False):
    """Install project dependencies."""
    print("Installing dependencies...")

    if all_deps:
        cmd = [sys.executable, "-m", "pip", "install", "-e", ".[all]"]
    elif dev:
        cmd = [sys.executable, "-m", "pip", "install", "-e", ".[dev,enhanced,quality]"]
    else:
        cmd = [sys.executable, "-m", "pip", "install", "-e", "."]

    run_command(cmd)
    print("Dependencies installed")


def discover_projects():
    """Run project discovery to generate documentation for all README files."""
    print("Scanning repository for README files...")
    print("Auto-generating project documentation pages...")

    if generate_projects is None:
        print("generate_project_docs.py not found. Auto-discovery disabled.")
        print("Make sure the generate_project_docs.py file exists in this directory.")
        return False

    try:
        generate_projects()
        return True
    except Exception as e:
        print(f"Project discovery failed: {e}")
        import traceback
        print("Full error details:")
        traceback.print_exc()
        return False


def build_projects():
    """Build project documentation from README files."""
    print("\n" + "="*60)
    print("STEP 1: BUILDING PROJECT DOCUMENTATION")
    print("="*60)
    
    if not discover_projects():
        print("Project discovery failed, but continuing with build...")
        return False
    
    print("Project documentation generation complete!")
    return True


def build_html(skip_projects=False):
    """Build HTML documentation."""
    print("\n" + "="*60)
    print("BUILDING COMPLETE DOCUMENTATION SITE")
    print("="*60)
    
    success = True
    
    # Step 1: Build project documentation (unless skipped)
    if not skip_projects:
        if not build_projects():
            print("Project documentation build had issues, continuing...")
    else:
        print("⏭️  Skipping project documentation generation...")
    
    # Step 2: Build main documentation
    print("\n" + "="*60)
    print("STEP 2: BUILDING SPHINX DOCUMENTATION")
    print("="*60)
    
    # Ensure build directory exists
    BUILD_DIR.mkdir(exist_ok=True)

    cmd = [sys.executable, "-m", "sphinx", "-b", "html", str(SOURCE_DIR), str(HTML_DIR)]
    result = run_command(cmd, check=False)

    if result.returncode == 0:
        print("\n" + "="*60)
        print("BUILD COMPLETE!")
        print("="*60)
        print(f"Open {HTML_DIR / 'index.html'} in your browser")
        print(f"Or run 'python docs.py serve' for development server")
    else:
        print("\n" + "="*60)
        print("BUILD FAILED")
        print("="*60)
        success = False

    return success


def serve():
    """Serve documentation with auto-rebuild."""
    print("Starting documentation server with auto-rebuild...")

    cmd = [
        sys.executable,
        "-m",
        "sphinx_autobuild",
        str(SOURCE_DIR),
        str(HTML_DIR),
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
        "--open-browser",
    ]

    try:
        run_command(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped")


def lint():
    """Run documentation linting and quality checks."""
    print("Running documentation quality checks...")

    success = True

    # Check RST files with rstcheck
    print("\nChecking RST syntax...")
    cmd = [sys.executable, "-m", "rstcheck", "--recursive", str(SOURCE_DIR)]
    result = run_command(cmd, check=False)
    if result.returncode != 0:
        success = False

    # Check documentation style with doc8
    print("\nChecking documentation style...")
    cmd = [sys.executable, "-m", "doc8", str(SOURCE_DIR)]
    result = run_command(cmd, check=False)
    if result.returncode != 0:
        success = False

    # Run Sphinx in nitpicky mode to catch warnings
    print("\nRunning Sphinx nitpicky build...")
    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        "-W",
        "--keep-going",
        "-n",  # nitpicky mode
        str(SOURCE_DIR),
        str(BUILD_DIR / "nitpicky"),
    ]
    result = run_command(cmd, check=False)
    if result.returncode != 0:
        success = False

    if success:
        print("All quality checks passed!")
    else:
        print("Some quality checks failed")
        return False

    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Documentation build and management tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s install           # Install basic dependencies
  %(prog)s install --dev     # Install development dependencies
  %(prog)s discover          # Discover and generate project documentation
  %(prog)s build             # Build HTML documentation (includes discovery)
  %(prog)s serve             # Start development server
  %(prog)s lint              # Run quality checks
  %(prog)s clean             # Clean build directories
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install dependencies")
    install_parser.add_argument(
        "--dev", action="store_true", help="Install development dependencies"
    )
    install_parser.add_argument(
        "--all", action="store_true", help="Install all optional dependencies"
    )

    # Discover command
    subparsers.add_parser(
        "discover", help="Discover and generate project documentation"
    )

    # Build command
    build_parser = subparsers.add_parser("build", help="Build HTML documentation")
    build_parser.add_argument(
        "--skip-projects", action="store_true", help="Skip project documentation generation"
    )
    
    # Projects command
    subparsers.add_parser(
        "projects", help="Build only project documentation from README files"
    )

    # Serve command
    subparsers.add_parser("serve", help="Serve documentation with auto-rebuild")

    # Lint command
    subparsers.add_parser("lint", help="Run documentation quality checks")

    # Clean command
    subparsers.add_parser("clean", help="Clean build directories")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Change to project directory
    import os

    os.chdir(PROJECT_ROOT)

    if args.command == "install":
        install_deps(dev=args.dev, all_deps=args.all)
    elif args.command == "discover":
        discover_projects()
    elif args.command == "projects":
        build_projects()
    elif args.command == "build":
        build_html(skip_projects=args.skip_projects)
    elif args.command == "serve":
        serve()
    elif args.command == "lint":
        lint()
    elif args.command == "clean":
        clean()


if __name__ == "__main__":
    main()
