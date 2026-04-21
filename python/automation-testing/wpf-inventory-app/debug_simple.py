"""Simple script to debug WPF control inspection."""

import subprocess
import time
from pywinauto import Application
from config import APP_EXECUTABLE, APP_WINDOW_TITLE_UIA


def simple_control_debug():
    """Simple debug to see what's in the WPF window."""

    print("=== Simple WPF Control Debug ===")

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

                    # Get all descendant controls
                    try:
                        descendants = window.descendants()
                        print(f"Total descendants: {len(descendants)}")

                        print("\nFirst 10 controls (basic info):")
                        for i, control in enumerate(descendants[:10]):
                            try:
                                print(f"Control {i}:")
                                print(f"  Type: {type(control)}")

                                try:
                                    ctrl_type = control.control_type()
                                    print(f"  ControlType: {ctrl_type}")
                                except Exception as e:
                                    print(f"  ControlType: Error - {e}")

                                try:
                                    class_name = control.class_name()
                                    print(f"  ClassName: {class_name}")
                                except Exception as e:
                                    print(f"  ClassName: Error - {e}")

                                try:
                                    text = control.window_text()
                                    print(f"  Text: '{text}'")
                                except Exception as e:
                                    print(f"  Text: Error - {e}")

                                try:
                                    auto_id = control.automation_id()
                                    print(f"  AutomationId: '{auto_id}'")
                                except Exception as e:
                                    print(f"  AutomationId: Error - {e}")

                                print()

                            except Exception as e:
                                print(f"Control {i}: Error accessing - {e}")

                        # Try to find controls by different methods
                        print("\n=== Alternative Search Methods ===")

                        # Method 1: Find by control type
                        try:
                            edit_controls = window.descendants(control_type="Edit")
                            print(f"Edit controls found: {len(edit_controls)}")
                            for i, edit in enumerate(edit_controls[:3]):
                                try:
                                    print(
                                        f"  Edit {i}: Text='{edit.window_text()}', Class='{edit.class_name()}'"
                                    )
                                except:
                                    print(f"  Edit {i}: <error getting info>")
                        except Exception as e:
                            print(f"Edit search failed: {e}")

                        # Method 2: Find by class name
                        try:
                            textbox_controls = window.descendants(
                                class_name_re=".*TextBox.*"
                            )
                            print(f"TextBox controls found: {len(textbox_controls)}")
                        except Exception as e:
                            print(f"TextBox search failed: {e}")

                        # Method 3: Find buttons
                        try:
                            button_controls = window.descendants(control_type="Button")
                            print(f"Button controls found: {len(button_controls)}")
                            for i, btn in enumerate(button_controls[:3]):
                                try:
                                    print(
                                        f"  Button {i}: Text='{btn.window_text()}', Class='{btn.class_name()}'"
                                    )
                                except:
                                    print(f"  Button {i}: <error getting info>")
                        except Exception as e:
                            print(f"Button search failed: {e}")

                    except Exception as e:
                        print(f"Error getting descendants: {e}")

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
    simple_control_debug()
