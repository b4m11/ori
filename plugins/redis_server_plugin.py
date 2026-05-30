# plugins/redis_server_plugin.py
"""Installs Redis database server"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class RedisServerPlugin(PluginBase):
    name = "redis_server"
    description = "Installs Redis database server"
    depends_on: List[str] = []
    categories: List[str] = ["database>server"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [
                "brew tap redis/redis",
                "brew install --cask redis"
            ]
        if os_name == "linux":
            if pkg == "apt":
                return [
                    """
                    apt-get install lsb-release curl gpg
                    curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
                    chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
                    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list
                    apt-get update
                    apt-get install redis
                    """
                ]
            if pkg == "snap":
                return [
                    "sudo apt update",
                    "sudo apt install redis-tools",
                    "sudo snap install redis"
                ]
        if os_name == "windows":
            if pkg == "scoop":
                return [
                    "scoop bucket add main",
                    "scoop install main/redis"
                ]
            if pkg == "winget":
                return ["winget install -e --id Redis.Redis"]
            if pkg == "choco":
                return [["choco", "install", "redis", "-y"]]
        return []
