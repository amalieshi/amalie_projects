#!/usr/bin/env python3
"""Convenience script for running different test suites."""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🚀 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)

    result = subprocess.run(cmd, cwd=Path(__file__).parent)

    if result.returncode == 0:
        print(f"✅ {description} completed successfully")
    else:
        print(f"❌ {description} failed with return code {result.returncode}")

    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="WPF Inventory App Test Runner")
    parser.add_argument(
        "--suite",
        choices=["basic", "performance", "all", "quick"],
        default="basic",
        help="Test suite to run (default: basic)",
    )
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Base pytest command
    base_cmd = ["python", "-m", "pytest"]

    if args.verbose:
        base_cmd.extend(["-v", "-s"])

    if args.parallel:
        base_cmd.extend(["-n", "auto"])

    if args.html:
        base_cmd.extend(["--html=test_report.html", "--self-contained-html"])

    # Determine test files based on suite
    if args.suite == "basic":
        test_files = ["tests/test_basic_functionality.py"]
        description = "Basic Functionality Tests"

    elif args.suite == "performance":
        test_files = ["tests/test_performance.py"]
        description = "Performance Tests"

    elif args.suite == "quick":
        test_files = ["tests/test_basic_functionality.py", "tests/test_performance.py"]
        base_cmd.extend(["-m", "not slow"])  # Exclude slow tests
        description = "Quick Test Suite (excluding slow tests)"

    elif args.suite == "all":
        test_files = ["tests/"]
        description = "Full Test Suite"

    # Build final command
    cmd = base_cmd + test_files

    # Run the tests
    return_code = run_command(cmd, description)

    if args.html and return_code == 0:
        print(f"\n📊 HTML report generated: test_report.html")

    sys.exit(return_code)


if __name__ == "__main__":
    main()
