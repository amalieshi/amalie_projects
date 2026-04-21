# WPF Inventory Management System

- **📂 Project Path**: `csharp/desktop-apps/wpf/WpfInventoryApp/`
- **🔗 GitHub Repository**: [https://github.com/AmalieShi/amalie_projects](https://github.com/AmalieShi/amalie_projects)

A comprehensive WPF desktop application built with enterprise-grade MVVM architecture for inventory management.

## Architecture

### Design Patterns
- **MVVM (Model-View-ViewModel)**: Strict separation of concerns
- **Repository Pattern**: Decoupled data access layer from business logic
- **Dependency Injection**: Microsoft.Extensions.DependencyInjection
- **Command Pattern**: RelayCommand and AsyncRelayCommand implementations

### Technology Stack
- **.NET 8**: Modern C# with latest features
- **WPF**: Rich desktop user interface
- **Entity Framework Core**: ORM with SQLite database
- **xUnit + FluentAssertions**: Comprehensive unit testing
- **Microsoft Extensions**: Configuration, Logging, DI

## Database Schema

### Products Table
```sql
CREATE TABLE Products (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT(100) NOT NULL,
    SKU TEXT(50) NOT NULL UNIQUE,
    Quantity INTEGER NOT NULL DEFAULT 0,
    Price DECIMAL(18,2) NOT NULL,
    CreatedAt DATETIME DEFAULT (datetime('now')),
    UpdatedAt DATETIME DEFAULT (datetime('now'))
);
```

## Features

### CRUD Operations
- ✅ **Create**: Add new products with validation
- ✅ **Read**: View all products in sortable DataGrid
- ✅ **Update**: Edit existing products with form validation
- ✅ **Delete**: Remove products with confirmation dialog

### Data Management
- **SQLite Database**: Lightweight, file-based storage
- **Entity Framework Core**: Code-first migrations
- **Unique SKU Validation**: Prevents duplicate product codes
- **Automatic Timestamps**: CreatedAt and UpdatedAt tracking

### User Experience
- **Responsive UI**: Modern WPF styling with visual feedback
- **Real-time Validation**: Input validation with error messages
- **Status Updates**: Progress indicators and status messages
- **Keyboard Navigation**: Full keyboard accessibility

## Configuration

### Environment Variables
```bash
# Database connection string (optional)
INVENTORY_DB_CONNECTION="Data Source=custom_inventory.db;Cache=Shared"
```

### appsettings.json
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=inventory.db;Cache=Shared"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  }
}
```

## Quality Assurance

### Unit Testing Coverage
- ✅ **Repository CRUD Operations**: All database operations tested
- ✅ **Data Validation**: Input validation and business rules
- ✅ **Error Handling**: Exception scenarios and edge cases
- ✅ **Memory Management**: Disposal and leak prevention
- ✅ **Connection Handling**: Database connection lifecycle

### Test Categories
1. **Functional Tests**: CRUD operations validation
2. **Integration Tests**: Database interaction testing
3. **Performance Tests**: Memory leak detection
4. **Boundary Tests**: Edge case handling

## Development Setup

### Prerequisites
- .NET 8 SDK
- Visual Studio 2022 or VS Code
- SQLite (embedded)

### Installation
```bash
# Clone repository
git clone https://github.com/AmalieShi/amalie_projects.git
cd amalie_projects/csharp/desktop-apps/wpf/WpfInventoryApp

# Restore dependencies
dotnet restore

# Build solution
dotnet build

# Run application
dotnet run
```

### Running Tests
```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"

# Run specific test category
dotnet test --filter "Category=Repository"
```

## 📁 Project Structure

```
WpfInventoryApp/
├── Commands/              # MVVM Command implementations
│   ├── RelayCommand.cs
│   └── AsyncRelayCommand.cs
├── Data/                  # Entity Framework DbContext
│   └── InventoryDbContext.cs
├── Models/                # Data models
│   └── Product.cs
├── Repositories/          # Repository pattern implementation
│   ├── IProductRepository.cs
│   └── ProductRepository.cs
├── ViewModels/            # MVVM ViewModels
│   ├── ViewModelBase.cs
│   ├── ProductViewModel.cs
│   └── MainViewModel.cs
├── Views/                 # WPF Views
│   ├── MainWindow.xaml
│   └── MainWindow.xaml.cs
├── App.xaml              # Application resources
├── App.xaml.cs           # Application startup
└── appsettings.json      # Configuration

WpfInventoryApp.Tests/
└── Repositories/         # Unit tests
    └── ProductRepositoryTests.cs
```

## Security & Best Practices

### Database Security
- **Parameterized Queries**: SQL injection prevention
- **Connection String Protection**: Environment variable support
- **Data Validation**: Input sanitization and validation

### Memory Management
- **IDisposable Implementation**: Proper resource cleanup
- **DbContext Scoping**: Dependency injection lifecycle management
- **Memory Leak Prevention**: Verified through unit tests

### Code Quality
- **SOLID Principles**: Clean architecture implementation
- **Separation of Concerns**: MVVM pattern enforcement
- **Error Handling**: Comprehensive exception management
- **Logging**: Structured logging with Microsoft.Extensions.Logging

## 📈 Performance Characteristics

- **Database**: SQLite with Entity Framework Core optimization
- **UI Responsiveness**: Async operations with progress indicators
- **Memory Footprint**: Lightweight with proper disposal patterns
- **Startup Time**: Fast initialization with dependency injection

## Contributing

This project follows enterprise development standards:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Write tests for new functionality
4. Ensure all tests pass (`dotnet test`)
5. Commit changes (`git commit -m 'Add AmazingFeature'`)
6. Push to branch (`git push origin feature/AmazingFeature`)
7. Open Pull Request

## License

This project is part of the Amalie Projects portfolio and is available under the Apache License.