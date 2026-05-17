"""Discovery Engine API — lightweight HTTP server for topic submissions.

Runs on the VM to receive topic submissions from the web app.
Writes to a JSON queue file that the pipeline cron job consumes.
Pushes results back to the discoveries repo for the queue dashboard.

Run: python3 discovery_api.py [port]
Default port: 8088
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler

QUEUE_DIR = os.path.expanduser("~/.hermes/discovery-queue")
QUEUE_FILE = os.path.join(QUEUE_DIR, "queue.json")
DASHBOARD_FILE = os.path.join(QUEUE_DIR, "queue-published.json")
DISCOVERIES_REPO = os.path.expanduser("~/discoveries")
MAX_BODY = 100 * 1024  # 100KB


def ensure_queue():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    if not os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "w") as f:
            json.dump({"topics": [], "runs": []}, f)


def load_queue():
    ensure_queue()
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(data):
    ensure_queue()
    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)
    # Also write the dashboard copy (for gh-pages)
    publish_dashboard(data)


def publish_dashboard(data):
    """Write a sanitized version of the queue for the web app dashboard."""
    dashboard = {
        "topics": [
            {
                "id": t["id"],
                "title": t["title"],
                "description": t.get("description", "")[:200],
                "status": t.get("status", "pending"),
                "created_at": t.get("created_at", ""),
                "completed_at": t.get("completed_at", ""),
                "publication_url": t.get("publication_url", ""),
            }
            for t in data.get("topics", [])
        ]
    }
    # Write to the discoveries repo so it gets deployed
    repo_path = DISCOVERIES_REPO
    if os.path.exists(os.path.join(repo_path, ".git")):
        dest = os.path.join(repo_path, "api", "queue.json")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w") as f:
            json.dump(dashboard, f, indent=2)
        try:
            subprocess.run(
                ["git", "add", "api/queue.json"], cwd=repo_path, capture_output=True
            )
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    f"queue: update dashboard — {len(dashboard['topics'])} topics",
                    "--allow-empty",
                ],
                cwd=repo_path,
                capture_output=True,
            )
            subprocess.run(["git", "push"], cwd=repo_path, capture_output=True)
        except Exception as e:
            print(f"[warn] git push failed: {e}")


def generate_id():
    ts = int(time.time() * 1000)
    return f"topic_{ts}"


class DiscoveryHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self._send_json({})

    def do_GET(self):
        if self.path == "/api/health":
            self._send_json({"status": "ok", "time": datetime.now(timezone.utc).isoformat()})
        elif self.path == "/api/queue":
            data = load_queue()
            # Return a sanitized version for the dashboard
            topics = [
                {
                    "id": t["id"],
                    "title": t["title"],
                    "description": t.get("description", "")[:200],
                    "status": t.get("status", "pending"),
                    "created_at": t.get("created_at", ""),
                }
                for t in data.get("topics", [])
            ]
            self._send_json({"topics": topics})
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/api/submit":
            self._send_json({"error": "not found"}, 404)

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > MAX_BODY:
            self._send_json({"error": "body too large"}, 413)

        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "invalid JSON"}, 400)

        title = (payload.get("title") or "").strip()
        if not title:
            self._send_json({"error": "title is required"}, 400)

        topic = {
            "id": generate_id(),
            "title": title,
            "description": (payload.get("description") or "").strip(),
            "domains": payload.get("domains", []),
            "email": (payload.get("email") or "").strip(),
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
            "publication_url": None,
        }

        data = load_queue()
        data["topics"].append(topic)
        save_queue(data)

        self._send_json(
            {"status": "accepted", "topic": topic}, status=201
        )


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8088
    ensure_queue()
    server = HTTPServer(("0.0.0.0", port), DiscoveryHandler)
    print(f"Discovery API running on http://0.0.0.0:{port}")
    print(f"Queue file: {QUEUE_FILE}")
    print(f"Dashboard pushed to: {DISCOVERIES_REPO}/api/queue.json")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
