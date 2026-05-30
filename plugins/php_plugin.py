# plugins/php_plugin.py
"""Installs PHP programming language"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class PhpPlugin(PluginBase):
    name = "php"
    description = "Installs PHP programming language"
    depends_on: List[str] = []
    categories: List[str] = ["language"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "php"]]
        if os_name == "linux":
            if pkg == "apt":
                return [["apt", "-y", "install", "php"]]
            if pkg == "snap":
                return ["snap install php"]
        if os_name == "windows":
            if pkg == "winget":
                return [["winget", "install", "PHP.PHP"]]
            if pkg == "choco":
                return [["choco", "install", "php", "-y"]]
        return []
