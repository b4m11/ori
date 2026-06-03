# plugins/kubernetes_plugin.py
"""Installs Kubernetes CLI (kubectl)"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class KubernetesPlugin(PluginBase):
    full_name = "Kubernetes"
    name = "kubernetes"
    description = "Installs Kubernetes CLI (kubectl)"
    depends_on: List[str] = []
    categories: List[str] = ["container", "devops"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "kubectl"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install kubectl"]

            if pkg == "snap":
                return ["sudo snap install kubectl --classic"]

            return [
                "curl -sSL https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/$(uname -m | sed -e 's/x86_64/amd64/' -e 's/aarch64/arm64/')/kubectl -o kubectl && chmod +x kubectl",
                "install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl",
                "kubectl version --client"
            ]
        if os_name == "windows":
            if pkg == "scoop":
                return ["scoop install kubectl"]
            if pkg == "winget":
                return [["winget", "install", "Kubernetes.kubectl"]]
            if pkg == "choco":
                return [["choco", "install", "kubernetes-cli", "-y"]]
                
            return ["curl.exe -LO \"https://dl.k8s.io/release/v1.36.0/bin/windows/amd64/kubectl.exe\""]
        return []
