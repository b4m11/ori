# plugins/terraform_plugin.py
"""Installs HashiCorp Terraform"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class TerraformPlugin(PluginBase):
    full_name = "Terraform"
    name = "terraform"
    description = "Installs HashiCorp Terraform"
    depends_on: List[str] = []
    categories: List[str] = ["iac", "devops"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [
                "brew tap hashicorp/tap",
                "brew install hashicorp/tap/terraform"
            ]
        if os_name == "linux":
            if pkg == "brew":
                return [
                    "brew tap hashicorp/tap",
                    "brew install hashicorp/tap/terraform"
                ]
            if pkg == "apt":
                return [
                    "wget -O - https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg",
                    "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main\" | sudo tee /etc/apt/sources.list.d/hashicorp.list",
                    "apt-get update",
                    "apt-get install terraform -y"
                ]
            if pkg == "snap":
                return ["snap install terraform --classic"]
        if os_name == "windows":
            if pkg == "scoop":
                return ["scoop install terraform"]
            if pkg == "winget":
                return [["winget", "install", "Hashicorp.Terraform"]]
            if pkg == "choco":
                return [["choco", "install", "terraform", "-y", "--pre"]]
        return []
