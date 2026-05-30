# plugins/gcp_cli_plugin.py
"""Installs Google Cloud Platform (GCP) CLI"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class GcpCliPlugin(PluginBase):
    name = "gcp_cli"
    description = "Installs Google Cloud Platform (GCP) CLI"
    depends_on: List[str] = []
    categories: List[str] = ["cloud", "devops"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "--cask", "gcloud-cli"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install --cask gcloud-cli"]
            if pkg == "apt":
                return [
                    "curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz",
                    "tar -xf google-cloud-cli-linux-x86_64.tar.gz",
                    "./google-cloud-sdk/install.sh",
                    "source ~/.bashrc",
                ]
            if pkg == "snap":
                return [["sudo", "snap", "install", "google-cloud-cli", "--classic"]]
        if os_name == "windows":
            if pkg == "winget":
                return ["winget install -e --id Google.CloudSDK"]
            if pkg == "choco":
                return [["choco", "install", "gcloudsdk", "-y"]]
        return []
