import sys
import shutil
from typing import Dict

def get_platform_info() -> Dict[str, str]:
    """Detect the current operating system and available package managers.

    Returns
    -------
    dict
        Keys:
        - "os": one of "mac", "linux", "windows"
        - "pkg_manager": the primary package manager command name
    """
    # Detect OS
    # print(f"platform:: {sys.platform} {shutil.which('brew')} {shutil.which('apt')} {shutil.which('snap')} {shutil.which('winget')} {shutil.which('choco')}")
    if sys.platform.startswith("darwin"):
        os_name = "mac"
        pkg_manager = "brew"
    elif sys.platform.startswith("linux"):
        os_name = "linux"
        if shutil.which("apt"):
            pkg_manager = "apt"
        elif shutil.which("brew"):
            pkg_manager = "brew"
        elif shutil.which("snap"):
            pkg_manager = "snap"
        else:
            pkg_manager = None
    elif sys.platform.startswith("win"):
        os_name = "windows"
        if shutil.which("winget"):
            pkg_manager = "winget"
        elif shutil.which("scoop"):
            pkg_manager = "scoop"
        elif shutil.which("choco"):
            pkg_manager = "choco"
        else:
            pkg_manager = None
    else:
        os_name = "unknown"
        pkg_manager = None
    return {"os": os_name, "pkg_manager": pkg_manager}
