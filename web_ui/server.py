# web_ui/server.py
"""Simple HTTP server serving the web UI and providing API endpoints.
Implements:
- GET /api/profiles   -> JSON list of profile categories
- GET /api/plugins   -> JSON list of plugin names with categories
- POST /api/run       -> Starts installation and streams output via Server‑Sent Events (SSE)
- GET  /api/stream    -> SSE endpoint yielding output lines
"""

import json
import os
import sys
import threading
import queue
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

# Import core components
from core.manager import SetupManager
from core.config import DEFAULT_CONFIG, load_config

# Global queue for streaming installation output
_output_queue: "queue.Queue[str]" = queue.Queue()

class DevSetupHandler(SimpleHTTPRequestHandler):
    """Handler serving static files from ./web_ui and JSON API routes."""

    def __init__(self, *args, manager: SetupManager, **kwargs):
        self.manager = manager
        # Resolve the directory containing the UI assets
        self.ui_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web_ui"))
        super().__init__(*args, directory=self.ui_dir, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/profiles":
            self._send_json({"profiles": self._gather_profiles()})
        elif parsed.path == "/api/plugins":
            self._send_json({"plugins": self._gather_plugins()})
        elif parsed.path == "/api/stream":
            self._handle_sse()
        else:
            # Serve static files (index.html, CSS, JS) normally
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/run":
            # Expect JSON body with optional "profiles" and "plugins"
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            data = json.loads(body) if body else {}
            # Store selection in manager config
            # self.manager.config["selected_plugins"] = data.get("plugins", [])
            self.manager.plugins = [p for p in self.manager.all_plugins if p.name in data.get("plugins", [])]

            # Run installation in background thread
            threading.Thread(target=self._run_installation, daemon=True).start()
            self.send_response(HTTPStatus.OK)
            self.end_headers()
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown endpoint")

    def _send_json(self, data):
        """Send JSON response with proper headers."""
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    # ---------------------------------------------------------------------
    # Helper methods
    # ---------------------------------------------------------------------
    def _gather_profiles(self) -> list:
        # Re‑use the same logic as in dev_setup.py to collect categories
        from core.manager import SetupManager
        sm = SetupManager(self.manager.config)
        all_cats = set()
        for p in sm.all_plugins:
            all_cats.update(getattr(p, "categories", []))
        return sorted(all_cats)

    def _gather_plugins(self) -> list:
        # Return list of plugin dicts: {name, categories}
        plugins = []
        for p in self.manager.all_plugins:
            plugins.append({"name": p.name, "categories": getattr(p, "categories", [])})
        return plugins

    def _run_installation(self):
        # Redirect stdout/stderr to the queue while manager runs.
        class QueueWriter:
            def write(self, s: str):
                if s:
                    _output_queue.put(s)
            def flush(self):
                pass
        original_stdout, original_stderr = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = QueueWriter()
        try:
            self.manager.run()
        finally:
            sys.stdout, sys.stderr = original_stdout, original_stderr
            # After run, gather plugin log files and send their contents to client
            try:
                import json, os
                log_dir = getattr(self.manager, "output_dir", None)
                if log_dir and os.path.isdir(log_dir):
                    for fname in os.listdir(log_dir):
                        if not fname.endswith('.log'):
                            continue
                        full_path = os.path.abspath(os.path.join(log_dir, fname))
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        payload = json.dumps({"name": fname, "content": content})
                        _output_queue.put('[LOGFILE]' + payload)
            except Exception as e:
                print(f"[ERROR] Gathering log files failed: {e}", file=sys.stderr)
            
            _output_queue.put('[DONE]')
            # After sending logs, delete them to clean up
            try:
                if log_dir and os.path.isdir(log_dir):
                    for f in os.listdir(log_dir):
                        if f.endswith('.log'):
                            os.remove(os.path.join(log_dir, f))
            except Exception as e_cleanup:
                print(f"[WARN] Failed to clean up log files: {e_cleanup}", file=sys.stderr)
            # Signal end of stream
            


    def _handle_sse(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.end_headers()
        
        while True:
            try:
                line = _output_queue.get(timeout=1.0)
                if line == "[DONE]":
                    self.wfile.write(f"data: [DONE]\n\n".encode())
                    self.wfile.write(b"event: close\ndata: end\n\n")
                    self.wfile.flush()
                    break

                # Escape newlines to keep data in one SSE event
                safe_line = line.replace('\n', ' ')
                self.wfile.write(f"data: {safe_line}\n\n".encode())
                self.wfile.flush()
            except queue.Empty:
                # Send keep-alive comment to prevent timeout
                self.wfile.write(b": keepalive\n\n")
                self.wfile.flush()
            except (ConnectionResetError, BrokenPipeError):
                break

def start_server(manager: SetupManager, host: str = "127.0.0.1", port: int = 8000):
    """Launch the HTTP server in a background thread."""
    handler = lambda *args, **kwargs: DevSetupHandler(*args, manager=manager, **kwargs)
    httpd = ThreadingHTTPServer((host, port), handler)
    print(f"[INFO] Web UI listening at http://{host}:{port}")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    # Block main thread – the server runs until the process is killed
    try:
        while True:
            pass
    except KeyboardInterrupt:
        httpd.shutdown()
        print("[INFO] Server stopped")
