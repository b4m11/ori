# IFA

A cross-platform, automated developer environment setup tool.

This tool provides a beautiful web-based UI and a robust CLI to bootstrap your development environment. It installs essential tools, package managers, programming languages, and IDEs effortlessly across Linux, macOS, and Windows.

## Features

- **Web UI & CLI:** Run it in the terminal or launch the sleek web UI to select the programs you need.
- **Cross-Platform:** Works seamlessly on Windows, macOS, and Linux, detecting your platform and using the appropriate package managers (like `brew`, `apt`, `snap`, `winget`, `choco`).
- **Real-Time Streaming:** Installation logs are streamed live to both the terminal and the web browser.
- **Extensible Plugin System:** All installations are handled via a modular plugin architecture.
- **Dependency Resolution:** Automatically handles plugin dependencies (e.g., installing `winget` before attempting to install a tool via `winget`).

# Installation

### macOS

```sh
curl -fsSL https://gist.githubusercontent.com/b4m11/f33dcc49b2f9d4d478973da0c00c87ab/raw/065e0476e3f06bd6556001e01cb3f5914ef95657/install.sh -o install.sh
chmod +x install.sh
./install.sh  # add any args, e.g., --web
```

### Linux

```sh
curl -fsSL https://gist.githubusercontent.com/b4m11/f33dcc49b2f9d4d478973da0c00c87ab/raw/065e0476e3f06bd6556001e01cb3f5914ef95657/install.sh -o install.sh
chmod +x install.sh
./install.sh  # add any args, e.g., --web
```

### Windows

Download the latest binary from the [Releases page](https://github.com/b4m11/ori/releases) and run the appropriate executable.



## Dev
You can run the setup tool via the command line:

```bash
# Run the setup tool
python dev_setup.py

# Launch the web UI on http://127.0.0.1:8000
python dev_setup.py --web
```

If you download the compiled PyInstaller binary from the Releases page, you can simply run the executable directly.

## Contributing Plugins

The power of this tool comes from its plugins! If you have a favorite tool, language, or setup script that isn't included, **I'm completely open to people writing new plugins**.

Please feel free to create a plugin for your favorite tools and submit an upstream **Pull Request**. 

### How to write a plugin

Creating a plugin is extremely simple. Just add a new Python file in the `plugins/` directory.

Example: `plugins/my_tool_plugin.py`
```python
from core.plugin_base import PluginBase
from core.platform_detect import get_platform_info
from typing import List

class MyToolPlugin(PluginBase):
    name = "my_tool" # this is the command name that runs your
    full_name = "My Tool"
    description = "Installs My Tool"
    depends_on: List[str] = [] # List dependencies here
    categories: List[str] = ["tool>utility"]
    compatible_systems: List[str] = ["linux", "mac", "windows"]

    @property
    def commands(self) -> List[List[str]]:
        info = get_platform_info()
        os_name = info["os"]
        pkg = info["pkg_manager"]
        
        if os_name == "mac":
            return ["brew install my_tool"]
        if os_name == "linux":
            if pkg == "apt":
                return ["apt-get install -y my_tool"]
        return []
```

## License
MIT License
