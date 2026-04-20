import os
from django.apps import AppConfig
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


class TestingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "testing"
    verbose_name = "API Testing Orchestrator"

    def ready(self):
        """Called when Django app is ready - auto-start FastAPI server"""
        # Only run auto-start in the main process (not during migrations/collectstatic)
        if os.environ.get("RUN_MAIN") or os.environ.get("RENDER"):
            self._auto_start_fastapi_server()

    def _auto_start_fastapi_server(self):
        """Automatically start the FastAPI server if it's not running"""
        try:
            # Check if migrations are pending to avoid issues during startup
            executor = MigrationExecutor(connection)
            if executor.migration_plan(executor.loader.graph.leaf_nodes()):
                print("[ORCHESTRATOR] Migrations pending, skipping FastAPI auto-start")
                return

            from .utils import FastAPIServerManager

            manager = FastAPIServerManager()

            if not manager.is_server_running():
                print(
                    "[ORCHESTRATOR] FastAPI server not running, starting automatically..."
                )
                result = manager.start_server()

                if result["success"]:
                    print(
                        f"[ORCHESTRATOR] ✅ FastAPI server started successfully on port {manager.port}"
                    )
                else:
                    print(
                        f"[ORCHESTRATOR] ❌ Failed to start FastAPI server: {result['message']}"
                    )
            else:
                print("[ORCHESTRATOR] ✅ FastAPI server already running")

        except Exception as e:
            print(f"[ORCHESTRATOR] ⚠️ Error during FastAPI auto-start: {str(e)}")
