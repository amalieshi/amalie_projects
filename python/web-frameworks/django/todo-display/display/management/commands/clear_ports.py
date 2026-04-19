"""
Django management command to clear port conflicts for development servers.
Usage: python manage.py clear_ports [--port PORT] [--all-common-ports]
"""

from django.core.management.base import BaseCommand, CommandError
from django.utils.termcolors import make_style
from display.server_manager import DjangoPortManager, FastAPIServerManager


class Command(BaseCommand):
    help = 'Clear port conflicts for Django and FastAPI development servers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            type=int,
            help='Specific port to clear (default: 8001 for Django)',
        )
        parser.add_argument(
            '--all-common-ports',
            action='store_true',
            help='Clear conflicts on all common development ports (8000, 8001, 8002, 8080)',
        )
        parser.add_argument(
            '--fastapi-port',
            action='store_true',
            help='Clear conflicts on FastAPI port (8000)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what processes would be killed without actually killing them',
        )

    def handle(self, *args, **options):
        success_style = make_style(opts=('bold',), fg='green')
        warning_style = make_style(opts=('bold',), fg='yellow')
        error_style = make_style(opts=('bold',), fg='red')
        
        ports_to_clear = []
        
        # Determine which ports to clear
        if options['all_common_ports']:
            ports_to_clear = [8000, 8001, 8002, 8080]
            self.stdout.write("Clearing conflicts on all common development ports...")
        elif options['fastapi_port']:
            ports_to_clear = [8000]
            self.stdout.write("Clearing conflicts on FastAPI port (8000)...")
        elif options['port']:
            ports_to_clear = [options['port']]
            self.stdout.write(f"Clearing conflicts on port {options['port']}...")
        else:
            # Default: clear Django port (8001)
            ports_to_clear = [8001]
            self.stdout.write("Clearing conflicts on default Django port (8001)...")

        total_killed = 0
        
        for port in ports_to_clear:
            self.stdout.write(f"\n--- Checking port {port} ---")
            
            if port == 8000:
                # Use FastAPI manager for port 8000
                manager = FastAPIServerManager()
                processes = manager.get_processes_using_port(port)
            else:
                # Use Django manager for other ports  
                manager = DjangoPortManager(port)
                processes = manager.get_processes_using_port(port)
            
            if not processes:
                self.stdout.write(success_style(f"✓ Port {port} is available"))
                continue
                
            self.stdout.write(warning_style(f"Found {len(processes)} process(es) using port {port}:"))
            
            for proc_info in processes:
                pid = proc_info['pid']
                name = proc_info['name']
                cmdline = ' '.join(proc_info.get('cmdline', [])[:3])  # Show first 3 parts
                self.stdout.write(f"  PID {pid}: {name} - {cmdline}...")
                
            if options['dry_run']:
                self.stdout.write(warning_style(f"[DRY RUN] Would kill {len(processes)} process(es) on port {port}"))
                continue
                
            # Kill the processes
            try:
                if port == 8000:
                    killed = manager.kill_processes_on_port(port)
                else:
                    killed = manager.kill_conflicting_processes(exclude_current_process=True)
                    
                if killed:
                    total_killed += len(killed)
                    self.stdout.write(success_style(f"✓ Successfully killed {len(killed)} process(es) on port {port}"))
                else:
                    self.stdout.write(warning_style(f"No processes were killed on port {port}"))
                    
            except Exception as e:
                self.stdout.write(error_style(f"✗ Error clearing port {port}: {str(e)}"))

        # Summary
        self.stdout.write(f"\n--- Summary ---")
        if options['dry_run']:
            self.stdout.write("Dry run completed. No processes were actually killed.")
        elif total_killed > 0:
            self.stdout.write(success_style(f"✓ Successfully cleared {total_killed} process(es) across {len(ports_to_clear)} port(s)"))
            self.stdout.write("You can now start your Django server without port conflicts.")
        else:
            self.stdout.write("No processes needed to be killed. All specified ports were available.")
        
        # Helpful usage examples
        self.stdout.write(f"\n--- Usage Examples ---")
        self.stdout.write("Clear specific port:     python manage.py clear_ports --port 8001")
        self.stdout.write("Clear FastAPI port:      python manage.py clear_ports --fastapi-port")
        self.stdout.write("Clear all common ports:  python manage.py clear_ports --all-common-ports")
        self.stdout.write("Dry run (preview):       python manage.py clear_ports --dry-run")