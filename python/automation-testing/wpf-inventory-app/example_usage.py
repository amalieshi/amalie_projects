#!/usr/bin/env python3
"""Example usage of the WPF Inventory Management App automation framework."""

import time
from pathlib import Path
from pywinauto import Application
from data_generator import ProductDataGenerator
from config import APP_EXECUTABLE, CONTROL_IDS, TEST_SETTINGS


def manual_automation_example():
    """Example of manual automation without pytest framework."""
    print("🚀 Manual Automation Example")
    print("=" * 40)

    # Check if app exists
    if not APP_EXECUTABLE.exists():
        print(f"❌ Application not found: {APP_EXECUTABLE}")
        print("Please build the WPF application first.")
        return

    # Generate test data
    generator = ProductDataGenerator()
    test_products = generator.generate_product_batch(3)

    print(f"Generated {len(test_products)} test products:")
    for i, product in enumerate(test_products, 1):
        print(f"  {i}. {product['name']} (SKU: {product['sku']}, ${product['price']})")

    # Start the application
    print("\n📱 Starting WPF application...")
    app = Application().start(str(APP_EXECUTABLE))

    try:
        # Connect to the main window
        main_window = app.top_window()
        main_window.wait("ready", timeout=TEST_SETTINGS["app_startup_timeout"])

        print("✅ Application started successfully")
        print(f"Window title: {main_window.window_text()}")

        # Add products one by one
        for i, product in enumerate(test_products, 1):
            print(f"\n📝 Adding product {i}/{len(test_products)}: {product['name']}")

            try:
                # Fill product name
                name_field = main_window.child_window(
                    auto_id=CONTROL_IDS["product_name_textbox"]
                )
                name_field.click_input()
                name_field.type_keys("^a")  # Select all
                name_field.type_keys(product["name"])

                # Fill SKU
                sku_field = main_window.child_window(
                    auto_id=CONTROL_IDS["product_sku_textbox"]
                )
                sku_field.click_input()
                sku_field.type_keys("^a")
                sku_field.type_keys(product["sku"])

                # Fill price
                price_field = main_window.child_window(
                    auto_id=CONTROL_IDS["product_price_textbox"]
                )
                price_field.click_input()
                price_field.type_keys("^a")
                price_field.type_keys(str(product["price"]))

                # Fill quantity
                quantity_field = main_window.child_window(
                    auto_id=CONTROL_IDS["product_quantity_textbox"]
                )
                quantity_field.click_input()
                quantity_field.type_keys("^a")
                quantity_field.type_keys(str(product["quantity"]))

                # Click Add button
                add_button = main_window.child_window(
                    auto_id=CONTROL_IDS["add_product_button"]
                )
                add_button.click()

                print(f"  ✅ Product '{product['name']}' added successfully")

                # Small delay between products
                time.sleep(0.5)

            except Exception as e:
                print(f"  ❌ Failed to add product '{product['name']}': {e}")

        print("\n🎉 Demo completed! Check the application for added products.")
        print("Press Enter to close the application...")
        input()

    except Exception as e:
        print(f"❌ Error during automation: {e}")

    finally:
        # Close the application
        try:
            main_window.close()
            print("✅ Application closed")
        except:
            print("⚠️  Could not close application gracefully")


def performance_monitoring_example():
    """Example of performance monitoring during automation."""
    print("\n📊 Performance Monitoring Example")
    print("=" * 40)

    import psutil
    import subprocess

    if not APP_EXECUTABLE.exists():
        print(f"❌ Application not found: {APP_EXECUTABLE}")
        return

    # Start application process
    print("📱 Starting application for performance monitoring...")
    process = subprocess.Popen([str(APP_EXECUTABLE)])

    try:
        # Wait for app to start
        time.sleep(3)

        # Get process info
        app_process = psutil.Process(process.pid)

        print(f"\n📈 Initial Performance Metrics:")
        print(f"  PID: {process.pid}")
        print(f"  Memory: {app_process.memory_info().rss / 1024 / 1024:.1f} MB")
        print(f"  CPU: {app_process.cpu_percent()}%")
        print(f"  Threads: {app_process.num_threads()}")

        # Monitor for a few seconds
        print("\n🔍 Monitoring for 10 seconds...")
        for i in range(10):
            time.sleep(1)
            try:
                cpu = app_process.cpu_percent()
                memory = app_process.memory_info().rss / 1024 / 1024
                threads = app_process.num_threads()

                print(
                    f"  [{i+1:2d}/10] Memory: {memory:6.1f} MB, CPU: {cpu:5.1f}%, Threads: {threads:2d}"
                )

            except psutil.NoSuchProcess:
                print("  ⚠️  Process terminated")
                break

        print("✅ Performance monitoring completed")

    except Exception as e:
        print(f"❌ Error during monitoring: {e}")

    finally:
        # Cleanup
        try:
            if process.poll() is None:
                process.terminate()
                time.sleep(1)
                if process.poll() is None:
                    process.kill()
            print("✅ Application process cleaned up")
        except Exception as e:
            print(f"⚠️  Cleanup error: {e}")


def test_data_generation_example():
    """Example of test data generation capabilities."""
    print("\n🎲 Test Data Generation Example")
    print("=" * 40)

    generator = ProductDataGenerator()

    # Generate different types of data
    print("📋 Available categories:")
    for category in generator.get_test_categories():
        print(f"  - {category}")

    print("\n📦 Sample generated products:")
    sample_products = generator.generate_product_batch(5)

    for i, product in enumerate(sample_products, 1):
        print(f"  {i}. {product['name']}")
        print(
            f"     SKU: {product['sku']} | Price: ${product['price']} | Qty: {product['quantity']} | Category: {product['category']}"
        )

    # Save sample data
    output_file = "example_generated_products.json"
    generator.save_generated_data(sample_products, output_file)
    print(f"\n💾 Sample data saved to: test_oracles/{output_file}")


def main():
    """Main example function."""
    print("🛠️  WPF Inventory Management App - Automation Examples")
    print("=" * 60)

    while True:
        print("\n🚀 Choose an example to run:")
        print("  1. Manual automation (add products to app)")
        print("  2. Performance monitoring")
        print("  3. Test data generation")
        print("  4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            manual_automation_example()
        elif choice == "2":
            performance_monitoring_example()
        elif choice == "3":
            test_data_generation_example()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
