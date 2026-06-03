# plugins/mongodb_server_plugin.py
"""Installs MongoDB database server"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class MongodbServerPlugin(PluginBase):
    full_name = "Mongo DB Server"
    name = "mongodb_server"
    description = "Installs MongoDB database server"
    depends_on: List[str] = []
    categories: List[str] = ["database>server"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "mongodb-atlas"]]
        if os_name == "linux":
            if pkg == "brew":
                return [["brew", "install", "mongodb-atlas"]]
            if pkg == "snap":
                return ["snap install charmed-mongodb"]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install -e --id MongoDB.Server"]
            if pkg == "choco":
                return ["choco install mongodb-atlas"]
        return []
