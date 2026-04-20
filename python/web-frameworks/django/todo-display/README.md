# Todo Display

## User-Focused Todo Application

A clean, intuitive Django web application designed for end users to create, view, and manage their todos in a user-friendly interface. This application focuses on user experience and simplicity.

🌐 **Live Demo**: [https://todo-list-6ldf.onrender.com/?filter=all&view=cards](https://todo-list-6ldf.onrender.com/?filter=all&view=cards)  
🚀 **Deployed on**: [Render](https://render.com) with automatic HTTPS, scaling, and zero-config deployment

## Purpose

**Target Audience**: End Users, General Public  
**Use Case**: Daily todo management, personal productivity

## Key Features

### User-Friendly Interface
- Clean, modern design optimized for usability
- Responsive layout that works on all devices
- Intuitive navigation with clear visual hierarchy
- Beautiful todo cards with status indicators

### Todo Management
- **Create new todos** with title and optional description
- View all todos in an organized layout
- **Edit existing todos** inline with save/cancel options
- **Delete todos** with confirmation dialogs
- Filter by status (active, completed, all)
- Quick actions for completing/uncompleting todos
- Search functionality to find specific todos
- Clean typography for easy reading

### User Experience
- Fast loading times with optimized queries
- Smooth interactions with minimal page refreshes
- Clear visual feedback for all actions
- Accessibility features for inclusive design
- Mobile-first responsive design

## Design Philosophy

- Simplicity over complexity: Focus on core functionality
- User-centric design: Every feature serves the end user
- Visual clarity: Clean layouts with purposeful whitespace
- Performance first: Fast, responsive interactions
- Accessibility: Usable by everyone

## Getting Started

### Prerequisites
- Python 3.8+
- FastAPI Todo List API server running
- Virtual environment activated

### Installation & Setup
```bash
# Navigate to project
cd todo-display

# Install dependencies from pyproject.toml
pip install -e .

# Run database migrations
python manage.py migrate

# Start the user-facing server
python manage.py runserver 8002
```

## Enhanced Development Features

### Automatic Port Conflict Resolution
The application now includes **intelligent port management** that automatically handles port conflicts for a seamless development experience.

#### Features
- **Automatic Detection**: Detects when ports are already in use
- **Smart Resolution**: Gracefully terminates conflicting processes
- **FastAPI Integration**: Automatically starts and manages FastAPI server
- **Health Monitoring**: Continuous server health checking
- **Manual Control**: Management commands for advanced users

#### How It Works
```bash
# Simply start Django - conflicts are handled automatically
python manage.py runserver 8001

# Output shows automatic resolution:
# Django server will use port 8001
# Port 8001 is in use by 1 process(es). Clearing conflicts...
# Successfully terminated process 12345
# Django port 8001 is ready: Port 8001 is now available after clearing conflicts
# FastAPI server auto-start completed
# Starting development server at http://127.0.0.1:8001/
```

### Port Management Commands

Clear port conflicts manually when needed:

```bash
# Clear specific port
python manage.py clear_ports --port 8001

# Clear FastAPI port (8000)
python manage.py clear_ports --fastapi-port

# Clear all common development ports (8000, 8001, 8002, 8080)
python manage.py clear_ports --all-common-ports

# Preview what would be cleared (dry run)
python manage.py clear_ports --dry-run --all-common-ports
```

#### Command Output Example
```bash
$ python manage.py clear_ports --all-common-ports

--- Checking port 8000 ---
Found 1 process(es) using port 8000:
  PID 21431: Python - uvicorn fastapi_todo_list.main:app...
Successfully killed 1 process(es) on port 8000

--- Checking port 8001 ---
Port 8001 is available

--- Summary ---
Successfully cleared 1 process(es) across 4 port(s)
```

### Concurrent Server Management

#### FastAPI Auto-Start
- **Automatic Detection**: Checks if FastAPI server is running
- **Smart Startup**: Only starts if needed, preserves existing healthy servers
- **Health Monitoring**: Continuous health checks with timeout handling
- **Process Management**: Graceful restarts for conflicting servers

#### Django Port Intelligence
- **Port Extraction**: Automatically detects which port Django will use
- **Conflict Prevention**: Clears conflicting processes before Django starts
- **Smart Exclusions**: Preserves important services (like FastAPI on port 8000)
- **Comprehensive Logging**: Detailed startup information for troubleshooting

### Usage
1. **Start the server** with `python manage.py runserver 8001`
   - **Automatic FastAPI startup** - No need to manually start the API server
   - **Port conflict resolution** - Old processes are automatically cleared  
   - **Health monitoring** - Servers are checked and restarted if needed
2. **Visit the application** at http://localhost:8001 or the live demo at [https://todo-list-6ldf.onrender.com](https://todo-list-6ldf.onrender.com)
3. **Create new todos** using the "Add New Todo" form at the top
4. **Browse your todos** in the clean interface
5. **Edit todos** inline by clicking the edit button
6. **Mark items complete** with simple clicks
7. **Delete todos** with confirmation dialogs
8. **Filter and search** to find what you need
9. **Enjoy a clutter-free** todo management experience

## API Integration

This Django application integrates with the FastAPI Todo API server to provide data. The integration includes:

- **Automatic Server Management**: FastAPI server is started automatically when Django starts
- **Health Monitoring**: Continuous health checks ensure API availability
- **Port Management**: Smart port allocation prevents conflicts
- **Error Handling**: Graceful degradation when API is unavailable

## Deployment

### Render Deployment

The application is fully configured for deployment on Render cloud platform. 🚀 **Live at**: [https://todo-list-6ldf.onrender.com](https://todo-list-6ldf.onrender.com)

#### Quick Deploy to Render

1. **Fork/Clone** this repository to your GitHub account
2. **Connect to Render**:
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
3. **Configure Service**:
   - **Name**: `todo-display` (or your preferred name)
   - **Region**: Choose your preferred region
   - **Branch**: `main` (or your deployment branch)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python manage.py runserver 0.0.0.0:$PORT`
4. **Deploy** and wait for completion (2-3 minutes)

#### Advanced Configuration

**Port Configuration**
- **Django**: Uses the `PORT` environment variable provided by Render
- **FastAPI**: Runs on port 10000 to avoid conflicts with Django
- **Environment Detection**: Automatically detects Render environment via `RENDER` env var
- **Smart Host Binding**: 
  - **External Access**: FastAPI binds to `0.0.0.0` on Render for public access
  - **Internal Communication**: Django communicates with FastAPI via `127.0.0.1` (localhost)
  - **Health Checks**: Uses `127.0.0.1` for reliable health monitoring even with `0.0.0.0` binding

**Dependencies**
All required dependencies are listed in both `pyproject.toml` and `requirements.txt`:
- Django and related packages
- FastAPI and uvicorn for the API server
- Required utilities (requests, psutil, whitenoise)

**Environment Variables** (Optional - Set in Render Dashboard)
```
RENDER=1                    # Automatically set by Render
DEBUG=False                 # Recommended for production
DJANGO_SECRET_KEY=xxx       # Generate secure key for production
ALLOWED_HOSTS=*             # Already configured
```

**Build & Start Commands**
```bash
# Build Command
pip install -r requirements.txt

# Start Command  
python manage.py runserver 0.0.0.0:$PORT
```

#### Production Features

**CSRF Protection**
- Configured for Render's domain structure
- Supports custom domain deployment
- Automatic HTTPS enforcement

**Static File Serving**
- Uses Whitenoise for efficient static file serving
- No additional CDN configuration required
- Optimized for production performance

**Auto-Scaling**
- Render automatically scales based on traffic
- Zero-downtime deployments
- Automatic SSL certificate management

### Local Development vs Production

#### Local Development
- Django runs on specified port (default: 8001)
- FastAPI runs on port 8000
- **Host Binding**: FastAPI uses `127.0.0.1` for local-only access
- **Internal Communication**: Django ↔ FastAPI via `127.0.0.1:8000`
- Includes auto-reload functionality

#### Production (Render)
- Django runs on Render's provided PORT
- FastAPI runs on port 10000
- **Host Binding**: FastAPI uses `0.0.0.0` for external access
- **Internal Communication**: Django ↔ FastAPI via `127.0.0.1:10000` (localhost)
- **Health Checks**: Always use `127.0.0.1` regardless of binding host
- Optimized for production performance

### Troubleshooting Deployment

**Common Render Deployment Issues:**

1. **Server Startup Issues**
   - **Check Dependencies**: Ensure all packages in requirements.txt are installed
   - **Verify Build Command**: Confirm `pip install -r requirements.txt` completes successfully
   - **Check Start Command**: Must use `python manage.py runserver 0.0.0.0:$PORT`

2. **CSRF Verification Failed**
   - Render domains are automatically trusted via `CSRF_TRUSTED_ORIGINS`
   - For custom domains, add them to Django settings
   - Check that requests are made over HTTPS in production

3. **Port Configuration**
   - Django automatically uses Render's `$PORT` environment variable
   - FastAPI runs on port 10000 (configured automatically)
   - No manual port configuration needed

4. **Static Files Not Loading**
   - Whitenoise is configured for static file serving
   - Run `python manage.py collectstatic` if needed
   - Check that `STATIC_URL` and `STATIC_ROOT` are properly configured

5. **FastAPI Connection Issues**
   - Health checks automatically detect Render environment
   - **Important**: API server binds to `0.0.0.0` but Django communicates via `127.0.0.1`
   - This separation allows external access while maintaining reliable internal communication
   - Check logs for FastAPI startup messages

**Deployment Validation Steps:**

```bash
# 1. Test locally first
python manage.py runserver 8001

# 2. Verify dependencies
pip install -r requirements.txt

# 3. Check environment detection
python -c "import os; print('Render detected:', bool(os.getenv('RENDER')))"

# 4. Test production settings
DEBUG=False python manage.py check --deploy
```

**Live Deployment**: Successfully running at [https://todo-list-6ldf.onrender.com](https://todo-list-6ldf.onrender.com) ✅

#### Technical Implementation Notes

**Host Binding Architecture**  
The application uses a dual-host configuration for optimal security and reliability:
- **External Binding**: `0.0.0.0` on Render allows public web access to FastAPI
- **Internal Communication**: `127.0.0.1` (localhost) for Django-FastAPI communication
- **Health Monitoring**: Always uses `127.0.0.1` for reliable server health checks

This architecture prevents external direct access to internal API endpoints while maintaining fast, reliable inter-service communication.

- **Seamless connection** to FastAPI Todo List API
- **Automatic server startup** - FastAPI starts concurrently with Django
- **Real-time data synchronization** 
- **Graceful error handling** for API unavailability
- **Automatic retry logic** for failed requests
- **Intelligent port management** prevents conflicts

## Development Ports

- **Todo Display (Django)**: http://localhost:8001 (user interface)
- **FastAPI API**: http://localhost:8000 (automatically managed data source)  
- **Automatic Management**: Both servers start together with zero configuration

## vs Todo Orchestrator

| Feature | Todo Display | Todo Orchestrator |
|---------|-------------|------------------|
| **Target Users** | End Users | Developers/Testers |
| **Purpose** | Daily todo management | API testing & debugging |
| **Interface** | Clean, simple | Technical, detailed |
| **Features** | Core functionality + Auto-management | Advanced testing tools |
| **Server Management** | Fully automatic | Manual setup required |
| **Port Handling** | Intelligent conflict resolution | Basic port usage |
| **Complexity** | Zero-config startup | Comprehensive setup |

## Troubleshooting

### Port Conflicts
If you encounter port conflicts, the system automatically resolves them. For manual control:

```bash
# Check what's using ports
python manage.py clear_ports --dry-run --all-common-ports

# Clear specific conflicts
python manage.py clear_ports --port 8001

# Force clear all development ports
python manage.py clear_ports --all-common-ports
```

### FastAPI Connection Issues
The system automatically manages FastAPI servers, but if you encounter issues:

```bash
# Check FastAPI server status
python manage.py clear_ports --fastapi-port --dry-run

# Restart FastAPI server (automatic on next Django start)
python manage.py clear_ports --fastapi-port
python manage.py runserver 8001
```

### Common Scenarios
- **"Port already in use"**: The system will automatically handle this
- **FastAPI not responding**: Health checks will restart the server
- **Multiple Django instances**: Conflicts are resolved automatically
- **Stale processes**: Use `clear_ports` command to clean up

### Logs & Debugging
The application provides detailed logging during startup:
- Port detection and resolution steps
- FastAPI health check results  
- Process termination confirmations
- Server startup success/failure messages

---

**Perfect for**: Personal productivity, team todo sharing, **zero-config development**  
**Not suitable for**: API testing, development debugging, server management