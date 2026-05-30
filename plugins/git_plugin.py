# plugins/git_plugin.py
"""Installs Git version control system"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class GitPlugin(PluginBase):
    name = "git"
    description = "Installs Git version control system"
    depends_on: List[str] = []
    categories: List[str] = ["tool>vcs"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "git"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install git"]
            if pkg == "apt":
                return [["sudo", "apt", "-y", "install", "git"]]
            if pkg == "snap":
                return []
        if os_name == "windows":
            if pkg == "winget":
                return [["winget", "install", "Git.Git"]]
            if pkg == "choco":
                return [["choco", "install", "git", "-y"]]
        return []
