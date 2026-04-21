"""Configuration file for WPF Inventory Management App automation testing."""

import os
from pathlib import Path

# Project root paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CSHARP_ROOT = PROJECT_ROOT / "csharp" / "desktop-apps" / "wpf"
WPF_APP_ROOT = CSHARP_ROOT / "WpfInventoryApp"

# Application executable paths
APP_EXECUTABLE_DEBUG = (
    WPF_APP_ROOT / "bin" / "Debug" / "net8.0-windows" / "WpfInventoryApp.exe"
)
APP_EXECUTABLE_RELEASE = (
    WPF_APP_ROOT / "bin" / "Release" / "net8.0-windows" / "WpfInventoryApp.exe"
)

# Default to debug build, fallback to release if not found
APP_EXECUTABLE = (
    APP_EXECUTABLE_DEBUG if APP_EXECUTABLE_DEBUG.exists() else APP_EXECUTABLE_RELEASE
)

# Test data paths
TEST_ORACLES_DIR = Path(__file__).parent / "test_oracles"
PRODUCT_DATA_FILE = TEST_ORACLES_DIR / "product_data.json"

# Application window and control identifiers (AutomationProperties.AutomationId)
APP_WINDOW_TITLE = "WPF Inventory Management System"
APP_WINDOW_TITLE_UIA = "inventory_management_main_window"
CONTROL_IDS = {
    # Main window elements
    "main_window": "inventory_main_window",
    "header_panel": "application_header_panel",
    "main_content_grid": "main_content_layout_grid",
    # Product form controls
    "product_name_textbox": "product_name_textbox",
    "product_sku_textbox": "product_sku_textbox",
    "product_price_textbox": "product_price_textbox",
    "product_quantity_textbox": "product_quantity_textbox",
    "product_category_combobox": "product_category_combobox",
    # Action buttons
    "add_product_button": "add_product_button",
    "edit_product_button": "edit_product_button",
    "delete_product_button": "delete_product_button",
    "save_product_button": "save_product_button",
    "cancel_product_button": "cancel_product_button",
    # Data grid
    "products_datagrid": "products_display_grid",
    # Search and filter
    "search_textbox": "search_filter_textbox",
    "search_button": "search_execute_button",
    "clear_search_button": "clear_search_filters_button",
    # Status and info
    "status_bar": "application_status_bar",
    "total_products_label": "total_products_count_label",
    "total_value_label": "inventory_total_value_label",
}

# Test execution settings
TEST_SETTINGS = {
    "app_startup_timeout": 10,  # seconds
    "element_timeout": 5,  # seconds
    "bulk_insert_count": 100,  # number of products for performance test
    "performance_sample_interval": 0.1,  # seconds between performance samples
    "screenshot_on_failure": True,
    "screenshot_dir": Path(__file__).parent / "screenshots",
}

# Performance monitoring settings
PERFORMANCE_SETTINGS = {
    "monitor_cpu": True,
    "monitor_memory": True,
    "monitor_handles": True,
    "monitor_threads": True,
    "sample_interval": 0.1,  # seconds
    "results_dir": Path(__file__).parent / "performance_results",
}

# Ensure directories exist
TEST_ORACLES_DIR.mkdir(exist_ok=True)
TEST_SETTINGS["screenshot_dir"].mkdir(exist_ok=True)
PERFORMANCE_SETTINGS["results_dir"].mkdir(exist_ok=True)
