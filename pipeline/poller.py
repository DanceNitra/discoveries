"""Pipeline poller — reads the discovery queue and triggers agent pipeline runs.

Now invokes Hermes skills in sequence:
  1. discovery-query-classifier
  2. discovery-orchestrator
  3. discovery-writer-agent
  4. discovery-validator-agent
  5. discovery-publisher-agent

The poller manages the queue and status. Skills do the actual work.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

QUEUE_DIR = os.path.expanduser("~/.hermes/discovery-queue")
QUEUE_FILE = os.path.join(QUEUE_DIR, "queue.json")
DISCOVERIES_REPO = os.path.expanduser("~/discoveries")
PID_FILE = os.path.join(QUEUE_DIR, "pipeline.pid")

STATUS_PENDING = "pending"
STATUS_IN_PROGRESS = "in_progress"
STATUS_PUBLISHED = "published"
STATUS_FAILED = "failed"
STATUS_VALIDATED = "validated"
STATUS_WRITING = "writing"
STATUS_VALIDATING = "validating"


def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return {"topics": [], "runs": []}
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(data):
    os.makedirs(QUEUE_DIR, exist_ok=True)
    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)
    publish_dashboard(data)


def publish_dashboard(data):
    dashboard = {
        "topics": [
            {
                "id": t["id"],
                "title": t["title"],
                "description": (t.get("description") or "")[:200],
                "domains": t.get("domains", []),
                "status": t.get("status", "pending"),
                "created_at": t.get("created_at", ""),
                "completed_at": t.get("completed_at", ""),
            }
            for t in data.get("topics", [])
        ]
    }
    if os.path.exists(os.path.join(DISCOVERIES_REPO, ".git")):
        dest = os.path.join(DISCOVERIES_REPO, "api", "queue.json")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w") as f:
            json.dump(dashboard, f, indent=2)
        try:
            subprocess.run(
                ["git", "add", "api/queue.json"],
                cwd=DISCOVERIES_REPO, capture_output=True,
            )
            subprocess.run(
                [
                    "git", "commit",
                    "-m", f"queue: update dashboard — {len(dashboard['topics'])} topics",
                    "--allow-empty",
                ],
                cwd=DISCOVERIES_REPO, capture_output=True,
            )
            subprocess.run(["git", "push"], cwd=DISCOVERIES_REPO, capture_output=True)
        except Exception as e:
            print(f"[warn] git push failed: {e}")


def acquire_lock():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print(f"[warn] Pipeline already running (PID {pid})")
            return False
        except (OSError, ValueError):
            pass
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True


def release_lock():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def ensure_results_dir(topic_id):
    d = os.path.join(QUEUE_DIR, "results", topic_id)
    os.makedirs(d, exist_ok=True)
    return d


def find_topic(data, topic_id):
    for t in data.get("topics", []):
        if t["id"] == topic_id:
            return t
    return None


def set_status(data, topic_id, status, **extra):
    t = find_topic(data, topic_id)
    if t:
        t["status"] = status
        for k, v in extra.items():
            t[k] = v
    return data


def main():
    once = "--once" in sys.argv
    force_topic = None
    for arg in sys.argv:
        if arg.startswith("--topic="):
            force_topic = arg.split("=", 1)[1]

    if not acquire_lock():
        return 1

    try:
        data = load_queue()

        # Determine which topics to process
        if force_topic:
            candidates = [t for t in data.get("topics", []) if t["id"] == force_topic]
        else:
            # Process in priority order: pending > failed > writing > validating
            candidates = [t for t in data.get("topics", [])
                         if t.get("status") in (STATUS_PENDING, STATUS_FAILED)]

        if not candidates:
            print("No topics to process.")
            return 0

        topic = candidates[0]
        topic_id = topic["id"]
        title = topic["title"]
        results_dir = ensure_results_dir(topic_id)

        print(f"Topic: {title} ({topic_id})")
        print(f"Status: {topic.get('status')}")
        print(f"Results dir: {results_dir}")
        print("")
        print("This script manages the queue. Skills do the work.")
        print("")
        print("To process this topic, run with an LLM-driven cron job")
        print("that loads the pipeline skills in sequence:")
        print("")
        print("  1. skill_view('discovery-query-classifier')")
        print("  2. skill_view('discovery-orchestrator')")
        print("  3. skill_view('discovery-writer-agent')")
        print("  4. skill_view('discovery-validator-agent')")
        print("  5. skill_view('discovery-publisher-agent')")
        print("")
        print("Each skill contains the full instructions for that stage.")
        print("")
        print(f"Topic data:")
        print(f"  Title: {topic.get('title')}")
        print(f"  Description: {topic.get('description')}")
        print(f"  Domains: {topic.get('domains', [])}")
        print(f"  Created: {topic.get('created_at')}")
        print(f"  Retries: {topic.get('retry_count', 0)}")

        # Set to in_progress
        set_status(data, topic_id, STATUS_IN_PROGRESS,
                   started_at=datetime.now(timezone.utc).isoformat())
        save_queue(data)

        print(f"\nStatus updated to: {STATUS_IN_PROGRESS}")
        print(f"An agent session should now load the skills and execute them.")

    finally:
        release_lock()

    return 0


if __name__ == "__main__":
    sys.exit(main())
