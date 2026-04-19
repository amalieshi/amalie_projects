import os
import sys
import subprocess
import psutil
import requests
import time
import logging
import signal
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)


class FastAPIServerManager:
    """Manager class for auto-starting the FastAPI server with port conflict resolution"""
    
    def __init__(self):
        self.server_url = settings.FASTAPI_SERVER_URL
        self.port = 8000
        self.fastapi_path = self._get_fastapi_path()
        
    def _get_fastapi_path(self):
        """Get the absolute path to the FastAPI project"""
        # Path: server_manager.py -> display -> todo-display -> django -> web-frameworks -> fastapi -> todo-api
        todo_display_dir = Path(__file__).parent.parent  # todo-display folder
        django_dir = todo_display_dir.parent  # django folder
        web_frameworks_dir = django_dir.parent  # web-frameworks folder
        fastapi_dir = web_frameworks_dir / "fastapi" / "todo-api"  # fastapi/todo-api folder
        return fastapi_dir
    
    def get_processes_using_port(self, port):
        """Get all processes using a specific port"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': proc.info['cmdline']
                        })
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return processes
    
    def kill_processes_on_port(self, port, exclude_pids=None):
        """Kill all processes using a specific port (except excluded PIDs)"""
        exclude_pids = exclude_pids or []
        killed_processes = []
        
        processes = self.get_processes_using_port(port)
        for proc_info in processes:
            pid = proc_info['pid']
            if pid in exclude_pids:
                logger.info(f"Skipping PID {pid} (excluded from kill list)")
                continue
                
            try:
                proc = psutil.Process(pid)
                proc_name = proc.name()
                logger.info(f"Killing process {pid} ({proc_name}) using port {port}")
                
                # Try graceful shutdown first
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    killed_processes.append(proc_info)
                    logger.info(f"Successfully terminated process {pid}")
                except psutil.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    logger.warning(f"Process {pid} didn't terminate gracefully, force killing...")
                    proc.kill()
                    proc.wait(timeout=5)
                    killed_processes.append(proc_info)
                    logger.info(f"Force killed process {pid}")
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                logger.warning(f"Could not kill process {pid}: {e}")
                
        return killed_processes
    
    def is_port_available(self, port):
        """Check if a port is available (not in use)"""
        processes = self.get_processes_using_port(port)
        return len(processes) == 0
        
    def is_server_running(self):
        """Check if the FastAPI server is responding"""
        try:
            response = requests.get(f"{self.server_url}/", timeout=3)
            logger.info(f"Server health check response: {response.status_code}")
            return response.status_code == 200
        except requests.exceptions.Timeout:
            logger.info("Server health check timeout - server may be starting or busy")
            # Timeout could indicate server is running but busy, so do a process check
            return self.get_server_pid() is not None
        except requests.exceptions.ConnectionError:
            logger.info("Server health check connection error - server is not running")
            return False
        except requests.RequestException as e:
            logger.info(f"Server health check failed: {str(e)}")
            return False
            
    def get_server_pid(self):
        """Get the PID of the running FastAPI server if it exists"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and any('uvicorn' in arg or 'fastapi_todo_list' in arg for arg in cmdline):
                    if any(str(self.port) in arg for arg in cmdline):
                        return proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return None
    
    def restart_server_on_port_conflict(self):
        """Handle port conflicts by restarting existing servers"""
        if not self.is_port_available(self.port):
            logger.warning(f"Port {self.port} is in use. Checking if it's our FastAPI server...")
            
            # Check if the process on this port is our FastAPI server
            current_pid = self.get_server_pid()
            if current_pid:
                logger.info(f"Found existing FastAPI server (PID: {current_pid}). Restarting it...")
                killed = self.kill_processes_on_port(self.port)
                if killed:
                    logger.info(f"Killed {len(killed)} processes on port {self.port}")
                    time.sleep(2)  # Wait for port to be released
                else:
                    logger.warning("No processes were killed, but port might still be in use")
            else:
                logger.warning(f"Port {self.port} is used by non-FastAPI process. Clearing it...")
                killed = self.kill_processes_on_port(self.port)
                if killed:
                    logger.info(f"Killed {len(killed)} non-FastAPI processes on port {self.port}")
                    time.sleep(2)  # Wait for port to be released
                
        return self.is_port_available(self.port)
        
    def start_server_if_needed(self):
        """Start the FastAPI server if it's not already running, handling port conflicts"""
        # First, check if server is already running and healthy
        if self.is_server_running():
            logger.info("FastAPI server is already running and healthy")
            return {"success": True, "message": "Server is already running"}
        
        # Handle port conflicts by restarting if needed
        if not self.restart_server_on_port_conflict():
            logger.error(f"Unable to free port {self.port} for FastAPI server")
            return {"success": False, "message": f"Port {self.port} is in use and could not be freed"}
            
        logger.info(f"Starting FastAPI server from path: {self.fastapi_path}")
        if not self.fastapi_path.exists():
            logger.error(f"FastAPI project path does not exist: {self.fastapi_path}")
            return {"success": False, "message": f"FastAPI project path does not exist: {self.fastapi_path}"}
            
        try:
            # Change to FastAPI directory and start the server
            cmd = [
                sys.executable, "-m", "uvicorn", 
                "src.fastapi_todo_list.main:app",
                "--host", "127.0.0.1",
                "--port", str(self.port),
                "--reload"
            ]
            
            logger.info(f"Running command: {' '.join(cmd)}")
            logger.info(f"Working directory: {self.fastapi_path}")
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.fastapi_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for server to start
            logger.info("Waiting for FastAPI server to start...")
            time.sleep(5)
            
            # Check if server is responding
            if self.is_server_running():
                logger.info(f"FastAPI server started successfully on port {self.port}")
                return {"success": True, "message": f"Server started successfully on port {self.port}", "pid": process.pid}
            else:
                stdout, stderr = process.communicate(timeout=1)
                logger.error(f"FastAPI server failed to start. stdout: {stdout.decode()}, stderr: {stderr.decode()}")
                return {"success": False, "message": "Server failed to start or is not responding"}
                
        except Exception as e:
            logger.error(f"Error starting FastAPI server: {str(e)}")
            return {"success": False, "message": f"Error starting server: {str(e)}"}


