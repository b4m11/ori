# plugins/helm_plugin.py
"""Installs Helm package manager for Kubernetes"""

from __future__ import annotations
from typing import List
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info

class HelmPlugin(PluginBase):
    full_name = "Helm"
    name = "helm"
    description = "Installs Helm package manager for Kubernetes"
    depends_on: List[str] = []
    categories: List[str] = ["container", "devops", "package_manager"]
    compatible_systems: List[str] = ["mac", "windows", "linux"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return [["brew", "install", "helm"]]
        if os_name == "linux":
            if pkg == "brew":
                return ["brew install helm"]
            if pkg == "apt":
                return [
                    """
                    HELM_BUILDKITE_APT_KEY_ID="DDF78C3E6EBB2D2CC223C95C62BA89D07698DBC6"'
                    apt-get install curl gpg apt-transport-https --yes'
                    curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey > "${TMPDIR:-/tmp}/helm.gpg"'
                    if [ "$(gpg --show-keys --with-colons "${TMPDIR:-/tmp}/helm.gpg" | awk -F: '$1 == "fpr" {print $10}' | head -n 1)" != "${HELM_BUILDKITE_APT_KEY_ID}" ]; then echo "ERROR: Unexpected Helm APT key ID: potential key compromise"; exit 1; fi'
                    cat "${TMPDIR:-/tmp}/helm.gpg" | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null'
                    echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list'
                    apt-get update'
                    apt-get install helm
                    """
                ]
            if pkg == "dnf":
                return ["sudo dnf install helm"]
            if pkg == "pkg":
                return ["pkg install helm"]
            if pkg == "snap":
                return [["sudo", "snap", "install", "helm", "--classic"]]
        if os_name == "windows":
            if pkg == "winget":
                return [["winget", "install", "Helm.Helm"]]
            if pkg == "choco":
                return [["choco", "install", "kubernetes-helm", "-y"]]
            if pkg == "scoop":
                return ["scoop install helm"]
        return []
