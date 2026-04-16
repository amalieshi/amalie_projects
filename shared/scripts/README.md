# Quick Setup Scripts 🛠️

This folder contains automation scripts for setting up development environments and common tasks.

## 📋 Available Scripts

### setup-python-env.ps1
PowerShell script to create Python virtual environments with common data science packages.

### setup-dotnet-project.ps1  
PowerShell script to scaffold new .NET projects with common dependencies.

### install-dev-tools.ps1
Script to install essential development tools and extensions.

### clean-projects.ps1
Script to clean build artifacts and temporary files across all projects.

## 🚀 Usage Examples

```powershell
# Set up Python environment for machine learning
.\setup-python-env.ps1 -EnvName "ml-project" -Packages "pytorch,tensorflow,scikit-learn"

# Create new .NET Web API project  
.\setup-dotnet-project.ps1 -ProjectName "TaskManagerAPI" -Template "webapi"

# Install all development tools
.\install-dev-tools.ps1

# Clean all projects
.\clean-projects.ps1
```