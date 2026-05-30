# plugins/vscode_plugin.py

from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info
from typing import List

class VsCodePlugin(PluginBase):
    name = "code"
    description = "Installs VSCODE on Windows"
    depends_on: List[str] = []
    categories: List[str] = ["tool>ide"]
    compatible_systems: List[str] = ["windows", "linux", "mac"]

    @property
    def install_commands(self) -> List[List[str]]:
        # Use PowerShell to download and install the latest winget MSIX bundle.
        # This is a simplified approach; in production you might need admin rights.
        return []

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return ["brew install --cask visual-studio-code"]
        if os_name == "linux":
            if pkg == "snap":
                return ["snap install code --classic"]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install -e --id Microsoft.VisualStudioCode"]
            if pkg == "choco":
                return ["choco install vscode.install -y"]
        return []

