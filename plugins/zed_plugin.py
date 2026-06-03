# plugins/zed_plugin.py
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info
from typing import List

class ZedPlugin(PluginBase):
    full_name = "Zed IDE"
    name = "zed"
    description = "Installs zed on Windows"
    depends_on: List[str] = []
    categories: List[str] = ["tool>ide"]
    compatible_systems: List[str] = ["windows", "linux", "mac"]

    @property
    def install_commands(self) -> List[List[str]]:
        return []

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return ["brew install --cask zed"]
        if os_name == "linux":
            return ["curl -f https://zed.dev/install.sh | sh"]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install -e --id ZedIndustries.Zed"]
        return []

