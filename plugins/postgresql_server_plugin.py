# plugins/postgresql_server_plugin.py
"""Installs PostgreSQL database server"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class PostgresqlServerPlugin(PluginBase):
    full_name = "PostgreSQL Server"
    name = "postgresql_server"
    description = "Installs PostgreSQL database server"
    depends_on: List[str] = []
    categories: List[str] = ["database>server"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "postgresql"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install postgresql"]
            if pkg == "apt":
                return [["apt", "-y", "install", "postgresql"]]
            if pkg == "snap":
                return ["snap install postgresql"]
        if os_name == "windows":
            if pkg == "scoop":
                return ["scoop install postgresql"]
            if pkg == "winget":
                return [["winget", "install", "PostgreSQL.PostgreSQL"]]
            if pkg == "choco":
                return [["choco", "install", "postgresql", "-y"]]
        return []
