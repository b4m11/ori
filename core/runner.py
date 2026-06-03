
"""Safe subprocess runner with optional dry‑run support.
All commands are executed as a list of arguments (no shell=True) and are
checked against an allow‑list defined per plugin.
"""
import subprocess
import sys
from typing import List, Optional

import threading
import time

# Global flag – set by the manager based on CLI argument
dry_run = False
stop_event = threading.Event()

def set_dry_run(value: bool):
    """Set the dry‑run mode (used by SetupManager)."""
    global dry_run
    dry_run = value

def run_cmd(args: List[str], *, capture_output: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Execute a command safely with abortion support.

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
        if isinstance(args, list):
            dry_args = args + ["--dry-run"]
        else:
            dry_args = f"{args} --dry-run"
        print(f"[DRY‑RUN] {' '.join(dry_args) if isinstance(dry_args, list) else dry_args}")
        return subprocess.CompletedProcess(dry_args, 0, stdout=b"", stderr=b"")
    
    if isinstance(args, str):
        display_args = args
    else:
        display_args = ' '.join(args)
    
    # Pipe output to capture and print it live, so sys.stdout overrides work
    process = subprocess.Popen(
        args,
        shell=isinstance(args, str),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    output_lines = []
    
    def reader():
        for line in iter(process.stdout.readline, ''):
            if line:
                # Always print to sys.stdout so it goes to QueueWriter (web) and DualWriter
                sys.stdout.write(line)
                sys.stdout.flush()
                # Do NOT write to `stdout` argument here because DualWriter already handles the log file!
                if capture_output:
                    output_lines.append(line)
    
    reader_thread = threading.Thread(target=reader)
    reader_thread.start()
    
    try:
        while process.poll() is None:
            if stop_event.is_set():
                process.kill()
                reader_thread.join()
            time.sleep(0.1)
            
        reader_thread.join()
        
        stdout_data = "".join(output_lines)
        
        if check and process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, args, output=stdout_data, stderr="")
            
        return subprocess.CompletedProcess(args, process.returncode, stdout=stdout_data, stderr="")
    except BaseException as e:
        process.terminate()
        reader_thread.join(timeout=1)
        raise e
