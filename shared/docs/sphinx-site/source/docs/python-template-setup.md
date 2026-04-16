# Python Package CI/CD Template Setup Guide

## Template File

**File Location:**  [View on GitHub](https://github.com/amalieshi/amalie_projects/blob/main/shared/templates/python-package-template.yml) | [Download Raw](https://raw.githubusercontent.com/amalieshi/amalie_projects/main/shared/templates/python-package-template.yml)

> **Note:** Click the links above to view/download the complete template file directly from the documentation or GitHub.

## Quick Start

1. **Copy the template file:**
   ```bash
   # From the repository root:
   cp shared/templates/python-package-template.yml .github/workflows/your-project-name.yml
   
   # Or download directly from GitHub
   curl -o .github/workflows/your-project-name.yml https://raw.githubusercontent.com/amalieshi/amalie_projects/main/shared/templates/python-package-template.yml
   ```

2. **Customize the variables at the top:**
   ```yaml
   env:
     # Project Configuration
     PROJECT_NAME: "your-project-name"                    # Display name for the project
     PACKAGE_DIR: "path/to/your/package"                  # Path to package directory from repo root
     PYPI_URL: "https://pypi.org/p/your-package-name"     # PyPI project URL
     
     # Git Configuration
     GIT_AUTHOR_NAME: "Your Name"                         # Git commit author name
     GIT_AUTHOR_EMAIL: "your.email@example.com"          # Git commit author email
     
     # Python Configuration
     PRIMARY_PYTHON_VERSION: "3.11"                      # Primary Python version for builds
     TEST_PYTHON_VERSIONS: '["3.8", "3.9", "3.10", "3.11", "3.12"]'  # Python versions to test
     TEST_OPERATING_SYSTEMS: '["ubuntu-latest", "windows-latest", "macos-latest"]'  # OS to test on
     
     # Package Configuration
     INSTALL_EXTRAS: "test"                               # Extra dependencies for testing (e.g., "test", "dev")
     LINT_MAX_LINE_LENGTH: "88"                          # Maximum line length for linting
     LINT_IGNORE: "E203,W503"                            # Flake8 ignore rules
   ```

3. **Update the trigger paths:**
   ```yaml
   on:
     push:
       paths:
         - "path/to/your/package/**"                      # Modify this path pattern
     pull_request:
       paths:
         - "path/to/your/package/**"                      # Modify this path pattern
   ```

## Building the YML File from Scratch

If you want to understand how to build the workflow file instead of using the template, here's the step-by-step approach:

### 1. Basic Structure
```yaml
name: "Your Project - CI/CD Pipeline"

# Define when the workflow runs
on:
  push:
    paths: ["your/package/path/**"]
  pull_request:
    paths: ["your/package/path/**"]
  workflow_dispatch:
    inputs:
      force_publish:
        description: "Force publish even if version exists"
        type: boolean
        default: false

# Configuration variables
env:
  PACKAGE_DIR: "your/package/path"
  PROJECT_NAME: "Your Project"
  # ... other config vars
```

### 2. Job Dependencies Flow
The jobs should follow this dependency chain:
```
check-version (always runs)
    ↓
test (always runs, independent)
    ↓  
build (only if should-publish=true)
    ↓
create-tag + publish-pypi + create-github-release (parallel)
    ↓
notify-success
```

### 3. Essential Jobs Explained

**check-version job:**
- Extracts version from `pyproject.toml`
- Checks if git tag already exists
- Outputs `should-publish=true/false`

**test job:**
- Matrix strategy for multiple Python versions & OS
- Install dependencies with `pip install -e ".[test]"`
- Run `pytest` and optional linting

**build job:**
- Uses `python -m build` to create wheel and tarball
- Validates with `twine check dist/*`
- Uploads artifacts for other jobs

**create-tag job:**
- Creates git tag like `project-name-v1.0.0`
- Pushes tag using `PAT_TOKEN` secret

**publish-pypi job:**
- Downloads build artifacts
- Uses `pypa/gh-action-pypi-publish` action
- Requires `id-token: write` permission for trusted publishing

### 4. Key Patterns

**Matrix Testing:**
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.9", "3.10", "3.11", "3.12"]
    exclude:
      - os: macos-latest
        python-version: "3.9"  # Skip expensive combinations
```

**Conditional Jobs:**
```yaml
job-name:
  if: needs.check-version.outputs.should-publish == 'true'
  needs: [check-version, build]
```

**Environment Variables in Scripts:**
```bash
cd ${{ env.PACKAGE_DIR }}
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
```

### 5. Security & Best Practices

- **Never publish on every push** - use version checking
- **Use trusted publishing** instead of API tokens when possible
- **Validate packages** with `twine check` before publishing
- **Use PAT tokens** for tag creation (needs repo write access)
- **Test on multiple platforms** to catch OS-specific issues

### 6. Common Gotchas

- **Artifact names must be unique** across workflow runs
- **Git tag format matters** - use consistent naming like `project-v1.0.0`
- **Working directory** - always `cd ${{ env.PACKAGE_DIR }}` before package operations
- **JSON arrays in env** - use `fromJson()` function: `${{ fromJson(env.TEST_VERSIONS) }}`
- **Matrix excludes** - reduce job count by skipping expensive combinations

## Required Repository Setup

### 1. Secrets (Repository Settings → Secrets and Variables → Actions)
- `PAT_TOKEN`: Personal Access Token for creating tags
- `PYPI_API_TOKEN`: (Optional, if not using trusted publishing)

### 2. PyPI Trusted Publishing (Recommended)
- Go to PyPI → Your Project → Settings → Publishing
- Add GitHub as trusted publisher
- Repository: `your-username/your-repo`
- Workflow name: `your-workflow-filename.yml`
- Environment: `pypi`

### 3. Package Structure Expected
```
your-package/
├── pyproject.toml          # Must have [project] name and version
├── src/
│   └── your_package/
│       └── __init__.py
└── tests/
    └── test_*.py
```

## Customization Options

### Python Versions
```yaml
TEST_PYTHON_VERSIONS: '["3.9", "3.10", "3.11", "3.12"]'  # Modify as needed
```

### Operating Systems
```yaml
TEST_OPERATING_SYSTEMS: '["ubuntu-latest", "windows-latest"]'  # Remove macos if not needed
```

### Package Installation
```yaml
INSTALL_EXTRAS: "test,dev"  # Add extra dependencies
```

### Linting Configuration
```yaml
LINT_MAX_LINE_LENGTH: "100"    # Adjust line length
LINT_IGNORE: "E203,W503,E501"  # Adjust ignore rules
```

## What This Template Provides

- **Multi-OS Testing**: Ubuntu, Windows, macOS  
- **Multi-Python Testing**: Python 3.8-3.12  
- **Version Management**: Automatic version detection  
- **Smart Publishing**: Only publishes new versions  
- **PyPI Publishing**: With trusted publishing support  
- **GitHub Releases**: Automatic release creation  
- **Git Tagging**: Automatic tag creation  
- **Linting**: Flake8 code quality checks  
- **Branch Support**: Works on any branch, including PRs  

## Usage Examples

### For a FastAPI project:
```yaml
PROJECT_NAME: "FastAPI Todo List"
PACKAGE_DIR: "python/web-frameworks/fastapi"
PYPI_URL: "https://pypi.org/p/todolist-fastapi"
```

### For a data science project:
```yaml
PROJECT_NAME: "ML Data Pipeline"
PACKAGE_DIR: "machine-learning/data-pipeline"
PYPI_URL: "https://pypi.org/p/ml-data-pipeline"
TEST_PYTHON_VERSIONS: '["3.9", "3.10", "3.11"]'  # Skip older versions
INSTALL_EXTRAS: "ml,test"
```

### For a simple utility:
```yaml
PROJECT_NAME: "CLI Utilities"
PACKAGE_DIR: "utils/cli-tools"
TEST_OPERATING_SYSTEMS: '["ubuntu-latest"]'  # Linux only
```

## Troubleshooting

- **Tag creation fails**: Check PAT_TOKEN secret has repo permissions
- **PyPI publish fails**: Verify trusted publishing setup or PYPI_API_TOKEN
- **Tests fail**: Check INSTALL_EXTRAS and package structure
- **Version not detected**: Ensure pyproject.toml has `version = "x.y.z"` format