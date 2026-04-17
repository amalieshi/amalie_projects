#!/usr/bin/env python3
"""
Quick version bump script - run from repository root.
Wrapper for python/web-frameworks/fastapi/bump_version.py
"""

import sys
import subprocess
from pathlib import Path


def main():
    # Get the directory where this script is located (repo root)
    script_dir = Path(__file__).parent
    fastapi_dir = script_dir / "python" / "web-frameworks" / "fastapi"
    bump_script = fastapi_dir / "bump_version.py"

    if not bump_script.exists():
        print(f"Error: bump_version.py not found at {bump_script}")
        sys.exit(1)

    # Pass all arguments to the actual bump script
    cmd = [sys.executable, str(bump_script)] + sys.argv[1:]

    # Run from the repository root
    try:
        subprocess.run(cmd, cwd=script_dir, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nCancelled by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
