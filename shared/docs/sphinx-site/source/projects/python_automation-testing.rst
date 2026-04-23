
Python Automation-Testing Projects  
==================================

This section showcases all python automation-testing projects with their documentation and source code.

.. admonition:: Navigation Tip
   :class: tip

   Click on any project card to view its complete documentation, or use the dropdown to preview key information.



.. grid:: 1 2 2 2
   :gutter: 3
   :margin: 2

   .. grid-item-card:: WPF Inventory Management App - Automation Testing Framework
      :link: python_automation-testing_wpf_inventory_app
      :link-type: doc
      :class-card: project-card
      :text-align: left

      A comprehensive automation testing framework for the WPF Inventory Management Application using PyWinAuto, pytest, and performance monitoring tools.
   
   :bdg-secondary:`Performance Testing`
   :bdg-secondary:`PyTest`
   :bdg-secondary:`PyWinAuto`
   :bdg-secondary:`Python`
   :bdg-secondary:`UI Automation`
   :bdg-secondary:`WPF`
      
      +++
      
      .. button-link:: python_automation-testing_wpf_inventory_app
         :color: primary
         :outline:
         :expand:
         
         View Details →



**Quick Preview**
^^^^^^^^^^^^^^^^^^

.. tab-set::


   .. tab-item:: WPF Inventory Management App - Automation Testing Framework

      A comprehensive automation testing framework for the WPF Inventory Management Application using PyWinAuto, pytest, and performance monitoring tools.
      
      **Technologies:** Performance Testing, PyTest, PyWinAuto, Python, UI Automation, WPF
      
      .. dropdown:: Quick Preview
         :color: info
         :icon: book

         A comprehensive automation testing framework for the WPF Inventory Management Application using PyWinAuto, pytest, and performance monitoring tools.
- **📂 Project Path**: `python\automation-testing`
- **🔗 GitHub Repository**: [https://github.com/AmalieShi/amalie_projects](https://github.com/AmalieShi/amalie_projects)

Overview
--------

This framework provides:
- **UI Automation**: Complete automation of WPF application using PyWinAuto
- **Performance Testing**: Monitor CPU, memory, and throughput during bulk operations
- **Test Data Generation**: Realistic product data with permutations for comprehensive testing
- **Continuous Integration Ready**: Structured for CI/CD pipelines with detailed reporting

Project Structure
-----------------


.. code-block:: text

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

Quick Start
-----------


Prerequisites
^^^^^^^^^^^^^

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
         
         :doc:`View Full Documentation → <python_automation-testing_wpf_inventory_app>`

