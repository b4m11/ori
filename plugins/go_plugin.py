# plugins/go_plugin.py
"""Installs Go programming language"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class GoPlugin(PluginBase):
    name = "go"
    description = "Installs Go programming language"
    depends_on: List[str] = []
    categories: List[str] = ["language"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "go"]]
        if os_name == "linux":
            if pkg == "brew":
                return [["brew", "install", "go"]]
            if pkg == "snap":
                return [["sudo", "snap", "install", "go", "--classic"]]
        if os_name == "windows":
            if pkg == "winget":
                return [["winget", "install", "GoLang.Go"]]
            if pkg == "choco":
                return [["choco", "install", "golang", "-y"]]
        return []
