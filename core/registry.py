# core/registry.py
"""Plugin registry – discovers and registers all PluginBase subclasses.
It scans the ``plugins`` package (and optional external plugin directories) and
builds a dependency‑ordered list of plugin instances.
"""
import importlib
import pkgutil
import sys
from pathlib import Path
from typing import List, Dict

from .plugin_base import PluginBase

def _load_modules_from_package(package_name: str) -> List[object]:
    """Import all modules in a package and return the module objects."""
    package = importlib.import_module(package_name)
    modules = []
    for _, mod_name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        if is_pkg:
            continue
        modules.append(importlib.import_module(mod_name))
    return modules

def _collect_plugins(modules: List[object]) -> List[PluginBase]:
    plugins = []
    for mod in modules:
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if isinstance(attr, type) and issubclass(attr, PluginBase) and attr is not PluginBase:
                plugins.append(attr())
    return plugins

def _topological_sort(plugins: List[PluginBase]) -> List[PluginBase]:
    """Return plugins ordered respecting ``depends_on``.
    Simple Kahn algorithm – raises RuntimeError on cycles.
    """
    name_to_plugin: Dict[str, PluginBase] = {p.name: p for p in plugins}
    indegree: Dict[str, int] = {p.name: 0 for p in plugins}
    graph: Dict[str, List[str]] = {p.name: [] for p in plugins}
    for p in plugins:
        for dep in p.depends_on:
            if dep not in name_to_plugin:
                raise RuntimeError(f"Plugin {p.name} depends on unknown plugin {dep}")
            graph[dep].append(p.name)
            indegree[p.name] += 1
    queue = [name for name, deg in indegree.items() if deg == 0]
    ordered = []
    while queue:
        n = queue.pop(0)
        ordered.append(name_to_plugin[n])
        for m in graph[n]:
            indegree[m] -= 1
            if indegree[m] == 0:
                queue.append(m)
    if len(ordered) != len(plugins):
        raise RuntimeError("Circular dependency detected among plugins")
    return ordered

def load_all_plugins(extra_plugin_dirs: List[Path] = None) -> List[PluginBase]:
    """Discover built‑in plugins and any external plugin directories.
    Returns a dependency‑ordered list of plugin instances.
    """
    extra_plugin_dirs = extra_plugin_dirs or []
    modules = _load_modules_from_package("plugins")
    for d in extra_plugin_dirs:
        sys.path.insert(0, str(d))
        for py_file in d.glob("*.py"):
            module_name = py_file.stem
            try:
                mod = importlib.import_module(module_name)
                modules.append(mod)
            except Exception as e:
                print(f"[WARN] Failed to import external plugin {py_file}: {e}", file=sys.stderr)
        sys.path.pop(0)
    plugins = _collect_plugins(modules)
    return _topological_sort(plugins)
