"""Simple debug test to see what's happening with window detection."""

import subprocess
import time
from pywinauto import Application
from config import APP_EXECUTABLE, APP_WINDOW_TITLE, APP_WINDOW_TITLE_UIA


def test_debug_connection():
    """Debug the connection issue during pytest."""

    print(f"\n=== Debug Connection Test ===")
    print(f"Starting app: {APP_EXECUTABLE}")

    # Start the application
    process = subprocess.Popen([str(APP_EXECUTABLE)])
    pid = process.pid
    print(f"App PID: {pid}")

    # Wait for startup
    time.sleep(3)

    try:
        # Test UIA backend
        print("\n--- UIA Backend ---")
        try:
            app_uia = Application(backend="uia").connect(process=pid)
            windows = app_uia.windows()
            print(f"UIA windows found: {len(windows)}")

            for i, window in enumerate(windows):
                try:
                    title = window.window_text()
                    print(f"  Window {i}: '{title}'")

                    # Check if this matches our expected titles
                    if title == APP_WINDOW_TITLE_UIA:
                        print(
                            f"  ✓ MATCH: UIA title '{title}' matches expected '{APP_WINDOW_TITLE_UIA}'"
                        )
                        # Try to access window
                        try:
                            window.exists()
                            print("  ✓ Window exists and is accessible")
                        except Exception as e:
                            print(f"  ✗ Window exists but not accessible: {e}")
                    else:
                        print(f"  ✗ No match: '{title}' != '{APP_WINDOW_TITLE_UIA}'")

                except Exception as e:
                    print(f"  Window {i}: Error getting title: {e}")

        except Exception as e:
            print(f"UIA backend failed: {e}")

        # Test Win32 backend
        print("\n--- Win32 Backend ---")
        try:
            app_win32 = Application(backend="win32").connect(process=pid)
            windows = app_win32.windows()
            print(f"Win32 windows found: {len(windows)}")

            for i, window in enumerate(windows):
                try:
                    title = window.window_text()
                    if title.strip():  # Only show non-empty titles
                        print(f"  Window {i}: '{title}'")

                        # Check if this matches our expected titles
                        if title == APP_WINDOW_TITLE or "Inventory" in title:
                            print(f"  ✓ MATCH: Win32 title '{title}' matches pattern")
                            # Try to access window
                            try:
                                window.exists()
                                print("  ✓ Window exists and is accessible")
                            except Exception as e:
                                print(f"  ✗ Window exists but not accessible: {e}")

                except Exception as e:
                    print(f"  Window {i}: Error getting info: {e}")

        except Exception as e:
            print(f"Win32 backend failed: {e}")

    finally:
        # Cleanup
        try:
            process.terminate()
            time.sleep(1)
            if process.poll() is None:
                process.kill()
        except:
            pass

    print("\n=== Debug Complete ===\n")


if __name__ == "__main__":
    test_debug_connection()
