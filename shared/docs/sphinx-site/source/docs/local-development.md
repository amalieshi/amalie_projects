# Local Development Workflow

Learn how to test and develop documentation locally using the modernized build system.

## Quick Start (Multiple Methods)

### Method 1: Built-in Script (Recommended)

```bash
cd shared/docs/sphinx-site
python docs.py serve
```

This will:
- Start a server at `http://127.0.0.1:8000`
- **Automatically rebuild** when you edit files
- **Auto-refresh** browser when changes are detected
- Open your browser automatically

### Method 2: Direct sphinx-autobuild (Alternative Port)

```bash
cd shared/docs/sphinx-site
python -m sphinx_autobuild source build/html --host 127.0.0.1 --port 8001 --open-browser
```

**Use this when:**
- Port 8000 is already in use
- You need a specific port number
- The built-in script has issues

### Method 3: Static Build + HTTP Server

```bash
cd shared/docs/sphinx-site
python docs.py build

# Then serve static files
cd build/html
python -m http.server 8002
# Visit http://127.0.0.1:8002
```

## Development Workflow

### Complete Setup (First Time)

```bash
cd shared/docs/sphinx-site

# Install all development dependencies
python docs.py install --dev

# Clean previous builds
python docs.py clean

# Start live server
python docs.py serve
```

### Quality Checks Before Committing

```bash
# Run all linting and quality checks
python docs.py lint
```

This checks:
- RST syntax validation
- Documentation style (doc8)
- Sphinx warnings in nitpicky mode

## Dependency Installation Options

```bash
cd shared/docs/sphinx-site

# Install basic dependencies
python docs.py install

# OR install development dependencies (recommended)
python docs.py install --dev

# OR install all dependencies
python docs.py install --all
```

## Available Commands

| Command | Description | Port |
|---------|-------------|------|
| `python docs.py serve` | **Live development server** with auto-reload | 8000 |
| `python -m sphinx_autobuild source build/html --port 8001 --open-browser` | **Direct sphinx-autobuild** (alternative port) | 8001 |
| `python docs.py build` | Build HTML documentation once | N/A |
| `python docs.py clean` | Clean build directories | N/A |
| `python docs.py lint` | Run quality checks and linting | N/A |
| `python docs.py install --dev` | Install development dependencies | N/A |
| `python -m http.server 8002` | Static file server (from build/html) | 8002 |

## Server Options & Port Management

### Default Configuration
When you run `python docs.py serve`:
- **URL**: http://127.0.0.1:8000
- **Port**: 8000 (default)
- **Auto-reload**: Watches for file changes
- **Browser**: Opens automatically

### Alternative Ports (Port Conflict Solutions)

If you get **"port already in use"** error, try these alternatives:

```bash
# Port 8001
python -m sphinx_autobuild source build/html --port 8001 --open-browser

# Port 8002
python -m sphinx_autobuild source build/html --port 8002 --open-browser

# Port 8003
python -m sphinx_autobuild source build/html --port 8003 --open-browser
```

### Advanced Server Options

```bash
# Custom host and port
python -m sphinx_autobuild source build/html --host 0.0.0.0 --port 8080

# No auto-browser opening
python -m sphinx_autobuild source build/html --port 8001 --no-initial

# Watch additional directories
python -m sphinx_autobuild source build/html --watch ../../../python --port 8001
```

## Typical Development Loop

1. **Start server**: `python docs.py serve`
2. **Edit files**: Make changes to `.md` or `.rst` files
3. **Auto-reload**: Server rebuilds and refreshes browser automatically
4. **Quality check**: Run `python docs.py lint` before committing
5. **Clean build**: `python docs.py clean && python docs.py build` for production testing

## Pro Tips

- **Leave `serve` running** while editing - it watches all files
- **Check terminal output** for build warnings/errors
- **Run `lint` before pushing** to catch issues early
- **Use `clean` if builds seem cached/stale**

## Benefits of the Modern System

- **No more Makefile dependencies** - Pure Python cross-platform
- **No more RST title underline issues** - Markdown format eliminates them
- **Live reload development** - See changes instantly
- **Integrated quality checks** - Built-in linting and validation
- **pyproject.toml dependency management** - Modern Python practices

## Troubleshooting

### Port Already in Use Error

**Error**: `[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`

**Solutions**:
```bash
# Method 1: Use alternative port
python -m sphinx_autobuild source build/html --port 8001 --open-browser

# Method 2: Kill existing process (Windows)
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Method 3: Use different port entirely
python -m sphinx_autobuild source build/html --port 8005 --open-browser
```

### MyST Parser Issues

**Error**: `Source parser for myst_parser not registered`

**Solutions**:
```bash
# Clean and rebuild
python docs.py clean
python docs.py build

# Reinstall dependencies
pip uninstall -y sphinx myst-parser
pip install -e ".[dev,enhanced]"
```

### Build Issues
```bash
# Clean and rebuild
python docs.py clean
python docs.py build

# Check for errors
python docs.py lint
```

### Dependency Issues
```bash
# Reinstall dependencies
python docs.py install --dev --force
```

### Server Not Auto-reloading
- Check terminal for error messages
- Ensure you're editing files in the `source/` directory
- Try restarting the server (Ctrl+C, then restart with alternative port)
- Clear browser cache (Ctrl+F5)

Your documentation system is now fully modernized and ready for efficient local development!