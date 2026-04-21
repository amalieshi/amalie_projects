"""Script to inspect actual AutomationIds in the WPF application."""

import subprocess
import time
from pywinauto import Application
from config import APP_EXECUTABLE, APP_WINDOW_TITLE_UIA


def inspect_wpf_controls():
    """Inspect all controls in the WPF app to see their actual AutomationIds."""

    print("=== Inspecting WPF Controls ===")

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
                    descendants = window.descendants()
                    print(f"\nFound {len(descendants)} controls:")

                    all_controls = []

                    for i, control in enumerate(descendants):
                        try:
                            auto_id = control.automation_id()
                            control_type = control.control_type()
                            class_name = control.class_name()
                            window_text = ""

                            try:
                                window_text = control.window_text()
                            except:
                                pass

                            # Show ALL controls, not just ones with AutomationId
                            all_controls.append(
                                {
                                    "index": i,
                                    "automation_id": auto_id if auto_id else "<none>",
                                    "control_type": control_type,
                                    "class_name": class_name,
                                    "window_text": window_text,
                                }
                            )

                        except Exception as e:
                            continue

                    # Show first 20 controls for inspection
                    print(f"\nFirst 20 controls for inspection:")
                    print("-" * 100)

                    for i, ctrl in enumerate(all_controls[:20]):
                        text_preview = (
                            ctrl["window_text"][:30] if ctrl["window_text"] else ""
                        )
                        print(
                            f"  {i:2}. Type: {ctrl['control_type']:15} | Class: {ctrl['class_name']:20} | Text: '{text_preview}' | AutoId: {ctrl['automation_id']}"
                        )

                    # Look for common WPF control types we need
                    print(f"\n=== Looking for Common WPF Controls ===")

                    # Find TextBoxes (likely our input fields)
                    textboxes = [
                        c
                        for c in all_controls
                        if "edit" in c["control_type"].lower()
                        or "text" in c["control_type"].lower()
                    ]
                    print(f"\nTextBox/Edit controls ({len(textboxes)}):")
                    for i, tb in enumerate(textboxes):
                        print(
                            f"  {i+1}. {tb['control_type']} | Class: {tb['class_name']} | Text: '{tb['window_text']}'"
                        )

                    # Find Buttons
                    buttons = [
                        c for c in all_controls if "button" in c["control_type"].lower()
                    ]
                    print(f"\nButton controls ({len(buttons)}):")
                    for i, btn in enumerate(buttons):
                        print(
                            f"  {i+1}. {btn['control_type']} | Class: {btn['class_name']} | Text: '{btn['window_text']}'"
                        )

                    # Find DataGrids/Lists
                    grids = [
                        c
                        for c in all_controls
                        if any(
                            word in c["control_type"].lower()
                            for word in ["grid", "table", "list"]
                        )
                    ]
                    print(f"\nGrid/Table controls ({len(grids)}):")
                    for i, grid in enumerate(grids):
                        print(
                            f"  {i+1}. {grid['control_type']} | Class: {grid['class_name']} | Text: '{grid['window_text']}'"
                        )

                    print("\n" + "=" * 80)

                    # Check specifically for our expected controls
                    print("=== Checking Expected Controls ===")
                    expected_ids = [
                        "product_name_textbox",
                        "product_sku_textbox",
                        "product_price_textbox",
                        "product_quantity_textbox",
                        "add_product_button",
                        "save_product_button",
                        "products_display_grid",
                    ]

                    found_ids = [
                        ctrl["automation_id"]
                        for ctrl in all_controls
                        if ctrl["automation_id"] != "<none>"
                    ]

                    for expected_id in expected_ids:
                        if expected_id in found_ids:
                            print(f"✓ Found: '{expected_id}'")
                        else:
                            print(f"✗ Missing: '{expected_id}'")

                            # Look for similar IDs
                            similar = [
                                fid
                                for fid in found_ids
                                if any(
                                    word in fid.lower()
                                    for word in expected_id.split("_")
                                )
                            ]
                            if similar:
                                print(f"    Similar: {similar}")

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
    inspect_wpf_controls()
