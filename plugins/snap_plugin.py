# plugins/snap_plugin.py

from core.plugin_base import PluginBase
from typing import List
from core.platform_detect import get_platform_info

class SnapPlugin(PluginBase):
    name = "snap"
    description = "Installs snap"
    depends_on: List[str] = []
    categories: List[str] = ["package_manager"]
    compatible_systems: List[str] = ["linux", "mac"]

    @property
    def install_commands(self) -> List[List[str]]:
        return []

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return ["brew install snapcraft"]
        if os_name == "linux":
            if pkg == "apt":
                return [
                    "apt install snapd",
                    "exec $(echo $0)",
                    "snap install snapd"
                ]
        return []

