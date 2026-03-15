#!/usr/bin/env python3
"""
Minimal HTTP server for testing the WebAssembly build locally.

Browsers require the Cross-Origin-Opener-Policy (COOP) and
Cross-Origin-Embedder-Policy (COEP) response headers to enable
SharedArrayBuffer, which is needed by pthreads.  Python's built-in
`http.server` does not set those headers, so this wrapper adds them.

Usage (from the repository root after building):

    cd build-wasm
    python3 ../src/wasm/server.py          # serves on port 8080
    python3 ../src/wasm/server.py 9000     # custom port

Then open http://localhost:8080/MarioKart64Recompiled.html
"""

import http.server
import sys
import os


class COEPHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler that injects COOP/COEP headers on every response."""

    def end_headers(self):
        # Required for SharedArrayBuffer / Atomics (pthreads inside WASM).
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Keep the default logging but prefix with a clear tag.
        sys.stderr.write("[wasm-server] " + (fmt % args) + "\n")


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server_address = ("", port)

    # Serve files from the directory where this script is invoked (typically
    # build-wasm/) rather than from the script's own directory.
    handler = COEPHandler
    handler.directory = os.getcwd()

    with http.server.HTTPServer(server_address, handler) as httpd:
        sys.stderr.write(
            f"[wasm-server] Serving on http://localhost:{port}/\n"
            f"[wasm-server] COOP + COEP headers enabled (SharedArrayBuffer / pthreads)\n"
            f"[wasm-server] Open http://localhost:{port}/MarioKart64Recompiled.html\n"
            f"[wasm-server] Press Ctrl-C to stop.\n"
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.stderr.write("\n[wasm-server] Stopped.\n")


if __name__ == "__main__":
    main()
