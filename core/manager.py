# core/manager.py
"""SetupManager – orchestrates configuration loading, plugin discovery, and execution.
Ensures safe subprocess handling via core.runner and respects dry‑run mode.
"""

from __future__ import annotations
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Any
from .platform_detect import get_platform_info
from .config import load_config, DEFAULT_CONFIG
from .registry import load_all_plugins
from .runner import set_dry_run, run_cmd, stop_event


class DualWriter:
    """Writes to both a file and the original stdout (QueueWriter)."""
    def __init__(self, file_obj, original_stdout):
        self.file = file_obj
        self.original = original_stdout
    def write(self, s: str):
        # Write to file
        self.file.write(s)
        # Forward to original stdout (which puts into the SSE queue)
        self.original.write(s)
    def flush(self):
        self.file.flush()
        self.original.flush()

class SetupManager:
    """Main orchestrator for the dev‑setup tool.

    Parameters
    ----------
    config: dict
        User configuration dictionary. Expected keys:
        - ``plugins``: List of plugin names to enable (optional, defaults to all built‑in).
        - ``extra_plugin_dirs``: List of directories containing external plugins.
        - ``dry_run``: bool flag to enable dry‑run mode.
    """

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or DEFAULT_CONFIG
        self.dry_run: bool = bool(self.config.get("dry_run", False))
        set_dry_run(self.dry_run)
        # Resolve extra plugin directories (list of Path objects)
        extra_dirs = [Path(p) for p in self.config.get("extra_plugin_dirs", [])]
        # Load all plugins (built‑in + external) respecting dependencies
        self.all_plugins: List[Any] = load_all_plugins(extra_dirs)
        # Determine which plugins to run based on configuration
        selected = set(self.config.get("plugins", []))
        if selected:
            # Filter to only plugins whose name is in the selection list
            self.plugins = [p for p in self.all_plugins if p.name in selected]
        else:
            # No explicit selection – run all discovered plugins
            self.plugins = self.all_plugins
        # Initialize output directory for per‑plugin logs
        self.output_dir = Path(self.config.get("output_dir", "plugin_outputs"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def stop_installation(self):
        """Set the stop event to abort the installation process."""
        stop_event.set()

    def _run_plugin(self, plugin) -> bool:
        """Execute a single plugin and capture its output to a log file.

        Returns ``True`` if all commands succeed, ``False`` otherwise.
        """
        # Prepare per‑plugin log file
        log_path = self.output_dir / f"{plugin.name}.log"
        with open(log_path, "w", encoding="utf-8") as log_file:
            # Preserve original stdout/stderr (QueueWriter) and redirect
            original_stdout, original_stderr = sys.stdout, sys.stderr
            sys.stdout = sys.stderr = DualWriter(log_file, original_stdout)
            try:
                try:
                    plugin.pre_install()
                except Exception as exc:
                    print(f"[WARN] pre_install of {plugin.name} failed: {exc}", file=sys.stderr)
                success = True
                for cmd in getattr(plugin, "commands", []) + getattr(plugin, "install_commands", []):
                    try:
                        if shutil.which(plugin.name):
                            print(f"[INFO] Skipping {plugin.name} – already installed/present.")
                            continue
                        run_cmd(cmd, capture_output=True, check=True)
                    except Exception as exc:
                        print(f"[ERROR] Command for plugin {plugin.name} failed: {exc}", file=sys.stderr)
                        print(f"[error] {exc.stdout}")
                        print(f"[error] {exc.stderr}")
                        success = False
                        break  # abort remaining commands for this plugin
                try:
                    plugin.post_install()
                except Exception as exc:
                    print(f"[WARN] post_install of {plugin.name} failed: {exc}", file=sys.stderr)
            finally:
                # Restore original stdout/stderr
                sys.stdout, sys.stderr = original_stdout, original_stderr
            
            return success
        stop_event.clear()

    def run(self) -> None:
        """Run all selected plugins respecting package‑manager dependencies.

        Flow:
        1. Detect platform and ensure primary package manager is installed.
        2. Scan selected plugins for required executables (first token of each command).
        3. For any missing executable, prepend its installer plugin if available.
        4. Record executables without installer plugins in a "could not process" list.
        5. Execute plugins in order, tracking successful vs failed installations.
        """
        info = get_platform_info()
        os_name = info["os"]
        pkg_mgr = info["pkg_manager"]

        # Step 2 – gather required executables from selected plugins
        required_exes = set()

        # Resolve plugin dependencies recursively and build ordered list without duplicates
        ordered_plugins: List[Any] = []
        visited: set = set()

        def add_plugin(p):
            if p.name in visited:
                return
            # Process only the first declared dependency, if any
            dep_names = getattr(p, "depends_on", [])
            if dep_names:
                dep_name = dep_names[0]
                dep_plugin = next((pl for pl in self.all_plugins if getattr(pl, "name", None) == dep_name), None)
                if dep_plugin:
                    add_plugin(dep_plugin)
                else:
                    print(f"[WARN] Dependency '{dep_name}' for plugin '{p.name}' not found.")
            visited.add(p.name)
            ordered_plugins.append(p)

        # Build ordered list based on selected plugins
        for plugin in self.plugins:
            add_plugin(plugin)

        # Run plugins in resolved order
        completed: List[str] = []
        failed: List[str] = []
        for plugin in ordered_plugins:
            if stop_event.is_set():
                print("\n[INFO] Installation aborted by user.")
                break
                
            print(f"[INFO] Installing package: {plugin.name}")
            ok = self._run_plugin(plugin)
            if ok:
                completed.append(plugin.name)
            else:
                failed.append(plugin.name)
        
        # Summary output
        print("\n=== Installation Summary ===")
        print(f"Completed installs ({len(completed)}): {', '.join(completed) if completed else 'none'}")
        print(f"Failed installs ({len(failed)}): {', '.join(failed) if failed else 'none'}")
        # if could_not_process:
        #     print(f"Could not process due to missing installer plugins ({len(could_not_process)}): {', '.join(could_not_process)}")
