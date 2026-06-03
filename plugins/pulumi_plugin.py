# plugins/pulumi_plugin.py
"""Installs Pulumi"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class PulumiPlugin(PluginBase):
    full_name = "Pulumi"
    name = "pulumi"
    description = "Installs Pulumi"
    depends_on: List[str] = []
    categories: List[str] = ["iac", "devops"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return ["brew install pulumi/tap/pulumi"]
        if os_name == "linux":
            return [["curl", "-fsSL", "https://get.pulumi.com", "|", "sh"]]
        if os_name == "windows":
            if pkg == "winget":
                return [["winget", "install", "pulumi"]]
            if pkg == "choco":
                return [["choco", "install", "pulumi", "-y"]]
            return [
                """
                @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://get.pulumi.com/install.ps1'))" && SET "PATH=%PATH%;%USERPROFILE%\.pulumi\bin"
                """
            ]
        return []
