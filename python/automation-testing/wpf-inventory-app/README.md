# WPF Inventory Management App - Automation Testing Framework

A comprehensive automation testing framework for the WPF Inventory Management Application using PyWinAuto, pytest, and performance monitoring tools.

## Overview

This framework provides:
- **UI Automation**: Complete automation of WPF application using PyWinAuto
- **Performance Testing**: Monitor CPU, memory, and throughput during bulk operations
- **Test Data Generation**: Realistic product data with permutations for comprehensive testing
- **Continuous Integration Ready**: Structured for CI/CD pipelines with detailed reporting

## Project Structure

```
wpf-inventory-app/
├── config.py                 # Configuration and application paths
├── conftest.py              # PyTest fixtures and app lifecycle management
├── data_generator.py        # Test data generation utilities
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── test_oracles/           # Test data and oracles
│   ├── product_data.json   # Base product templates
│   ├── performance_test_products.json  # Generated performance test data
│   └── general_test_products.json      # Generated general test data
├── tests/                  # Test suites
│   ├── test_basic_functionality.py     # Basic CRUD and UI tests
│   ├── test_performance.py             # Performance and stress tests
│   └── __init__.py
├── screenshots/           # Failure screenshots (auto-created)
└── performance_results/   # Performance test results (auto-created)
```

## Quick Start

### Prerequisites

1. **WPF Application**: Ensure the WPF Inventory Management App is built:
   ```bash
   cd C:\projects\github\amalie_projects\csharp\desktop-apps\wpf
   dotnet build
   ```

2. **Python Environment**: Python 3.8+ recommended
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

**Basic Functionality Tests:**
```bash
pytest tests/test_basic_functionality.py -v
```

**Performance Tests:**
```bash
pytest tests/test_performance.py -v -m "not slow"
```

**Full Performance Suite (includes 100-item bulk test):**
```bash
pytest tests/test_performance.py -v
```

**All Tests with HTML Report:**
```bash
pytest -v --html=report.html --self-contained-html
```

**Parallel Execution:**
```bash
pytest -n auto -v
```

## Performance Testing

### Bulk Insert Performance Test

The framework includes a comprehensive performance test that:
- Inserts 100 products continuously
- Monitors CPU, memory, thread count, and handle usage
- Measures insertion throughput and response times
- Generates detailed performance reports

**Key Metrics Tracked:**
- **Throughput**: Products inserted per second
- **Response Time**: Average time per insertion
- **Memory Usage**: Peak and average memory consumption
- **CPU Usage**: Processing overhead
- **UI Responsiveness**: Interface lag under load

### Performance Results

Results are automatically saved to `performance_results/` with detailed JSON reports containing:
- Execution timestamps
- Success/failure rates
- Performance statistics
- Resource utilization metrics

## Configuration

### Application Paths (`config.py`)

The framework automatically detects the WPF application executable:
- **Debug Build**: `bin/Debug/net8.0-windows/WpfInventoryApp.exe`
- **Release Build**: `bin/Release/net8.0-windows/WpfInventoryApp.exe`

### Control Identifiers

All UI controls are identified using AutomationProperties.AutomationId:
```python
CONTROL_IDS = {
    "product_name_textbox": "product_name_textbox",
    "add_product_button": "add_product_button",
    "products_datagrid": "products_display_grid",
    # ... more controls
}
```

### Test Settings

Customize test behavior:
```python
TEST_SETTINGS = {
    "app_startup_timeout": 10,        # Application startup wait time
    "element_timeout": 5,             # UI element search timeout
    "bulk_insert_count": 100,         # Number of products for performance test
    "screenshot_on_failure": True,    # Capture screenshots on test failure
}
```

## Test Data Generation

### Product Data Templates

The framework generates realistic test data using configurable templates in `test_oracles/product_data.json`:
- **Categories**: Electronics, Clothing, Home & Garden, etc.
- **Name Variations**: Adjectives, colors, sizes
- **Price Ranges**: Category-appropriate pricing
- **SKU Patterns**: Formatted with random IDs

### Data Generator Usage

```python
from data_generator import ProductDataGenerator

generator = ProductDataGenerator()

# Generate single product
product = generator.generate_random_product()

# Generate batch for testing
products = generator.generate_product_batch(50)

# Generate performance test data
perf_data = generator.generate_performance_test_data(100)
```

## Test Categories

### Basic Functionality Tests
- **Application Startup**: Verify app launches correctly
- **UI Element Presence**: Check all controls are accessible
- **Single Product Addition**: Test basic CRUD operations
- **Form Validation**: Test input validation and error handling
- **Search Functionality**: Test product search features
- **Data Grid Interaction**: Test table/grid operations

### Performance Tests
- **Bulk Insert Performance**: 100-product continuous insertion
- **Memory Stability**: Monitor memory leaks during extended operation
- **UI Responsiveness**: Measure interface lag under load

## Failure Diagnostics

**Automatic Screenshots**: Screenshots are captured on test failures and saved to `screenshots/`

**Detailed Logging**: Comprehensive logging with timestamps and context

**Performance Profiles**: Detailed resource usage reports for performance analysis

## Extending the Framework

### Adding New Tests

1. Create test files in `tests/` directory
2. Use the `app_window` fixture for application access
3. Use `performance_monitor` fixture for resource monitoring
4. Follow the established patterns for control identification

### Adding New Controls

1. Update `CONTROL_IDS` in `config.py` with AutomationId
2. Ensure WPF app has corresponding `AutomationProperties.AutomationId` set
3. Create helper methods in test classes for control interaction

### Custom Test Data

1. Extend `product_data.json` with new templates
2. Modify `ProductDataGenerator` for custom data patterns
3. Create specialized data generation methods as needed

## Performance Benchmarks

**Expected Performance Targets:**
- **Insertion Rate**: > 0.2 products/second
- **Average Response**: < 5 seconds per insertion
- **UI Response**: < 1 second average, < 3 seconds maximum
- **Memory Growth**: < 50% increase during bulk operations
- **Peak Memory**: < 500 MB

## Troubleshooting

### Common Issues

**Application Not Found:**
- Ensure WPF app is built: `dotnet build`
- Check paths in `config.py`
- Verify executable exists in expected location

**Control Not Found:**
- Verify AutomationId matches between test and WPF app
- Check if control is visible and enabled
- Increase timeout values if needed

**Performance Test Failures:**
- Close other applications to free resources
- Run tests on a dedicated test machine
- Adjust performance thresholds in test assertions

### Debug Mode

```bash
# Run with verbose logging
pytest -v -s --log-cli-level=INFO

# Run single test with full output
pytest tests/test_basic_functionality.py::TestBasicFunctionality::test_add_single_product -v -s
```

## Reporting

**HTML Reports**: Use `--html=report.html` for detailed test reports

**Performance Reports**: JSON files with detailed metrics in `performance_results/`

**Screenshots**: Automatic failure screenshots in `screenshots/`

**Console Output**: Real-time logging with progress indicators

---

## Contributing

When adding new tests or features:
1. Follow existing code patterns and naming conventions
2. Add appropriate logging and error handling
3. Update this README with new functionality
4. Ensure tests are reliable and not flaky
5. Add performance assertions where appropriate

## License

This testing framework is part of the Amalie Development Portfolio project.
