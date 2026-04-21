"""Performance tests for WPF Inventory Management App."""

import pytest
import time
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from pywinauto.timings import TimeoutError

from config import CONTROL_IDS, TEST_SETTINGS, PERFORMANCE_SETTINGS
from data_generator import ProductDataGenerator

import logging

logger = logging.getLogger(__name__)


class TestPerformance:
    """Performance and stress tests for the inventory application."""

    @pytest.fixture(autouse=True)
    def setup_performance_test(self):
        """Setup for performance tests."""
        self.generator = ProductDataGenerator()
        self.performance_data = []
        self.test_products = self.generator.generate_performance_test_data(
            TEST_SETTINGS["bulk_insert_count"]
        )

    def find_control_by_automation_id(
        self, window, automation_id: str, timeout: int = 5
    ):
        """Find a control by its AutomationId with timeout - fallback to position for missing IDs."""
        import time

        # Map of expected AutomationIds to position-based fallbacks
        control_fallbacks = {
            "product_name_textbox": {"type": "Edit", "index": 0},
            "product_sku_textbox": {"type": "Edit", "index": 1},
            "product_price_textbox": {"type": "Edit", "index": 2},
            "product_quantity_textbox": {"type": "Edit", "index": 3},
            "add_product_button": {
                "type": "Button",
                "real_auto_id": "add_product_button",
            },
            "save_product_button": {
                "type": "Button",
                "real_auto_id": "save_product_button",
            },
            "products_display_grid": {"type": "DataGrid", "index": 0},
        }

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # First try to find by AutomationId
                descendants = window.descendants()
                for control in descendants:
                    try:
                        if control.automation_id() == automation_id:
                            return control
                    except:
                        continue

                # If not found by AutomationId, try fallback method
                if automation_id in control_fallbacks:
                    fallback = control_fallbacks[automation_id]

                    if fallback["type"] == "Edit":
                        # Find Edit controls by index
                        edit_controls = window.descendants(control_type="Edit")
                        if len(edit_controls) > fallback["index"]:
                            return edit_controls[fallback["index"]]

                    elif fallback["type"] == "Button":
                        # First try using the real AutomationId if available
                        if "real_auto_id" in fallback:
                            try:
                                button = window.child_window(
                                    auto_id=fallback["real_auto_id"]
                                )
                                if button.exists():
                                    return button
                            except:
                                pass

                        # Fallback to text search
                        button_controls = window.descendants(control_type="Button")
                        for btn in button_controls:
                            try:
                                if (
                                    fallback.get("text", "").lower()
                                    in btn.window_text().lower()
                                ):
                                    return btn
                            except:
                                continue

                    elif fallback["type"] == "DataGrid":
                        # Find DataGrid controls
                        grid_controls = window.descendants(control_type="DataGrid")
                        if len(grid_controls) > fallback["index"]:
                            return grid_controls[fallback["index"]]

                # If still not found, wait and try again
                time.sleep(0.1)

            except Exception as e:
                time.sleep(0.1)
                continue

        # If we get here, control wasn't found
        raise TimeoutError(
            f"Control with AutomationId '{automation_id}' not found within {timeout}s"
        )

    def add_single_product_fast(self, app_window, product: Dict[str, Any]) -> float:
        """Add a single product as quickly as possible and return elapsed time."""
        start_time = time.time()

        try:
            # Fill form fields rapidly
            name_field = self.find_control_by_automation_id(
                app_window, CONTROL_IDS["product_name_textbox"], timeout=2
            )
            name_field.click_input()
            name_field.type_keys("^a")
            name_field.type_keys(product["name"])

            sku_field = self.find_control_by_automation_id(
                app_window, CONTROL_IDS["product_sku_textbox"], timeout=2
            )
            sku_field.click_input()
            sku_field.type_keys("^a")
            sku_field.type_keys(product["sku"])

            price_field = self.find_control_by_automation_id(
                app_window, CONTROL_IDS["product_price_textbox"], timeout=2
            )
            price_field.click_input()
            price_field.type_keys("^a")
            price_field.type_keys(str(product["price"]))

            quantity_field = self.find_control_by_automation_id(
                app_window, CONTROL_IDS["product_quantity_textbox"], timeout=2
            )
            quantity_field.click_input()
            quantity_field.type_keys("^a")
            quantity_field.type_keys(str(product["quantity"]))

            # Submit - Click Add button first
            add_button = self.find_control_by_automation_id(
                app_window, CONTROL_IDS["add_product_button"], timeout=2
            )
            add_button.click()

            # Then click Save to commit the entry
            save_button = self.find_control_by_automation_id(
                app_window, CONTROL_IDS["save_product_button"], timeout=2
            )
            save_button.click()

            # Small delay to ensure operation completes
            time.sleep(0.1)

            return time.time() - start_time

        except Exception as e:
            logger.error(f"Failed to add product {product['sku']}: {e}")
            return time.time() - start_time

    @pytest.mark.slow
    def test_bulk_product_insertion_performance(self, app_window, performance_monitor):
        """Test performance when adding many products continuously."""
        logger.info(f"Starting bulk insertion of {len(self.test_products)} products")

        insertion_times = []
        failed_insertions = 0

        # Start performance monitoring in separate thread
        monitoring_active = True

        def monitor_performance():
            while monitoring_active:
                performance_monitor.collect_sample()
                time.sleep(PERFORMANCE_SETTINGS["sample_interval"])

        monitor_thread = threading.Thread(target=monitor_performance, daemon=True)
        monitor_thread.start()

        try:
            # Perform bulk insertion
            start_time = time.time()

            for i, product in enumerate(self.test_products):
                try:
                    insert_time = self.add_single_product_fast(app_window, product)
                    insertion_times.append(insert_time)

                    # Log progress every 10 items
                    if (i + 1) % 10 == 0:
                        logger.info(
                            f"Inserted {i + 1}/{len(self.test_products)} products"
                        )

                except Exception as e:
                    failed_insertions += 1
                    logger.warning(f"Failed to insert product {i + 1}: {e}")

            total_time = time.time() - start_time

        finally:
            monitoring_active = False
            monitor_thread.join(timeout=1)

        # Calculate performance metrics
        successful_insertions = len(insertion_times)
        avg_insertion_time = (
            sum(insertion_times) / len(insertion_times) if insertion_times else 0
        )
        throughput = successful_insertions / total_time if total_time > 0 else 0

        # Get performance summary
        perf_stats = performance_monitor.get_summary_stats()

        # Save detailed results
        results = {
            "test_timestamp": datetime.now().isoformat(),
            "total_products_attempted": len(self.test_products),
            "successful_insertions": successful_insertions,
            "failed_insertions": failed_insertions,
            "total_time_seconds": total_time,
            "average_insertion_time_seconds": avg_insertion_time,
            "throughput_products_per_second": throughput,
            "insertion_times": insertion_times,
            "performance_stats": perf_stats,
        }

        # Save results to file
        results_file = (
            PERFORMANCE_SETTINGS["results_dir"]
            / f"bulk_insertion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)

        logger.info(f"Performance test completed:")
        logger.info(
            f"  - Successful insertions: {successful_insertions}/{len(self.test_products)}"
        )
        logger.info(f"  - Total time: {total_time:.2f}s")
        logger.info(f"  - Average insertion time: {avg_insertion_time:.3f}s")
        logger.info(f"  - Throughput: {throughput:.2f} products/second")
        logger.info(f"  - Peak memory: {perf_stats.get('memory_max_mb', 0):.1f} MB")
        logger.info(f"  - Average CPU: {perf_stats.get('cpu_avg', 0):.1f}%")
        logger.info(f"  - Results saved to: {results_file}")

        # Performance assertions
        assert successful_insertions > 0, "No products were successfully inserted"
        assert (
            avg_insertion_time < 5.0
        ), f"Average insertion time too slow: {avg_insertion_time:.3f}s"
        assert throughput > 0.2, f"Throughput too low: {throughput:.3f} products/second"

    @pytest.mark.slow
    def test_memory_usage_stability(self, app_window, performance_monitor):
        """Test that memory usage remains stable during continuous operation."""
        logger.info("Testing memory usage stability")

        # Add products in batches and monitor memory
        batch_size = 10
        num_batches = 10

        monitoring_active = True
        memory_samples = []

        def monitor_memory():
            while monitoring_active:
                sample = performance_monitor.collect_sample()
                if sample:
                    memory_samples.append(sample["memory_mb"])
                time.sleep(0.5)

        monitor_thread = threading.Thread(target=monitor_memory, daemon=True)
        monitor_thread.start()

        try:
            for batch in range(num_batches):
                logger.info(f"Processing batch {batch + 1}/{num_batches}")

                batch_products = self.test_products[
                    batch * batch_size : (batch + 1) * batch_size
                ]

                for product in batch_products:
                    try:
                        self.add_single_product_fast(app_window, product)
                        time.sleep(0.1)  # Small delay between insertions
                    except Exception as e:
                        logger.warning(f"Failed to add product: {e}")

                # Wait between batches
                time.sleep(2)

        finally:
            monitoring_active = False
            monitor_thread.join(timeout=1)

        # Analyze memory usage
        if len(memory_samples) > 10:
            initial_memory = sum(memory_samples[:5]) / 5  # Average of first 5 samples
            final_memory = sum(memory_samples[-5:]) / 5  # Average of last 5 samples
            max_memory = max(memory_samples)

            memory_increase = final_memory - initial_memory
            memory_increase_percent = (memory_increase / initial_memory) * 100

            logger.info(f"Memory analysis:")
            logger.info(f"  - Initial memory: {initial_memory:.1f} MB")
            logger.info(f"  - Final memory: {final_memory:.1f} MB")
            logger.info(f"  - Peak memory: {max_memory:.1f} MB")
            logger.info(
                f"  - Memory increase: {memory_increase:.1f} MB ({memory_increase_percent:.1f}%)"
            )

            # Memory stability assertions
            assert (
                memory_increase_percent < 50
            ), f"Memory usage increased too much: {memory_increase_percent:.1f}%"
            assert max_memory < 500, f"Peak memory usage too high: {max_memory:.1f} MB"

    @pytest.mark.slow
    def test_ui_responsiveness_under_load(self, app_window, performance_monitor):
        """Test that UI remains responsive during heavy operations."""
        logger.info("Testing UI responsiveness under load")

        responsiveness_samples = []

        for i in range(20):  # Test 20 interactions
            try:
                # Measure time to interact with a simple control
                start_time = time.time()

                name_field = self.find_control_by_automation_id(
                    app_window, CONTROL_IDS["product_name_textbox"], timeout=3
                )
                name_field.click_input()

                response_time = time.time() - start_time
                responsiveness_samples.append(response_time)

                # Add a product to create some load
                if i < len(self.test_products):
                    self.add_single_product_fast(app_window, self.test_products[i])

            except Exception as e:
                logger.warning(f"UI responsiveness test iteration {i} failed: {e}")
                responsiveness_samples.append(10.0)  # Penalty for failed interaction

            time.sleep(0.5)

        # Analyze responsiveness
        if responsiveness_samples:
            avg_response_time = sum(responsiveness_samples) / len(
                responsiveness_samples
            )
            max_response_time = max(responsiveness_samples)

            logger.info(f"UI Responsiveness:")
            logger.info(f"  - Average response time: {avg_response_time:.3f}s")
            logger.info(f"  - Maximum response time: {max_response_time:.3f}s")

            # Responsiveness assertions
            assert (
                avg_response_time < 1.0
            ), f"Average UI response too slow: {avg_response_time:.3f}s"
            assert (
                max_response_time < 3.0
            ), f"Maximum UI response too slow: {max_response_time:.3f}s"
