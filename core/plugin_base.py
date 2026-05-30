# core/plugin_base.py
"""Base class for all setup plugins.
Each plugin must subclass :class:`PluginBase` and implement the required
attributes and methods. Plugins declare their name, optional dependencies on
other plugins, and a list of commands needed for installation.
The framework will execute the commands via :func:`core.runner.run_cmd`
ensuring safe subprocess invocation (no ``shell=True``).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

class PluginBase(ABC):
    """Abstract base class for setup plugins.

    Attributes
    ----------
    name: str
        Human‑readable identifier for the plugin.
    description: str
        Short description displayed in the UI.
    depends_on: List[str]
        List of plugin names that must be executed before this one.
    """

    name: str = "base"
    description: str = "Base plugin – should be subclassed."
    depends_on: List[str] = []
    compatible_systems: List[str] = []  # e.g., ['mac','linux','windows']; empty means all

    @property
    @abstractmethod
    def commands(self) -> List[List[str]]:
        """Return a list of command‑argument lists to run.

        Each command is represented as a list of strings, e.g.
        ``["brew", "install", "git"]``. The framework will call
        :func:`core.runner.run_cmd` for each entry.
        """
        raise NotImplementedError

    def pre_install(self) -> None:
        """Hook executed before any commands run.
        Sub‑classes may override to perform checks or setup steps.
        """
        pass

    def post_install(self) -> None:
        """Hook executed after all commands complete.
        Sub‑classes may override to perform cleanup or verification.
        """
        pass
