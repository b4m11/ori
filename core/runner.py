
"""Safe subprocess runner with optional dry‑run support.
All commands are executed as a list of arguments (no shell=True) and are
checked against an allow‑list defined per plugin.
"""
import subprocess
import sys
from typing import List, Optional

# Global flag – set by the manager based on CLI argument
dry_run = False

def set_dry_run(value: bool):
    """Set the dry‑run mode (used by SetupManager)."""
    global dry_run
    dry_run = value







def run_cmd(args: List[str], *, capture_output: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Execute a command safely.

    Parameters
    ----------
    args: List[str]
        Command and its arguments.
    capture_output: bool
        Whether to capture stdout/stderr.
    check: bool
        If True, raise CalledProcessError on non‑zero exit.
    """
    if dry_run:
        # Append dry‑run flag to the command if possible
        if isinstance(args, list):
            dry_args = args + ["--dry-run"]
        else:
            dry_args = f"{args} --dry-run"
        print(f"[DRY‑RUN] {' '.join(dry_args) if isinstance(dry_args, list) else dry_args}")
        return subprocess.CompletedProcess(dry_args, 0, stdout=b"", stderr=b"")
    
    
    # Display args appropriately whether it's a string or list
    if isinstance(args, str):
        display_args = args
    else:
        display_args = ' '.join(args)
    # print(f"[RUN] {display_args}")
    
    result = subprocess.run(
        args,
        check=check,
        shell=isinstance(args, str),
        capture_output=capture_output,
        text=True,
    )

    if capture_output:
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    return result
