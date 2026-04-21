"""Test just the basic textbox interaction to verify the approach works."""

import subprocess
import time
from pywinauto import Application
from config import APP_EXECUTABLE, APP_WINDOW_TITLE_UIA


def test_textbox_interaction():
    """Test basic textbox filling to verify approach works."""

    print("=== Testing Basic TextBox Interaction ===")

    # Start app
    process = subprocess.Popen([str(APP_EXECUTABLE)])
    pid = process.pid
    time.sleep(3)

    try:
        # Connect with UIA
        app = Application(backend="uia").connect(process=pid)
        windows = app.windows()

        if windows:
            print(f"Found {len(windows)} windows")

            # Inspect all windows to find the interactive one
            for window_idx, window in enumerate(windows):
                title = window.window_text()
                if title == APP_WINDOW_TITLE_UIA:
                    edit_controls = window.descendants(control_type="Edit")

                    # Look for sample_product content
                    has_sample_product = False
                    try:
                        # Check all descendant controls for "Sample Product" text
                        all_controls = window.descendants()
                        for ctrl in all_controls[
                            :50
                        ]:  # Check first 50 controls to avoid timeout
                            try:
                                text_content = ctrl.window_text()
                                if text_content and (
                                    "sample product" in text_content.lower()
                                    or "sample" in text_content.lower()
                                ):
                                    has_sample_product = True
                                    print(
                                        f"      Found sample product text: '{text_content}'"
                                    )
                                    break
                            except:
                                continue
                    except:
                        pass

                    print(
                        f"Window {window_idx}: '{title}' - Edit controls: {len(edit_controls)}, Has sample_product: {has_sample_product}"
                    )

            # Now find the interactive window (with sample_product content)
            interactive_window = None
            for window in windows:
                title = window.window_text()
                if title == APP_WINDOW_TITLE_UIA:
                    edit_controls = window.descendants(control_type="Edit")

                    # Check for sample_product content
                    has_sample_product = False
                    try:
                        # Check all descendant controls for "Sample Product" text
                        all_controls = window.descendants()
                        for ctrl in all_controls[
                            :50
                        ]:  # Check first 50 controls to avoid timeout
                            try:
                                text_content = ctrl.window_text()
                                if text_content and (
                                    "sample product" in text_content.lower()
                                    or "sample" in text_content.lower()
                                ):
                                    has_sample_product = True
                                    break
                            except:
                                continue
                    except:
                        pass

                    # Prefer the window with sample_product content
                    if has_sample_product:
                        interactive_window = window
                        print(
                            f"\\nSelected interactive window: Has sample_product={has_sample_product}, Edit controls={len(edit_controls)}"
                        )
                        break

            # Fallback to any window with edit controls if no sample product found
            if not interactive_window:
                for window in windows:
                    title = window.window_text()
                    if title == APP_WINDOW_TITLE_UIA:
                        edit_controls = window.descendants(control_type="Edit")
                        if len(edit_controls) >= 4:
                            interactive_window = window
                            print(
                                f"\\nFallback window selected: Edit controls={len(edit_controls)}"
                            )
                            break

            if interactive_window:
                window = interactive_window

                print(f"Connected to interactive window: {window.window_text()}")

                # Find Edit controls
                edit_controls = window.descendants(control_type="Edit")
                print(f"Found {len(edit_controls)} Edit controls")
                print(f"Connected to interactive window: {window.window_text()}")

                # Find Edit controls
                edit_controls = window.descendants(control_type="Edit")
                print(f"Found {len(edit_controls)} Edit controls")

                if len(edit_controls) >= 4:
                    print("\\nTesting TextBox interactions...")

                    # Test first textbox (should be Name field)
                    try:
                        name_field = edit_controls[0]
                        print(f"  TextBox 0: Class='{name_field.class_name()}'")

                        # Try to interact with it
                        name_field.click_input()
                        name_field.type_keys("^a")  # Select all
                        name_field.type_keys("Test Product Name")

                        # Verify text was entered
                        current_text = name_field.window_text()
                        print(f"  ✓ Name field: '{current_text}'")

                    except Exception as e:
                        print(f"  ✗ Name field failed: {e}")

                    # Test second textbox (should be SKU field)
                    try:
                        sku_field = edit_controls[1]
                        print(f"  TextBox 1: Class='{sku_field.class_name()}'")

                        sku_field.click_input()
                        sku_field.type_keys("^a")
                        sku_field.type_keys("TEST-SKU-001")

                        current_text = sku_field.window_text()
                        print(f"  ✓ SKU field: '{current_text}'")

                    except Exception as e:
                        print(f"  ✗ SKU field failed: {e}")

                    # Test third textbox (should be Price field)
                    try:
                        price_field = edit_controls[2]
                        print(f"  TextBox 2: Class='{price_field.class_name()}'")

                        price_field.click_input()
                        price_field.type_keys("^a")
                        price_field.type_keys("29.99")

                        current_text = price_field.window_text()
                        print(f"  ✓ Price field: '{current_text}'")

                    except Exception as e:
                        print(f"  ✗ Price field failed: {e}")

                    # Test fourth textbox (should be Quantity field)
                    try:
                        quantity_field = edit_controls[3]
                        print(f"  TextBox 3: Class='{quantity_field.class_name()}'")

                        quantity_field.click_input()
                        quantity_field.type_keys("^a")
                        quantity_field.type_keys("50")

                        current_text = quantity_field.window_text()
                        print(f"  ✓ Quantity field: '{current_text}'")

                    except Exception as e:
                        print(f"  ✗ Quantity field failed: {e}")

                # Now check what button texts are ACTUALLY available
                print("\\n=== Available Buttons ===")
                button_controls = window.descendants(control_type="Button")
                print(f"Found {len(button_controls)} Button controls:")

                for i, btn in enumerate(button_controls):
                    try:
                        text = btn.window_text()
                        class_name = btn.class_name()
                        auto_id = btn.automation_id()

                        # Skip system buttons (minimize, maximize, close)
                        if text not in ["Minimize", "Maximize", "Close"]:
                            print(
                                f"  Button {i}: Text='{text}', Class='{class_name}', AutoId='{auto_id}'"
                            )
                    except Exception as e:
                        print(f"  Button {i}: Error - {e}")

                print("\\nForm filled! Check the WPF app to see if data appears.")
                input("Press Enter when ready to close...")

            else:
                print("No interactive window found!")

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
    test_textbox_interaction()
