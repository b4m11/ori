# plugins/docker_plugin.py
"""Installs Docker Engine / Desktop"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class DockerPlugin(PluginBase):
    full_name = "Docker"
    name = "docker"
    description = "Installs Docker Engine / Desktop"
    depends_on: List[str] = []
    categories: List[str] = ["container", "devops"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return ["brew install docker"]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install docker"]
            return ["curl -fsSL https://get.docker.com -o get-docker.sh | sh get-docker.sh"]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install -e --id Docker.DockerDesktop"]
            if pkg == "choco":
                return [["choco", "install", "docker-desktop", "-y"]]
        return []
