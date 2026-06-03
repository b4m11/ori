# plugins/mysql_server_plugin.py
"""Installs MySQL database server"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class MysqlServerPlugin(PluginBase):
    full_name = "MySQL Server"
    name = "mysql_server"
    description = "Installs MySQL database server"
    depends_on: List[str] = []
    categories: List[str] = ["database>server"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "mysql"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install mysql"]
            if pkg == "apt":
                return [["apt", "-y", "install", "mysql-server"]]
            if pkg == "dnf":
                return ["dnf install mysql-community-server"]
            if pkg == "snap":
                return ["snap install mysql"]
        if os_name == "windows":
            if pkg == "scoop":
                return ["scoop install mysql -g"]
            if pkg == "winget":
                return [["winget", "install", "Oracle.MySQL"]]
            if pkg == "choco":
                return [["choco", "install", "mysql-cli", "-y"]]
        return []
