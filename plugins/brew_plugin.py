# plugins/brew_plugin.py
"""Plugin to install Homebrew on macOS if it is missing.
The plugin name matches the executable `brew` so that the manager can discover it
when a command requires `brew` and it is not present on the system.
"""


from core.plugin_base import PluginBase
from typing import List
import os


class BrewPlugin(PluginBase):
    full_name = "Homebrew"
    name = "brew"
    description = "Installs Homebrew package manager on macOS."
    categories: List[str] = ["package_manager"]
    compatible_systems: List[str] = ["mac"]
    # No dependencies – should run before any other plugins that need brew.
    depends_on: List[str] = []

    @property
    def commands(self) -> List[List[str]]:
        # No regular install commands – the purpose of this plugin is to provide
        # installer commands when brew is missing.
        return []

    @property
    def install_commands(self) -> List[List[str]]:
        # Official Homebrew installation script.
        # os.environ['NONINTERACTIVE'] = '1'
        return [
            # 'NONINTERACTIVE=1 bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
            "curl -L -o /tmp/brew-installer.pkg 'https://github.com/Homebrew/brew/releases/download/5.1.14/Homebrew.pkg'",
            "installer -pkg /tmp/brew-installer.pkg -target /",
            'eval "$(/opt/homebrew/bin/brew shellenv)"'
        ]
