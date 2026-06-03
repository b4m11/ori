# plugins/ruby_plugin.py
"""Installs Ruby programming language"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class RubyPlugin(PluginBase):
    full_name = "Ruby"
    name = "ruby"
    description = "Installs Ruby programming language"
    depends_on: List[str] = []
    categories: List[str] = ["language"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "ruby"]]
        if os_name == "linux":
            if pkg == "apt":
                return [["apt-get", "install", "-y", "ruby-full"]]
            if pkg == "snap":
                return [["snap", "install", "ruby", "--classic"]]
        if os_name == "windows":
            if pkg == "winget":
                return [["winget", "install", "RubyInstallerTeam.Ruby"]]
            if pkg == "choco":
                return [["choco", "install", "ruby", "-y"]]
        return []
