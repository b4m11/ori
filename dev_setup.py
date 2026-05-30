#!/usr/bin/env python3
"""dev_setup.py
A cross‑platform development environment setup tool.
"""

import argparse
import shutil
import sys
from pathlib import Path
import json
import curses
from web_ui.server import start_server
from core.platform_detect import get_platform_info

from typing import List

# Import core components
from core.manager import SetupManager
from core.config import load_config, DEFAULT_CONFIG

# ASCII art for welcome screen

ASCII_ART = r"""
  ___   _____   ___ 
 |_ _| |  ___| |_ _|
   | | | |_   | | 
   |_| |____| |_|
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross‑platform development environment setup tool"
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Run the web UI instead of the terminal UI."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Enable dry-run mode, passing --dry-run to commands."
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a JSON configuration file. If omitted, a built‑in default is used.",
    )
    return parser.parse_args()


def curses_plugin_selector(plugin_names):
    """Curses UI to select plugins.
    Returns a list of selected plugin names or ``None`` if the user presses Backspace to return to the previous screen.
    """
    selected = set()
    index = 0

    def draw(stdscr):
        nonlocal index, selected
        curses.curs_set(0)
        scroll_offset = 0
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            # Render ASCII art header
            # art_lines = ASCII_ART.splitlines()
            # for i, line in enumerate(art_lines):
            #     stdscr.addstr(i, 0, line)
            # prompt_y = len(art_lines) + 1
            
            prompt = "Select plugins (Space toggle, 'a' select all, 'd' deselect all, Backspace to go back, Enter confirm):"
            stdscr.addstr(0, 0, prompt[:width-1])
            
            available_lines = height - 2
            if available_lines <= 0:
                available_lines = 1
                
            if index < scroll_offset:
                scroll_offset = index
            elif index >= scroll_offset + available_lines:
                scroll_offset = index - available_lines + 1

            for i in range(scroll_offset, min(scroll_offset + available_lines, len(plugin_names))):
                name = plugin_names[i]
                marker = "[X]" if name in selected else "[ ]"
                line = f"{marker} {name}"[:width-1]
                line_y = 2 + i - scroll_offset
                if i == index:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(line_y, 0, line)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(line_y, 0, line)
            key = stdscr.getch()
            if key in (curses.KEY_UP, ord('k')):
                index = (index - 1) % len(plugin_names)
            elif key in (curses.KEY_DOWN, ord('j')):
                index = (index + 1) % len(plugin_names)
            elif key == ord(' '):
                name = plugin_names[index]
                if name in selected:
                    selected.remove(name)
                else:
                    selected.add(name)
            elif key == ord('a'):
                selected = set(plugin_names)
            elif key == ord('d'):
                selected.clear()
            elif key in (curses.KEY_ENTER, 10, 13):
                break
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                return None
            # Handle resize gracefully
            height, width = stdscr.getmaxyx()
        return list(selected)

    return curses.wrapper(draw)


def curses_profile_selector(profiles: List[str]) -> List[str]:
    """Hierarchical curses UI to select profile categories.

    Profiles may contain a '>' to denote hierarchy, e.g., "backend>js".
    Top‑level entries (e.g., "backend") are shown and selecting them
    includes all sub‑categories that start with "backend>".
    Returns a list of selected leaf profile strings.
    """
    # Build hierarchy mapping parent -> list of child full strings
    hierarchy: dict[str, List[str]] = {}
    leaves: set[str] = set()
    for cat in profiles:
        if ">" in cat:
            parent, child = cat.split('>', 1)
            hierarchy.setdefault(parent, []).append(cat)
            leaves.add(cat)
        else:
            hierarchy.setdefault(cat, [])
            leaves.add(cat)
    
    # Prepare display list: each entry is (display_text, associated leaf categories)
    display_items: List[tuple[str, List[str]]] = []
    for parent, children in hierarchy.items():
        if children:
            # Parent entry selects all its children
            display_items.append((parent + " (all)", children))
        else:
            # No children – treat as leaf itself
            display_items.append((parent, [parent]))
        # Add each child indented
        for child in children:
            # Show only the part after '>'
            display_items.append(("  " + child.split('>', 1)[1], [child]))

    selected: set[str] = set()
    index = 0

    def draw(stdscr):
        nonlocal index, selected
        curses.curs_set(0)
        scroll_offset = 0
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            prompt = "Select profiles (Space toggle, 'a' select all, 'd' deselect all, Enter confirm):"
            stdscr.addstr(0, 0, prompt[:width-1])
            
            available_lines = height - 2
            if available_lines <= 0:
                available_lines = 1
                
            if index < scroll_offset:
                scroll_offset = index
            elif index >= scroll_offset + available_lines:
                scroll_offset = index - available_lines + 1

            for i in range(scroll_offset, min(scroll_offset + available_lines, len(display_items))):
                disp, cats = display_items[i]
                # Mark selected if any of its associated leaf cats are selected
                marker = "[X]" if any(c in selected for c in cats) else "[ ]"
                line = f"{marker} {disp}"[:width-1]
                line_y = 2 + i - scroll_offset
                if i == index:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(line_y, 0, line)
                    stdscr.attroff(curses.A_REVERSE)
                else:
                    stdscr.addstr(line_y, 0, line)
            key = stdscr.getch()
            if key in (curses.KEY_UP, ord('k')):
                index = (index - 1) % len(display_items)
            elif key in (curses.KEY_DOWN, ord('j')):
                index = (index + 1) % len(display_items)
            elif key == ord(' '):
                # Toggle selection for all leaf categories associated with this entry
                _, cats = display_items[index]
                for c in cats:
                    if c in selected:
                        selected.remove(c)
                    else:
                        selected.add(c)
            elif key == ord('a'):
                selected = set(leaves)
            elif key == ord('d'):
                selected.clear()
            elif key in (curses.KEY_ENTER, 10, 13):
                break
            # Resize handling (no operation)
            _ = stdscr.getmaxyx()
        return list(selected)

    return curses.wrapper(draw)


def main() -> int:
    args = parse_args()
    try:
        config = load_config(args.config) if args.config else DEFAULT_CONFIG
        # Override dry_run flag from CLI argument if provided
        if getattr(args, "dry_run", False):
            config["dry_run"] = True

    except Exception as exc:
        print(f"[ERROR] Failed to load configuration: {exc}", file=sys.stderr)
        return 1

    # Initialise manager to discover all available plugins
    manager = SetupManager(config)

    # If web flag is set, start the web UI and exit
    if getattr(args, "web", False):
        start_server(manager)
        return 0

    # Ensure default package manager is installed before any user interaction
    platform_info = get_platform_info()
    default_pkg_mgr = platform_info.get("pkg_manager")
    if default_pkg_mgr and not shutil.which(default_pkg_mgr):
        # Find the installer plugin that provides this package manager
        installer = next((p for p in manager.all_plugins if getattr(p, "name", None) == default_pkg_mgr), None)
        if installer:
            print(f"[INFO] Installing default package manager: {default_pkg_mgr}")
            # Run the installer plugin directly
            manager._run_plugin(installer)
        else:
            print(f"[WARN] No installer plugin found for default package manager '{default_pkg_mgr}'.")

    # Gather all unique categories from plugins (default empty list if not present)
    all_categories = set()
    for p in manager.all_plugins:
        cats = getattr(p, "categories", [])
        all_categories.update(cats)

    # Profile selection UI (separate step)
    while True:
        # Profile selection UI (separate step)
        selected_profiles = []
        if all_categories:
            try:
                selected_profiles = curses_profile_selector(sorted(all_categories))
            except Exception as e:
                print(f"[WARN] Profile selection failed: {e}", file=sys.stderr)
        # Filter plugins based on selected profiles, always include plugins without categories (like installer plugins)
        if selected_profiles:
            available_plugins = []
            for p in manager.all_plugins:
                cats = getattr(p, "categories", [])
                if not cats:
                    # Include plugins that don't define categories (e.g., installer plugins)
                    available_plugins.append(p)
                    continue
                if any(cat in selected_profiles for cat in cats):
                    available_plugins.append(p)
        else:
            # If no profile selected or no categories, show all plugins
            available_plugins = manager.all_plugins

        # Determine current OS
        current_os = get_platform_info().get("os")
        # Filter plugins by compatible_systems attribute (empty means all)
        filtered_plugins = []
        for p in available_plugins:
            compat = getattr(p, "compatible_systems", [])
            if not compat or current_os in compat:
                filtered_plugins.append(p)
        available_plugins = filtered_plugins

        all_plugin_names = [p.name for p in available_plugins]
        # Run curses UI for plugin selection
        try:
            selected_plugins = curses_plugin_selector(all_plugin_names)
        except Exception:
            # Fallback: if curses fails, select all
            selected_plugins = all_plugin_names
        if selected_plugins is None:
            # User pressed Backspace – restart profile selection
            continue
        # Restrict manager to chosen plugins (by name)
        manager.plugins = [p for p in available_plugins if p.name in selected_plugins]
        manager.run()
        return 0


if __name__ == "__main__":
    sys.exit(main())
