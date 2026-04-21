"""Debug script to test PyWinAuto connection to WPF application."""

import subprocess
import time
import psutil
from pywinauto import Application, Desktop
from pywinauto.timings import TimeoutError
from config import APP_EXECUTABLE, APP_WINDOW_TITLE


def test_connection_methods():
    """Test different PyWinAuto connection approaches."""

    print(f"Starting WPF app: {APP_EXECUTABLE}")

    # Start the application
    process = subprocess.Popen([str(APP_EXECUTABLE)])
    pid = process.pid

    print(f"App started with PID: {pid}")

    # Wait for app to initialize
    time.sleep(3)
    s
    print("\n=== Testing Connection Methods ===")

    # Method 1: Connect by process ID with UIA backend
    try:
        print("\n1. Trying UIA backend with process ID...")
        app_uia = Application(backend="uia").connect(process=pid)
        windows = app_uia.windows()
        print(f"   ✓ UIA connection successful! Found {len(windows)} windows")
        for i, window in enumerate(windows):
            try:
                title = window.window_text()
                print(f"   Window {i}: '{title}'")
            except:
                print(f"   Window {i}: <no title>")
    except Exception as e:
        print(f"   ✗ UIA connection failed: {e}")

    # Method 2: Connect by process ID with Win32 backend
    try:
        print("\n2. Trying Win32 backend with process ID...")
        app_win32 = Application(backend="win32").connect(process=pid)
        windows = app_win32.windows()
        print(f"   ✓ Win32 connection successful! Found {len(windows)} windows")
        for i, window in enumerate(windows):
            try:
                title = window.window_text()
                print(f"   Window {i}: '{title}'")
            except:
                print(f"   Window {i}: <no title>")
    except Exception as e:
        print(f"   ✗ Win32 connection failed: {e}")

    # Method 3: Connect by window title
    try:
        print(f"\n3. Trying to connect by window title: '{APP_WINDOW_TITLE}'...")
        app_title = Application(backend="uia").connect(title=APP_WINDOW_TITLE)
        windows = app_title.windows()
        print(f"   ✓ Title connection successful! Found {len(windows)} windows")
    except Exception as e:
        print(f"   ✗ Title connection failed: {e}")

    # Method 4: Use Desktop to find all windows
    print("\n4. Scanning all desktop windows...")
    try:
        desktop = Desktop(backend="uia")
        all_windows = desktop.windows()

        print(f"   Found {len(all_windows)} desktop windows:")
        for i, window in enumerate(all_windows):
            try:
                title = window.window_text()
                class_name = window.class_name()
                pid_window = window.process_id()
                if pid_window == pid:
                    print(f"   ★ Window {i}: '{title}' (Class: {class_name}) - OUR APP")
                else:
                    print(f"     Window {i}: '{title}' (Class: {class_name})")
            except:
                print(f"     Window {i}: <error getting info>")
    except Exception as e:
        print(f"   ✗ Desktop scan failed: {e}")

    # Method 5: Direct app connection with longer wait
    try:
        print("\n5. Trying direct app connection with longer wait...")
        app = Application(backend="uia").connect(process=pid)

        # Wait for window to become available
        print("   Waiting for main window...")
        for i in range(15):  # Wait up to 15 seconds
            try:
                windows = app.windows()
                if windows:
                    main_window = windows[0]
                    main_window.wait("visible", timeout=1)
                    print(f"   ✓ Window became visible after {i+1} seconds")
                    print(f"   Window title: '{main_window.window_text()}'")
                    print(f"   Window class: '{main_window.class_name()}'")
                    break
            except:
                print(f"   Waiting... ({i+1}/15)")
                time.sleep(1)
        else:
            print("   ✗ Window never became ready")

    except Exception as e:
        print(f"   ✗ Direct connection failed: {e}")

    print(f"\n=== Process Information ===")
    try:
        proc_info = psutil.Process(pid)
        print(f"Process name: {proc_info.name()}")
        print(f"Process status: {proc_info.status()}")
        print(f"Memory usage: {proc_info.memory_info().rss / 1024 / 1024:.1f} MB")
        print(f"Threads: {proc_info.num_threads()}")
    except Exception as e:
        print(f"Process info error: {e}")

    # Cleanup
    input("\nPress Enter to close the application...")
    try:
        process.terminate()
    except:
        process.kill()


if __name__ == "__main__":
    test_connection_methods()
