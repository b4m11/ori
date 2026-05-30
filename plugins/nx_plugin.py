# plugins/nx_plugin.py
"""Installs Nx build system"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class NxPlugin(PluginBase):
    name = "nx"
    description = "Installs Nx build system"
    depends_on: List[str] = ["node"]
    categories: List[str] = ["devops", "tool>build"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["npm", "install", "-g", "nx"]]
        if os_name == "linux":
            if pkg == "apt":
                return [["sudo", "npm", "install", "-g", "nx"]]
            if pkg == "snap":
                return [["sudo", "npm", "install", "-g", "nx"]]
        if os_name == "windows":
            if pkg == "winget":
                return [["npm", "install", "-g", "nx"]]
            if pkg == "choco":
                return [["npm", "install", "-g", "nx"]]
        return []
