#!/usr/bin/env python3
"""
Version bump script for FastAPI Todo List package.
Updates version in pyproject.toml and optionally commits & pushes.

Usage:
    python bump_version.py patch|minor|major [--commit] [--push]
    python bump_version.py 1.2.3 [--commit] [--push]

Run from either location:
    # From repository root:
    python python/web-frameworks/fastapi/bump_version.py patch --push

    # From FastAPI project directory:
    python bump_version.py patch --push

Examples:
    python bump_version.py patch           # 1.0.0 → 1.0.1
    python bump_version.py minor --commit  # 1.0.1 → 1.1.0
    python bump_version.py major --push    # 1.1.0 → 2.0.0
    python bump_version.py 2.1.5 --commit --push
"""

import re
import sys
import argparse
import subprocess
from pathlib import Path


def get_current_version():
    """Get current version from pyproject.toml"""
    # Try different possible paths
    possible_paths = [
        Path("pyproject.toml"),  # Current directory
        Path("python/web-frameworks/fastapi/pyproject.toml"),  # From repo root
        Path("../../../pyproject.toml"),  # From nested directory
        Path("../../pyproject.toml"),  # From parent directory
        Path("../pyproject.toml"),  # From immediate parent
    ]

    pyproject_path = None
    for path in possible_paths:
        if path.exists():
            pyproject_path = path
            break

    if not pyproject_path:
        print("Error: pyproject.toml not found in any expected location.")
        print("Expected locations:")
        for path in possible_paths:
            print(f"  - {path.absolute()}")
        print("\nRun this script from:")
        print("  - Repository root: python/web-frameworks/fastapi/bump_version.py")
        print("  - FastAPI directory: python bump_version.py")
        sys.exit(1)

    content = pyproject_path.read_text()
    match = re.search(r'version = "([^"]+)"', content)

    if not match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)

    return match.group(1), pyproject_path


def parse_version(version_str):
    """Parse version string into major.minor.patch"""
    try:
        parts = version_str.split(".")
        if len(parts) != 3:
            raise ValueError("Version must have 3 parts")
        return [int(p) for p in parts]
    except ValueError as e:
        print(
            f"Error: Invalid version format '{version_str}'. Expected major.minor.patch"
        )
        sys.exit(1)


def bump_version(current_version, bump_type):
    """Bump version based on type"""
    major, minor, patch = parse_version(current_version)

    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        # Assume it's a specific version
        try:
            major, minor, patch = parse_version(bump_type)
        except:
            print(
                f"Error: Invalid bump type '{bump_type}'. Use patch|minor|major or specific version."
            )
            sys.exit(1)

    return f"{major}.{minor}.{patch}"


def update_pyproject_version(new_version, pyproject_path):
    """Update version in pyproject.toml"""
    content = pyproject_path.read_text()

    # Replace version
    new_content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content)

    pyproject_path.write_text(new_content)
    return pyproject_path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Bump version for FastAPI Todo List")
    parser.add_argument(
        "bump_type",
        help="Version bump type: patch|minor|major or specific version (e.g., 1.2.3)",
    )
    parser.add_argument(
        "--commit", action="store_true", help="Commit the version change"
    )
    parser.add_argument(
        "--push", action="store_true", help="Push after committing (implies --commit)"
    )

    args = parser.parse_args()

    if args.push:
        args.commit = True

    # Get current version
    current_version, pyproject_path = get_current_version()
    print(f"Current version: {current_version}")
    print(f"Found pyproject.toml at: {pyproject_path}")

    # Calculate new version
    new_version = bump_version(current_version, args.bump_type)
    print(f"New version: {new_version}")

    # Confirm change
    response = input(f"Update version from {current_version} to {new_version}? (y/N): ")
    if response.lower() != "y":
        print("Cancelled.")
        return

    # Update version
    updated_file = update_pyproject_version(new_version, pyproject_path)
    print(f"Updated {updated_file}")

    # Git operations
    if args.commit:
        commit_message = f"Bump version to {new_version}"

        # Add the changed file
        if not run_command(f"git add {updated_file}", "Adding updated pyproject.toml"):
            return

        # Commit
        if not run_command(
            f'git commit -m "{commit_message}"', "Committing version change"
        ):
            return

        print(f"Committed: {commit_message}")

        # Push if requested
        if args.push:
            if not run_command("git push", "Pushing to remote"):
                return
            print("Pushed to remote")
            print(
                f"GitHub Actions will automatically tag and publish v{new_version}"
            )

    print(
        f"""
Version bumped successfully!

Next steps:
{'Changes committed and pushed' if args.push else '1. git add python/web-frameworks/fastapi/pyproject.toml'}
{'GitHub Actions will handle the rest' if args.push else '2. git commit -m "Bump version to ' + new_version + '"'}
{'   ' if args.push else '3. git push'}
{'   ' if args.push else '4. GitHub Actions will automatically tag and publish v' + new_version}

Monitor progress: https://github.com/amalieshi/amalie_projects/actions
PyPI release: https://pypi.org/project/todolist_fastapi/{new_version}/
GitHub release: https://github.com/amalieshi/amalie_projects/releases/tag/v{new_version}
"""
    )


if __name__ == "__main__":
    main()
