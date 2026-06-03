# plugins/gitlab_cli_plugin.py
"""Installs GitLab CLI (glab)"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class GitlabCliPlugin(PluginBase):
    full_name = "GitLab CLI"
    name = "gitlab_cli"
    description = "Installs GitLab CLI (glab)"
    depends_on: List[str] = []
    categories: List[str] = ["tool>vcs"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return ["brew install glab"]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install glab"]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install glab.glab"]
            if pkg == "choco":
                return ["choco install glab -y"]
        return []
