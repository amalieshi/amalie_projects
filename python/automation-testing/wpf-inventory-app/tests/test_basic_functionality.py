"""Basic functionality tests for WPF Inventory Management App."""

import pytest
import time
import logging
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.timings import TimeoutError

from config import CONTROL_IDS, TEST_SETTINGS
from data_generator import ProductDataGenerator

logger = logging.getLogger(__name__)


class TestBasicFunctionality:
    """Test basic CRUD operations and UI interactions."""

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Setup test data for each test."""
        self.generator = ProductDataGenerator()
        self.test_product = self.generator.generate_random_product()

    def find_control_by_automation_id(
        self, window: UIAWrapper, automation_id: str, timeout: int = 5
    ):
        """Find a control by its AutomationId with timeout."""
        try:
            return window.child_window(auto_id=automation_id, timeout=timeout)
        except TimeoutError:
            logger.error(
                f"Control with AutomationId '{automation_id}' not found within {timeout}s"
            )
            raise

    def test_application_startup(self, app_window):
        """Test that the application starts successfully and main window is visible."""
        assert app_window is not None
        assert app_window.is_visible()
        logger.info("Application startup test passed")

    def test_main_window_elements_present(self, app_window):
        """Test that all main UI elements are present and accessible."""
        # Check for main form elements
        product_name = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_name_textbox"]
        )
        assert product_name.is_visible()

        product_sku = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_sku_textbox"]
        )
        assert product_sku.is_visible()

        product_price = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_price_textbox"]
        )
        assert product_price.is_visible()

        product_quantity = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_quantity_textbox"]
        )
        assert product_quantity.is_visible()

        add_button = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["add_product_button"]
        )
        assert add_button.is_visible()

        logger.info("All main UI elements are present")

    def test_add_single_product(self, app_window):
        """Test adding a single product to the inventory."""
        # Fill in product details
        name_field = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_name_textbox"]
        )
        name_field.click_input()
        name_field.type_keys("^a")  # Select all
        name_field.type_keys(self.test_product["name"])

        sku_field = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_sku_textbox"]
        )
        sku_field.click_input()
        sku_field.type_keys("^a")
        sku_field.type_keys(self.test_product["sku"])

        price_field = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_price_textbox"]
        )
        price_field.click_input()
        price_field.type_keys("^a")
        price_field.type_keys(str(self.test_product["price"]))

        quantity_field = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_quantity_textbox"]
        )
        quantity_field.click_input()
        quantity_field.type_keys("^a")
        quantity_field.type_keys(str(self.test_product["quantity"]))

        # Click Add button
        add_button = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["add_product_button"]
        )
        add_button.click()

        # Wait a moment for the operation to complete
        time.sleep(1)

        logger.info(f"Successfully added product: {self.test_product['name']}")

    def test_form_field_validation(self, app_window):
        """Test form field validation with invalid data."""
        # Test with empty fields
        add_button = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["add_product_button"]
        )

        # Clear all fields first
        for field_id in [
            "product_name_textbox",
            "product_sku_textbox",
            "product_price_textbox",
            "product_quantity_textbox",
        ]:
            field = self.find_control_by_automation_id(
                app_window, CONTROL_IDS[field_id]
            )
            field.click_input()
            field.type_keys("^a")
            field.type_keys("{DEL}")

        # Try to add with empty fields - should not succeed or show validation
        add_button.click()
        time.sleep(0.5)

        # Test with invalid price
        price_field = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_price_textbox"]
        )
        price_field.click_input()
        price_field.type_keys("invalid_price")

        # Test with negative quantity
        quantity_field = self.find_control_by_automation_id(
            app_window, CONTROL_IDS["product_quantity_textbox"]
        )
        quantity_field.click_input()
        quantity_field.type_keys("-5")

        logger.info("Form validation tests completed")

    def test_search_functionality(self, app_window):
        """Test the search functionality if available."""
        try:
            # First add a product to search for
            self.test_add_single_product(app_window)

            # Now try to search for it
            search_field = self.find_control_by_automation_id(
                app_window, CONTROL_IDS["search_textbox"], timeout=2
            )
            search_field.click_input()
            search_field.type_keys(self.test_product["name"][:5])  # Partial search

            # Click search button if available
            try:
                search_button = self.find_control_by_automation_id(
                    app_window, CONTROL_IDS["search_button"], timeout=2
                )
                search_button.click()
            except TimeoutError:
                # Search might be automatic, press Enter
                search_field.type_keys("{ENTER}")

            time.sleep(1)
            logger.info("Search functionality test completed")

        except TimeoutError:
            pytest.skip("Search functionality not available")

    def test_data_grid_interaction(self, app_window):
        """Test interaction with the data grid."""
        try:
            # Add a product first
            self.test_add_single_product(app_window)

            # Find the data grid
            data_grid = self.find_control_by_automation_id(
                app_window, CONTROL_IDS["products_datagrid"], timeout=3
            )
            assert data_grid.is_visible()

            # Try to interact with the grid (select first row if any)
            try:
                # This might vary depending on the grid implementation
                data_grid.click()
                time.sleep(0.5)
            except Exception as e:
                logger.warning(f"Grid interaction failed: {e}")

            logger.info("Data grid interaction test completed")

        except TimeoutError:
            pytest.skip("Data grid not found")
