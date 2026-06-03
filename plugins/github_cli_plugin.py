# plugins/github_cli_plugin.py
"""Installs GitHub CLI (gh)"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class GithubCliPlugin(PluginBase):
    full_name = "GitHub CLI"
    name = "github_cli"
    description = "Installs GitHub CLI (gh)"
    depends_on: List[str] = []
    categories: List[str] = ["tool>vcs"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "gh"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install gh"]
            return [
                '(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
                && sudo mkdir -p -m 755 /etc/apt/keyrings \
                && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
                && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
                && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
                && sudo mkdir -p -m 755 /etc/apt/sources.list.d \
                && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
                && sudo apt update \
                && sudo apt install gh -y'
            ]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install --id GitHub.cli --source winget"]
            if pkg == "choco":
                return [["choco", "install", "gh", "-y"]]
        return []
