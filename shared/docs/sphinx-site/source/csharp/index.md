# C# Development

## 🔷 **C# Technology Stack**

My C# development journey focuses on building robust, scalable applications using modern .NET technologies and best practices.

### **Web Development**
- ASP.NET Core Web APIs
- Blazor Server & WebAssembly
- Entity Framework Core
- JWT Authentication & Authorization

### **Desktop Applications**
- WPF with MVVM pattern
- WinUI 3 modern apps
- .NET MAUI cross-platform
- Local database integration

### **Architecture & Patterns**
- Clean Architecture
- CQRS with MediatR
- Domain-Driven Design
- Dependency Injection

### **Testing & Quality**
- Unit Testing with xUnit
- Integration Testing
- Test-Driven Development
- Code Coverage & Analysis

## 🚀 **Featured C# Projects**

### **Task Management API**

```{tip}
**Project Highlights**

A production-ready REST API showcasing clean architecture, comprehensive testing, and modern development practices.
```

**Key Features:**
- JWT-based authentication and role-based authorization
- Entity Framework Core with code-first migrations
- Comprehensive unit and integration test suite
- API documentation with Swagger/OpenAPI
- Docker containerization and CI/CD pipeline

**Technical Implementation:**
- **Architecture**: Clean Architecture with separate layers for API, Application, Domain, and Infrastructure
- **Database**: SQL Server with Entity Framework Core
- **Authentication**: JWT tokens with refresh token support
- **Validation**: FluentValidation for request validation
- **Logging**: Serilog for structured logging
- **Testing**: xUnit with Moq for mocking dependencies

**Repository Structure:**
```
TaskManagerAPI/
├── src/
│   ├── TaskManager.Api/           # Web API layer
│   ├── TaskManager.Application/   # Business logic
│   ├── TaskManager.Domain/        # Domain entities
│   └── TaskManager.Infrastructure/ # Data access
├── tests/
│   ├── TaskManager.UnitTests/
│   └── TaskManager.IntegrationTests/
└── docs/
```

### **Inventory Desktop Application**

A modern WPF application demonstrating desktop development best practices with the MVVM pattern.

**Key Features:**
- Real-time inventory tracking with SQLite database
- Modern UI with Material Design principles
- Data binding and command patterns
- Export functionality to Excel and PDF
- Backup and restore capabilities

### **Personal Budget Tracker (Blazor)**

An interactive web application built with Blazor Server, showcasing real-time updates and modern web development.

**Key Features:**
- Real-time budget tracking with SignalR
- Interactive charts and visualizations
- Category-based expense tracking
- Monthly and yearly reporting
- Responsive design for mobile devices

## 📚 **Learning Progress**

| Skill Area | Beginner | Intermediate | Advanced |
|------------|----------|--------------|----------|
| **C# Language Features** | ✅ Complete | ✅ Complete | 🚧 Learning |
| **ASP.NET Core** | ✅ Complete | ✅ Complete | 🚧 Learning |
| **Entity Framework** | ✅ Complete | ✅ Complete | 📋 Planned |
| **Desktop Development** | ✅ Complete | 🚧 Learning | 📋 Planned |
| **Testing Practices** | ✅ Complete | 🚧 Learning | 📋 Planned |
| **Microservices** | 📋 Planned | 📋 Planned | 📋 Planned |

## 🛠️ **Development Environment**

**IDE & Tools:**
- Visual Studio 2022 Community Edition
- VS Code with C# extensions
- SQL Server Management Studio
- Postman for API testing

**Package Managers & Tools:**
- NuGet for package management
- .NET CLI for project scaffolding
- Entity Framework CLI tools
- Docker Desktop for containerization

**Key NuGet Packages:**
```
# Web API Development
Microsoft.AspNetCore.Authentication.JwtBearer
Microsoft.EntityFrameworkCore.SqlServer
AutoMapper.Extensions.Microsoft.DependencyInjection
FluentValidation.AspNetCore
Serilog.AspNetCore

# Testing
Microsoft.AspNetCore.Mvc.Testing
xunit
Moq
FluentAssertions

# Desktop Development
Microsoft.WindowsAppSDK
CommunityToolkit.Mvvm
MaterialDesignThemes
```

## 🎯 **Current Learning Focus**

### Clean Architecture

**Objective**: Master the implementation of clean architecture principles in .NET applications.

**Topics:**
- Dependency inversion and IoC containers
- Application and domain layer separation
- CQRS pattern with MediatR
- Domain events and handlers

### Advanced Testing

**Objective**: Implement comprehensive testing strategies for complex applications.

**Topics:**
- Integration testing with TestContainers
- Behavior-driven development (BDD)
- Performance testing and profiling
- Test automation and CI/CD integration

### Microservices

**Objective**: Design and implement microservices architectures.

**Topics:**
- Service-to-service communication
- API gateways and service mesh
- Distributed data management
- Container orchestration with Kubernetes

## 📈 **Next Steps**

**Immediate Goals (Next 3 Months):**
1. Complete advanced testing implementation in current projects
2. Build a microservices demo application
3. Implement event-driven architecture patterns
4. Explore cloud deployment with Azure

**Long-term Objectives (6+ Months):**
1. Contribute to open-source .NET projects
2. Build a production-ready SaaS application
3. Implement advanced security patterns
4. Master performance optimization techniques

---

**Want to explore the code?** Check out my C# projects in the [csharp/](https://github.com/yourusername/amalie_projects/tree/main/csharp) folder of my repository.