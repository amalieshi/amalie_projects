# C# Development Projects

This folder contains C# projects organized by application type and technology stack.

## Project Structure

### Web Development
- **[aspnet-core/](web-development/aspnet-core/)** - ASP.NET Core web applications and APIs
- **[web-apis/](web-development/web-apis/)** - RESTful APIs, GraphQL, gRPC services
- **[blazor/](web-development/blazor/)** - Blazor Server and WebAssembly applications

### Desktop Applications  
- **[wpf/](desktop-apps/wpf/)** - Windows Presentation Foundation applications
- **[winui/](desktop-apps/winui/)** - WinUI 3 modern Windows applications
- **[maui/](desktop-apps/maui/)** - .NET Multi-platform App UI projects

### Additional Projects
- **[console-apps/](console-apps/)** - Command-line applications and tools
- **[shared-libraries/](shared-libraries/)** - Reusable class libraries and NuGet packages

## Technology Focus

Projects in this directory demonstrate:
- Modern .NET development practices
- Clean Architecture and SOLID principles
- Entity Framework Core for data access
- Authentication and authorization patterns
- API design and RESTful services
- Cross-platform desktop development
- Testing strategies and TDD practices

## Development Requirements

### Essential
- **.NET 8 SDK** or later
- **Visual Studio 2022** or **VS Code** with C# extension
- **SQL Server Developer** or **SQLite** for database projects

### Optional  
- **Docker Desktop** for containerization
- **Postman** or **Insomnia** for API testing
- **SQL Server Management Studio** for database management

## 📚 Learning Resources

### Official Documentation
- [.NET Documentation](https://docs.microsoft.com/en-us/dotnet/)
- [ASP.NET Core Documentation](https://docs.microsoft.com/en-us/aspnet/core/)
- [Blazor Documentation](https://docs.microsoft.com/en-us/aspnet/core/blazor/)

### Recommended Courses & Tutorials
- Microsoft Learn C# Learning Path
- Pluralsight ASP.NET Core courses
- Clean Code and SOLID principles in C#

## 🚀 Quick Start Templates

```bash
# Create new console application
dotnet new console -n MyConsoleApp

# Create new Web API
dotnet new webapi -n MyWebApi

# Create new Blazor Server app
dotnet new blazorserver -n MyBlazorApp

# Create new WPF application
dotnet new wpf -n MyWpfApp

# Create new MAUI application
dotnet new maui -n MyMauiApp
```

## 📝 Project Naming Convention

Use descriptive, PascalCase names that indicate the project purpose:
- `TaskManagerApi` - Web API for task management
- `InventoryDesktopApp` - WPF inventory management
- `PersonalBudgetBlazor` - Blazor budgeting application
- `FileUtilitiesConsole` - Console file management tools

## ✅ Best Practices Checklist

- [ ] Follow C# coding conventions and naming standards
- [ ] Implement proper error handling and logging
- [ ] Write unit tests for business logic
- [ ] Use dependency injection for loose coupling  
- [ ] Apply SOLID principles
- [ ] Document public APIs and complex logic
- [ ] Use async/await for I/O operations
- [ ] Implement proper security measures (authentication, authorization, input validation)