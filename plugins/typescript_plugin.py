# plugins/typescript_plugin.py
"""Installs TypeScript compiler globally"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class TypescriptPlugin(PluginBase):
    full_name = "Typescript"
    name = "typescript"
    description = "Installs TypeScript compiler globally"
    depends_on: List[str] = ["node"]
    categories: List[str] = ["language"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        return ["npm install typescript -g"]
