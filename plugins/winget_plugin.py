# plugins/winget_plugin.py
"""Winget installer plugin – installs the Windows Package Manager (winget) if missing.
The plugin name matches the executable `winget` so the manager can discover it and run its
installation commands when the platform is Windows and winget is not present.
"""

from core.plugin_base import PluginBase
from typing import List

class WingetPlugin(PluginBase):
    full_name = "Winget"
    name = "winget"
    description = "Installs Winget package manager on Windows"
    depends_on: List[str] = []
    categories: List[str] = ["package_manager"]
    compatible_systems: List[str] = ["windows"]

    @property
    def install_commands(self) -> List[List[str]]:
        # Use PowerShell to download and install the latest winget MSIX bundle.
        # This is a simplified approach; in production you might need admin rights.
        return [
            ["powershell", "-Command", "Invoke-WebRequest -Uri https://aka.ms/getwinget -OutFile winget.msixbundle"],
            ["powershell", "-Command", "Add-AppxPackage winget.msixbundle"],
        ]

    @property
    def commands(self) -> List[List[str]]:
        # No regular install commands – the purpose of this plugin is to provide
        # installer commands when brew is missing.
        return []
