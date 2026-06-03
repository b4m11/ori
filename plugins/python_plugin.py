# plugins/python_plugin.py
"""Python plugin – ensures Python 3 is installed and optionally pip packages."""

from __future__ import annotations

from typing import List

from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class PythonPlugin(PluginBase):
    full_name = "Python"
    name = "python3"
    description = "Installs Python 3 interpreter"
    depends_on: List[str] = []
    categories: List[str] = ["language"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        if os_name == "mac":
            return [["brew", "install", "python3"]]
        if os_name == "linux":
            if pkg == "brew":
                return [["brew", "install", "python3"]]
            if pkg == "apt":
                return [["sudo", "apt", "-y", "install", "python3"]]
        if os_name == "windows":
            if pkg == "winget":
                return [["winget", "install", "python3"]]
            if pkg == "choco":
                return [["choco", "install", "python3", "--pre"]]
        return []
