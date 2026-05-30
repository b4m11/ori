# core/config.py
"""Configuration handling for dev_setup.
Provides a default configuration dictionary and a helper to load a YAML file.
"""

import json
from pathlib import Path

# Default configuration used when no config file is provided.
DEFAULT_CONFIG = {
    # "dry_run": True,
    "plugins": [],
    "custom_plugins": [],
}

def load_config(path: Path):
    """Load a JSON configuration file.

    Parameters
    ----------
    path: Path
        Path to the JSON config file.
    Returns
    -------
    dict
        Parsed configuration dictionary.
    """
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f) if path.suffix.lower() in {".json", ".js"} else {}
    return data
