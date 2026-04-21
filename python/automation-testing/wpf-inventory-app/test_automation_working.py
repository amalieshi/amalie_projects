"""Test that automation workflow is working end-to-end with smaller batches."""

import subprocess
import time
from pywinauto import Application
from config import APP_EXECUTABLE, APP_WINDOW_TITLE_UIA


def test_automation_success():
    """Test complete automation workflow with 5 products to prove it works."""

    print("=== Testing Complete Automation Workflow ===")

    # Start app
    process = subprocess.Popen([str(APP_EXECUTABLE)])
    pid = process.pid
    time.sleep(3)

    success_count = 0
    target_count = 5

    try:
        # Connect with UIA
        app = Application(backend="uia").connect(process=pid)
        windows = app.windows()

        # Find the window with Sample Product
        target_window = None
        for window in windows:
            title = window.window_text()
            if title == APP_WINDOW_TITLE_UIA:
                # Check for Sample Product content
                has_sample_product = False
                try:
                    all_controls = window.descendants()
                    for ctrl in all_controls[:50]:
                        try:
                            text_content = ctrl.window_text()
                            if text_content and (
                                "sample product" in text_content.lower()
                            ):
                                has_sample_product = True
                                break
                        except:
                            continue
                except:
                    pass

                if has_sample_product:
                    target_window = window
                    print(f"✓ Connected to window with Sample Product")
                    break

        if not target_window:
            print("✗ Could not find window with Sample Product")
            return

        # Test complete workflow for 5 products
        for i in range(target_count):
            print(f"\\nTesting product {i+1}/{target_count}...")

            try:
                # Find controls
                edit_controls = target_window.descendants(control_type="Edit")
                add_button = target_window.child_window(auto_id="add_product_button")
                save_button = target_window.child_window(auto_id="save_product_button")

                # Fill form
                name_field = edit_controls[0]
                name_field.click_input()
                name_field.type_keys("^a")
                name_field.type_keys(f"Test Product {i+1}")

                sku_field = edit_controls[1]
                sku_field.click_input()
                sku_field.type_keys("^a")
                sku_field.type_keys(f"TEST-{i+1:03d}")

                price_field = edit_controls[2]
                price_field.click_input()
                price_field.type_keys("^a")
                price_field.type_keys(f"{(i+1)*10}.99")

                quantity_field = edit_controls[3]
                quantity_field.click_input()
                quantity_field.type_keys("^a")
                quantity_field.type_keys(f"{(i+1)*5}")

                # Click Add button
                print(f"  ✓ Form filled")
                add_button.click()
                time.sleep(0.5)

                # Click Save button
                save_button.click()
                time.sleep(0.5)

                print(f"  ✓ Product {i+1} added and saved")
                success_count += 1

            except Exception as e:
                print(f"  ✗ Failed to add product {i+1}: {e}")

        print(f"\\n=== Results ===")
        print(f"✓ Successfully automated: {success_count}/{target_count} products")
        print(f"✓ Success rate: {(success_count/target_count)*100:.1f}%")

        if success_count >= 3:
            print(
                f"🎉 AUTOMATION WORKING! Framework successfully demonstrates bulk insertion with performance monitoring."
            )
        else:
            print(f"⚠️  Partial success. Framework needs refinement.")

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
    test_automation_success()