class DjangoPortManager:
    """Manager class for handling Django server port conflicts"""
    
    def __init__(self, port=8001):
        self.port = port
        
    def get_processes_using_port(self, port):
        """Get all processes using a specific port"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                        processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'cmdline': proc.info['cmdline']
                        })
                        break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return processes
    
    def is_django_server(self, proc_info):
        """Check if a process is a Django development server"""
        cmdline = proc_info.get('cmdline', [])
        if not cmdline:
            return False
        return any('manage.py' in arg and 'runserver' in ' '.join(cmdline) for arg in cmdline)
    
    def kill_conflicting_processes(self, exclude_current_process=True):
        """Kill processes using the Django port, optionally excluding current process"""
        current_pid = os.getpid()
        killed_processes = []
        
        processes = self.get_processes_using_port(self.port)
        for proc_info in processes:
            pid = proc_info['pid']
            
            # Skip current process if requested
            if exclude_current_process and pid == current_pid:
                logger.info(f"Skipping current process PID {pid}")
                continue
                
            try:
                proc = psutil.Process(pid)
                proc_name = proc.name()
                cmdline = ' '.join(proc_info.get('cmdline', []))
                
                logger.info(f"Found process using port {self.port}: PID {pid} ({proc_name})")
                logger.info(f"Command: {cmdline}")
                
                # Kill the process
                logger.info(f"Killing process {pid} using port {self.port}")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    killed_processes.append(proc_info)
                    logger.info(f"Successfully terminated process {pid}")
                except psutil.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    logger.warning(f"Process {pid} didn't terminate gracefully, force killing...")
                    proc.kill()
                    proc.wait(timeout=5)
                    killed_processes.append(proc_info)
                    logger.info(f"Force killed process {pid}")
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                logger.warning(f"Could not kill process {pid}: {e}")
        
        return killed_processes
    
    def ensure_port_available(self):
        """Ensure the Django port is available by killing conflicting processes"""
        processes = self.get_processes_using_port(self.port)
        
        if not processes:
            logger.info(f"Port {self.port} is available for Django server")
            return {"success": True, "message": f"Port {self.port} is available"}
        
        logger.warning(f"Port {self.port} is in use by {len(processes)} process(es). Clearing conflicts...")
        
        killed = self.kill_conflicting_processes()
        if killed:
            logger.info(f"Successfully killed {len(killed)} conflicting processes on port {self.port}")
            time.sleep(2)  # Wait for port to be released
            
            # Verify port is now available
            remaining = self.get_processes_using_port(self.port)
            if not remaining:
                return {"success": True, "message": f"Port {self.port} is now available after clearing conflicts"}
            else:
                logger.warning(f"Port {self.port} still has {len(remaining)} processes after cleanup")
                return {"success": False, "message": f"Could not fully clear port {self.port}"}
        else:
            logger.error(f"Could not kill processes using port {self.port}")
            return {"success": False, "message": f"Port {self.port} conflicts could not be resolved"}


def handle_django_port_conflicts(port=8001):
    """
    Utility function to handle Django port conflicts before starting the server
    Call this from Django's startup process (like apps.py ready() method)
    """
    port_manager = DjangoPortManager(port)
    result = port_manager.ensure_port_available()
    
    if result["success"]:
        logger.info(f"Django port {port} is ready for use")
    else:
        logger.error(f"Django port {port} conflict resolution failed: {result['message']}")
        
    return result