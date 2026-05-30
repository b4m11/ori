# plugins/ansible_plugin.py
"""Installs Ansible"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class AnsiblePlugin(PluginBase):
    name = "ansible"
    description = "Installs Ansible"
    depends_on: List[str] = []
    categories: List[str] = ["iac", "devops"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[str]:
        info = get_platform_info()
        os_name = info["os"]
        
        if os_name == "mac":
            return ["brew install ansible"]
        
        return ["python3 -m pip install ansible"]
