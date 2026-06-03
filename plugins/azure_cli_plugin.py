# plugins/azure_cli_plugin.py
"""Installs Microsoft Azure CLI"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class AzureCliPlugin(PluginBase):
    name = "azure_cli"
    full_name = "Azure CLI"
    description = "Installs Microsoft Azure CLI"
    depends_on: List[str] = []
    categories: List[str] = ["cloud", "devops"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "azure-cli"]]
        if os_name == "linux":
            return ["curl -fsSL 'https://azurecliprod.blob.core.windows.net/$root/deb_install.sh' | sudo bash"]

        if os_name == "windows":
            if pkg == "winget":
                return ["winget install --exact --id Microsoft.AzureCLI"]
            if pkg == "choco":
                return [["choco", "install", "azure-cli", "-y"]]
        return []
