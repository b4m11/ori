# plugins/java_plugin.py
"""Installs Java OpenJDK"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class JavaPlugin(PluginBase):
    full_name = "Java"
    name = "java"
    description = "Installs Java OpenJDK"
    depends_on: List[str] = []
    categories: List[str] = ["language"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "openjdk"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install openjdk"]
            if pkg == "snap":
                return ["snap install openjdk"]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install -e --id Microsoft.OpenJDK.25"]
            if pkg == "scoop":
                return [
                    "scoop bucket add java",
                    "scoop install java/openjdk"
                ]
            if pkg == "choco":
                return [["choco", "install", "openjdk", "-y"]]
        return []
