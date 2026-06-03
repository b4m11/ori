# plugins/postman_plugin.py
"""Installs Postman API client"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class PostmanPlugin(PluginBase):
    full_name = "Postman"
    name = "postman"
    description = "Installs Postman API client"
    depends_on: List[str] = []
    categories: List[str] = ["tool>api"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "--cask", "postman"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install --cask postman"]
            if pkg == "snap":
                return [["sudo", "snap", "install", "postman"]]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install -e --id Postman.Postman"]
            if pkg == "scoop":
                return [
                    "scoop bucket add extras",
                    "scoop install postman"
                ]
            if pkg == "choco":
                return ["choco install postman -y"]
        return []
