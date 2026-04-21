"""Test script to identify correct PyWinAuto methods for UIA."""

import subprocess
import time
from pywinauto import Application
from config import APP_EXECUTABLE, APP_WINDOW_TITLE_UIA


def test_uia_methods():
    """Test what methods are available on UIA window objects."""

    print("=== Testing UIA Methods ===")

    # Start app
    process = subprocess.Popen([str(APP_EXECUTABLE)])
    pid = process.pid
    time.sleep(3)

    try:
        # Connect with UIA
        app = Application(backend="uia").connect(process=pid)
        windows = app.windows()

        if windows:
            # Get the main window
            for window in windows:
                title = window.window_text()
                if title == APP_WINDOW_TITLE_UIA:
                    print(f"Found main window: {title}")
                    print(f"Window type: {type(window)}")

                    # List available methods
                    print("\nAvailable methods:")
                    methods = [
                        method for method in dir(window) if not method.startswith("_")
                    ]
                    for method in sorted(methods):
                        print(f"  {method}")

                    # Test specific methods for finding child controls
                    print("\n=== Testing Child Control Methods ===")

                    # Method 1: Try descendants()
                    try:
                        descendants = window.descendants()
                        print(
                            f"✓ descendants() works - found {len(descendants)} descendants"
                        )

                        # Look for controls with AutomationId
                        for i, desc in enumerate(descendants[:10]):  # Check first 10
                            try:
                                auto_id = desc.automation_id()
                                control_type = desc.control_type()
                                if auto_id:
                                    print(
                                        f"  Descendant {i}: AutomationId='{auto_id}', Type='{control_type}'"
                                    )
                            except:
                                pass

                    except Exception as e:
                        print(f"✗ descendants() failed: {e}")

                    # Method 2: Try children()
                    try:
                        children = window.children()
                        print(f"✓ children() works - found {len(children)} children")
                    except Exception as e:
                        print(f"✗ children() failed: {e}")

                    # Method 3: Try find methods
                    try:
                        # Look for textbox with specific AutomationId
                        result = window.child_window(auto_id="product_name_textbox")
                        print(f"✓ child_window(auto_id=...) works: {result}")
                    except Exception as e:
                        print(f"✗ child_window(auto_id=...) failed: {e}")

                    break

    finally:
        # Cleanup
        try:
            process.terminate()
            time.sleep(1)
            if process.poll() is None:
                process.kill()
        except:
            pass


if __name__ == "__main__":
    test_uia_methods()
