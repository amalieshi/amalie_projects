"""PyTest fixtures and configuration for WPF Inventory Management App automation testing."""

import pytest
import subprocess
import time
import psutil
import os
from pathlib import Path
from pywinauto import Application, Desktop
from pywinauto.timings import TimeoutError
import logging
from datetime import datetime

from config import (
    APP_EXECUTABLE,
    APP_WINDOW_TITLE,
    APP_WINDOW_TITLE_UIA,
    TEST_SETTINGS,
    PERFORMANCE_SETTINGS,
    CONTROL_IDS,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AppManager:
    """Manages the WPF application lifecycle and PyWinAuto connection."""

    def __init__(self):
        self.process = None
        self.app = None
        self.main_window = None
        self.pid = None

    def start_application(self):
        """Start the WPF application and connect to it."""
        if not APP_EXECUTABLE.exists():
            raise FileNotFoundError(
                f"Application executable not found: {APP_EXECUTABLE}"
            )

        logger.info(f"Starting application: {APP_EXECUTABLE}")

        # Start the application process
        self.process = subprocess.Popen([str(APP_EXECUTABLE)])
        self.pid = self.process.pid

        # Wait for application to start
        time.sleep(2)

        # Connect using PyWinAuto - try both backends
        connection_successful = False

        # Try UIA backend first
        try:
            logger.info("Attempting UIA backend connection...")
            self.app = Application(backend="uia").connect(process=self.pid)
            windows = self.app.windows()

            if windows:
                # Look for the window with Sample Product content first
                target_window = None
                fallback_window = None

                for window in windows:
                    try:
                        title = window.window_text()
                        if title == APP_WINDOW_TITLE_UIA:
                            edit_controls = window.descendants(control_type="Edit")

                            # Look for "Sample Product" to identify the correct window
                            has_sample_product = False
                            try:
                                # Check descendant controls for "Sample Product" text
                                all_controls = window.descendants()
                                for ctrl in all_controls[
                                    :50
                                ]:  # Limit to first 50 to avoid timeout
                                    try:
                                        text_content = ctrl.window_text()
                                        if text_content and (
                                            "sample product" in text_content.lower()
                                            or "sample" in text_content.lower()
                                        ):
                                            has_sample_product = True
                                            break
                                    except:
                                        continue
                            except:
                                pass

                            # Prioritize window with Sample Product
                            if has_sample_product:
                                target_window = window
                                logger.info(
                                    f"Found target window with Sample Product: {title} (Edit controls: {len(edit_controls)})"
                                )
                                break
                            # Keep track of fallback window
                            elif len(edit_controls) >= 4 and fallback_window is None:
                                fallback_window = window
                    except:
                        continue

                # Use target window or fallback
                if target_window:
                    self.main_window = target_window
                    connection_successful = True
                    logger.info(
                        f"UIA connection successful to window with Sample Product"
                    )
                elif fallback_window:
                    self.main_window = fallback_window
                    connection_successful = True
                    logger.info(f"UIA connection successful to fallback window")
        except Exception as e:
            logger.warning(f"UIA backend failed: {e}")

        # Try Win32 backend if UIA failed
        if not connection_successful:
            try:
                logger.info("Attempting Win32 backend connection...")
                self.app = Application(backend="win32").connect(process=self.pid)
                windows = self.app.windows()

                if windows:
                    # Look for main window by title
                    for window in windows:
                        try:
                            title = window.window_text()
                            if title == APP_WINDOW_TITLE or "Inventory" in title:
                                self.main_window = window
                                connection_successful = True
                                logger.info(
                                    f"Win32 connection successful to window: {title}"
                                )
                                break
                        except:
                            continue
            except Exception as e:
                logger.warning(f"Win32 backend failed: {e}")

        if not connection_successful:
            raise TimeoutError("Failed to connect with both UIA and Win32 backends")

    def cleanup(self):
        """Clean up application process and connections."""
        logger.info("Cleaning up application")

        if self.process:
            try:
                # Try graceful shutdown first
                if self.main_window:
                    try:
                        self.main_window.close()
                        time.sleep(1)
                    except:
                        pass

                # Force kill if still running
                if self.process.poll() is None:
                    self.process.terminate()
                    time.sleep(1)

                    if self.process.poll() is None:
                        self.process.kill()

            except Exception as e:
                logger.warning(f"Error during cleanup: {e}")

        self.process = None
        self.app = None
        self.main_window = None
        self.pid = None


class PerformanceMonitor:
    """Monitors application performance using psutil."""

    def __init__(self, pid):
        self.pid = pid
        self.process = psutil.Process(pid)
        self.samples = []
        self.monitoring = False

    def start_monitoring(self):
        """Start performance monitoring."""
        self.monitoring = True
        self.samples = []
        logger.info("Performance monitoring started")

    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.monitoring = False
        logger.info(
            f"Performance monitoring stopped. Collected {len(self.samples)} samples"
        )

    def collect_sample(self):
        """Collect a single performance sample."""
        if not self.monitoring:
            return None

        try:
            sample = {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": self.process.cpu_percent(),
                "memory_mb": self.process.memory_info().rss / 1024 / 1024,
                "memory_percent": self.process.memory_percent(),
                "num_threads": self.process.num_threads(),
                "num_handles": getattr(self.process, "num_handles", lambda: 0)(),
            }
            self.samples.append(sample)
            return sample
        except psutil.NoSuchProcess:
            logger.warning("Process no longer exists")
            return None

    def get_summary_stats(self):
        """Get summary statistics from collected samples."""
        if not self.samples:
            return {}

        cpu_values = [s["cpu_percent"] for s in self.samples]
        memory_values = [s["memory_mb"] for s in self.samples]

        return {
            "sample_count": len(self.samples),
            "cpu_avg": sum(cpu_values) / len(cpu_values),
            "cpu_max": max(cpu_values),
            "memory_avg_mb": sum(memory_values) / len(memory_values),
            "memory_max_mb": max(memory_values),
            "memory_peak_percent": max(s["memory_percent"] for s in self.samples),
            "threads_max": max(s["num_threads"] for s in self.samples),
            "handles_max": max(s["num_handles"] for s in self.samples),
        }


@pytest.fixture(scope="session")
def app_manager():
    """Session-scoped fixture for managing the application lifecycle."""
    manager = AppManager()

    try:
        manager.start_application()
        yield manager
    finally:
        manager.cleanup()


@pytest.fixture(scope="function")
def app_window(app_manager):
    """Function-scoped fixture providing access to the main window."""
    # Reset application state before each test
    logger.info("Preparing application for test")

    # Ensure window is in focus and ready
    if app_manager.main_window:
        try:
            app_manager.main_window.set_focus()
        except:
            pass

    yield app_manager.main_window

    # Cleanup after test if needed
    logger.info("Test completed")


@pytest.fixture(scope="function")
def performance_monitor(app_manager):
    """Function-scoped fixture for performance monitoring."""
    if not app_manager.pid:
        pytest.skip("Application not running")

    monitor = PerformanceMonitor(app_manager.pid)
    monitor.start_monitoring()

    yield monitor

    monitor.stop_monitoring()

    # Log summary stats
    stats = monitor.get_summary_stats()
    if stats:
        logger.info(f"Performance Summary: {stats}")


@pytest.fixture(scope="function")
def screenshot_on_failure(request, app_manager):
    """Take screenshot on test failure."""
    yield

    if request.node.rep_call.failed and TEST_SETTINGS["screenshot_on_failure"]:
        try:
            if app_manager.main_window:
                screenshot_path = (
                    TEST_SETTINGS["screenshot_dir"]
                    / f"failure_{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                app_manager.main_window.capture_as_image().save(screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
