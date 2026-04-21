# WPF UI Automation Reference Guide

## Overview
This document provides comprehensive guidance for UI automation testing support in the WPF Inventory Management System. All controls now have automation properties equivalent to your QML experience.

## WPF Automation Properties (QML Equivalents)

| WPF Property | QML Equivalent | Purpose |
|--------------|----------------|---------|
| `AutomationProperties.AutomationId` | `objectName` | Unique identifier for test automation |
| `AutomationProperties.Name` | `Accessible.name` | Human-readable description |
| `AutomationProperties.LabeledBy` | - | Associates controls with their labels |
| `AutomationProperties.HelpText` | - | Additional accessibility description |

## Control Automation IDs

### Window & Main Elements
- **main_window** - Main application window
- **app_title** - Application title text
- **status_bar** - Status bar container
- **products_datagrid** - Main products data grid

### Navigation & Action Buttons  
- **refresh_button** - Refresh products data
- **add_product_button** - Add new product
- **edit_product_button** - Edit selected product  
- **delete_product_button** - Delete selected product

### Form Input Controls
- **product_name_textbox** - Product name input field
- **product_sku_textbox** - Product SKU input field
- **product_quantity_textbox** - Product quantity input field
- **product_price_textbox** - Product price input field

### Form Action Buttons
- **save_product_button** - Save new product (add mode)
- **update_product_button** - Update existing product (edit mode)
- **cancel_edit_button** - Cancel edit operation
- **clear_form_button** - Clear form fields

### Status & Information Elements
- **status_message_text** - Application status messages
- **product_count_text** - Total products count display
- **loading_progress_bar** - Loading indicator

## Naming Conventions

Following your QML experience, all automation IDs use:
- **lowercase** letters
- **underscores** (_) as separators  
- **descriptive** names indicating purpose
- **consistent** patterns across similar controls

### Pattern Examples:
```
{control_purpose}_{control_type}
product_name_textbox
refresh_button
products_datagrid
```

## Test Automation Usage

### C# Test Frameworks (MS Test, NUnit, xUnit)
```csharp
// Using TestStack.White
var window = Application.GetWindow("main_window");
var addButton = window.Get<Button>("add_product_button");
var nameTextBox = window.Get<TextBox>("product_name_textbox");

// Using FlaUI  
var window = app.GetMainWindow();
var addButton = window.FindFirstDescendant(cf => cf.ByAutomationId("add_product_button"));
var nameTextBox = window.FindFirstDescendant(cf => cf.ByAutomationId("product_name_textbox"));
```

### PowerShell (UI Automation)
```powershell
# Find elements by AutomationId
$window = Get-UiaWindow -Name "*Inventory Management*"
$addButton = $window | Get-UiaButton -AutomationId "add_product_button"
$nameTextBox = $window | Get-UiaEdit -AutomationId "product_name_textbox"
```

### Coded UI Tests (Visual Studio)
```csharp
[TestMethod]
public void TestAddProduct()
{
    // Find controls by automation properties
    var addButton = this.UIInventoryManagementWindow
                        .UIAddProductButton; // Maps to AutomationId="add_product_button"
    var nameTextBox = this.UIInventoryManagementWindow
                          .UIProductNameTextBox; // Maps to AutomationId="product_name_textbox"
}
```

## Best Practices

### 1. Consistent Naming
- Use the established naming convention for new controls
- Update automation properties when control purpose changes
- Keep names unique across the application

### 2. Contextual Information  
- Include relevant context in automation names
- Use descriptive suffixes (\_button, \_textbox, \_datagrid)
- Make names self-documenting for test engineers

### 3. Accessibility Support
```xml
<!-- Example with full accessibility support -->
<TextBox AutomationProperties.AutomationId="product_name_textbox"
         AutomationProperties.Name="product_name_input_field"
         AutomationProperties.HelpText="Enter the product name for inventory tracking"
         AutomationProperties.LabeledBy="{Binding ElementName=ProductNameLabel}"/>
```

### 4. Dynamic Content Support
For dynamic controls, use data binding in automation properties:
```xml
<Button AutomationProperties.AutomationId="edit_product_button"
        AutomationProperties.Name="{Binding SelectedProduct.Name, 
                                   StringFormat='edit_product_{0}_button'}"/>
```

## Testing Scenarios

### Complete Test Flow Example:
1. **Startup**: Verify main_window loads
2. **Navigation**: Click refresh_button  
3. **Data Entry**: 
   - Enter text in product_name_textbox
   - Enter text in product_sku_textbox
   - Enter numbers in product_quantity_textbox
   - Enter price in product_price_textbox
4. **Actions**: Click save_product_button
5. **Verification**: Check products_datagrid contains new item
6. **Status**: Verify status_message_text shows success

### Error Handling Tests:
- Test validation with empty fields
- Test edit/cancel workflows 
- Test delete confirmations
- Test loading states via loading_progress_bar

## Integration with CI/CD

Add automation tests to your build pipeline:
```yaml
# Azure DevOps example
- task: VSTest@2
  displayName: 'Run UI Automation Tests'
  inputs:
    testSelector: 'testAssemblies'
    testAssemblyVer2: |
      **\*UITests*.dll
    searchFolder: '$(System.DefaultWorkingDirectory)'
```

## Future Extensions

When adding new views or controls:
1. Follow the established naming convention
2. Add automation properties to all interactive elements  
3. Update this reference document
4. Create corresponding test cases
5. Verify accessibility compliance

## Tools & Resources

### Recommended Testing Frameworks:
- **TestStack.White** - Simple WPF automation
- **FlaUI** - Modern UI automation framework
- **Appium for Windows** - Cross-platform automation
- **Microsoft UI Automation** - Native Windows support

### Inspection Tools:
- **Accessibility Insights** - Microsoft's accessibility inspector
- **UI Spy** - Legacy but useful automation inspector  
- **FlaUI Inspect** - Modern inspection tool
- **Windows SDK Inspect** - Built-in Windows tool

---

*This automation implementation follows established QML patterns and provides comprehensive test automation support for the WPF Inventory Management System.*