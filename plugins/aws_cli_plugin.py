# plugins/aws_cli_plugin.py
"""Installs Amazon Web Services (AWS) CLI"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class AwsCliPlugin(PluginBase):
    full_name = "AWS CLI"
    name = "aws_cli"
    description = "Installs Amazon Web Services (AWS) CLI"
    depends_on: List[str] = []
    categories: List[str] = ["cloud", "devops"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "linux":
            return [
                'curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"',
                'unzip awscliv2.zip',
                'sudo ./aws/install'
            ]

        if os_name == "mac":
            return [
                'curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"',
                'sudo installer -pkg AWSCLIV2.pkg -target /'
            ]
            
        if os_name == "windows":
            return [
                "msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi"
            ]
        return []

