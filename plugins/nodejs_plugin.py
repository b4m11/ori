# plugins/nodejs_plugin.py
"""Installs Node.js"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class NodejsPlugin(PluginBase):
    name = "node"
    description = "Installs Node.js"
    depends_on: List[str] = []
    categories: List[str] = ["backend>javascript"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "node"]]
        if os_name == "linux":
            if pkg == "apt":
                return [["apt", "-y", "install", "nodejs"]]
            if pkg == "snap":
                return [["snap", "install", "node", "--classic"]]
        if os_name == "windows":
            if pkg == "winget":
                return [["winget", "install", "OpenJS.NodeJS"]]
            if pkg == "choco":
                return [["choco", "install", "nodejs", "-y"]]
        return []
