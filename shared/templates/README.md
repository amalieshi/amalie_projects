# Project Templates

This folder contains starter templates for common project types across different technology stacks.

## Available Templates

### C# Project Templates
- **console-app-template/** - Basic console application structure
- **webapi-template/** - ASP.NET Core Web API with authentication
- **blazor-template/** - Blazor Server application template
- **wpf-template/** - WPF desktop application template

### Python Project Templates  
- **django-api-template/** - Django REST API project structure
- **fastapi-template/** - FastAPI project with async operations
- **ml-project-template/** - Machine learning project structure
- **data-analysis-template/** - Data science project template

### Frontend Templates
- **react-app-template/** - React TypeScript application
- **vue-app-template/** - Vue 3 composition API application
- **vanilla-js-template/** - Modern vanilla JavaScript project

### Full-Stack Templates
- **dotnet-react-template/** - .NET API + React frontend
- **python-vue-template/** - FastAPI + Vue.js full-stack
- **maui-blazor-template/** - .NET MAUI with Blazor hybrid

## Usage Instructions

### Option 1: Copy Template Folder
```bash
# Copy template to your project location
cp -r shared/templates/webapi-template csharp/web-development/aspnet-core/MyNewAPI
cd csharp/web-development/aspnet-core/MyNewAPI
# Follow template README for setup
```

### Option 2: Use dotnet templates (for .NET projects)
```bash
# Install custom template
dotnet new --install shared/templates/webapi-template

# Create new project from template
dotnet new mywebapi -n MyProjectName
```

## 📝 Template Structure Example

Each template folder contains:
```
template-name/
├── README.md              # Setup and usage instructions
├── .gitignore             # Template-specific gitignore
├── project-files/         # Source code and configuration
├── docs/                  # Template documentation
└── scripts/               # Setup and build scripts
```

## ✨ Customization Guidelines

1. **Replace placeholders**: Look for `{{PROJECT_NAME}}`, `{{AUTHOR}}`, etc.
2. **Update namespaces**: Change default namespaces to match your project
3. **Configure dependencies**: Update package references as needed
4. **Customize README**: Update project-specific documentation
5. **Set up CI/CD**: Configure build and deployment pipelines

## 🤝 Contributing Templates

To add a new template:
1. Create a new folder with descriptive name
2. Include comprehensive README.md
3. Add example code and configuration
4. Test the template by creating a new project
5. Document any special setup requirements