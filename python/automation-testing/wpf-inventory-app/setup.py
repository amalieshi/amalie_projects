#!/usr/bin/env python3
"""Setup script for WPF Inventory Management App automation testing framework."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command with error handling."""
    print(f"\n🚀 {description}")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    else:
        print(
            f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )

    # Check if WPF app is built
    from config import APP_EXECUTABLE

    if not APP_EXECUTABLE.exists():
        print(f"❌ WPF Application not found at: {APP_EXECUTABLE}")
        print("Please build the WPF application first:")
        print("  cd C:\\projects\\github\\amalie_projects\\csharp\\desktop-apps\\wpf")
        print("  dotnet build")
        return False
    else:
        print(f"✅ WPF Application found: {APP_EXECUTABLE}")

    return True


def install_dependencies():
    """Install Python dependencies."""
    return run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Installing Python dependencies",
    )


def generate_test_data():
    """Generate initial test data."""
    return run_command([sys.executable, "data_generator.py"], "Generating test data")


def run_verification_test():
    """Run a quick verification test."""
    return run_command(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_basic_functionality.py::TestBasicFunctionality::test_application_startup",
            "-v",
        ],
        "Running verification test",
        check=False,  # Don't fail setup if test fails
    )


def main():
    """Main setup function."""
    print("🛠️  WPF Inventory Management App - Test Framework Setup")
    print("=" * 60)

    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Setup failed due to missing prerequisites")
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)

    # Generate test data
    if not generate_test_data():
        print("\n❌ Setup failed during test data generation")
        sys.exit(1)

    # Run verification test
    print("\n🧪 Running verification test...")
    verification_passed = run_verification_test()

    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("\n🚀 Quick start commands:")
    print("  # Run basic tests:")
    print("  python run_tests.py --suite basic --verbose")
    print("\n  # Run performance tests:")
    print("  python run_tests.py --suite performance --verbose")
    print("\n  # Run all tests with HTML report:")
    print("  python run_tests.py --suite all --html --verbose")

    if not verification_passed:
        print("\n⚠️  Verification test failed, but setup is complete.")
        print("    This might be expected if the WPF app isn't running properly.")
        print("    Try running tests manually to diagnose issues.")


if __name__ == "__main__":
    main()
