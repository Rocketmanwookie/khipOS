from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

from .runtime import Runtime


class Handler(SimpleHTTPRequestHandler):
    runtime: Runtime
    ui_dir: Path

    def translate_path(self, path: str) -> str:
        requested = urlparse(path).path.lstrip("/") or "index.html"
        return str(self.ui_dir / requested)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[khip-os] {fmt % args}")

    def send_json(self, status: int, value: dict | list) -> None:
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/status":
            return self.send_json(200, self.runtime.status())
        if path == "/api/projects":
            return self.send_json(200, self.runtime.list_projects())
        super().do_GET()

    def do_POST(self) -> None:
        try:
            payload = self.read_json()
            if self.path == "/api/intents":
                return self.send_json(200, self.runtime.handle_intent(payload.get("text", ""), payload.get("project_id")))
            if self.path == "/api/projects":
                return self.send_json(201, self.runtime.create_project(payload.get("name", ""), payload.get("description", "")))
            self.send_json(404, {"error": "Not found"})
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json(400, {"error": str(exc)})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    parser.add_argument("--data", default="data")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    Handler.runtime = Runtime(Path(args.data).resolve())
    Handler.ui_dir = root / "ui"
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"KHIP OS running at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
