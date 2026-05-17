"""Pipeline poller — reads the discovery queue and triggers pipeline runs.

Designed to run on a cron schedule (every 15-30 minutes).
Picks up pending topics, spawns the discovery pipeline for each,
updates status to in_progress, and pushes results back.

Run: python3 pipeline_poller.py [--once]

In cron mode (--once), processes one batch and exits.
The scheduler/cron handles frequency.
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


def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return {"topics": [], "runs": []}
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(data):
    os.makedirs(QUEUE_DIR, exist_ok=True)
    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)
    # Publish dashboard
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
                cwd=DISCOVERIES_REPO,
                capture_output=True,
            )
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    f"queue: update dashboard — {len(dashboard['topics'])} topics",
                    "--allow-empty",
                ],
                cwd=DISCOVERIES_REPO,
                capture_output=True,
            )
            subprocess.run(["git", "push"], cwd=DISCOVERIES_REPO, capture_output=True)
        except Exception as e:
            print(f"[warn] git push failed: {e}")


def acquire_lock():
    """Prevent concurrent pipeline runs."""
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE) as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)  # Check if process exists
            print(f"[warn] Pipeline already running (PID {pid})")
            return False
        except (OSError, ValueError):
            pass  # Stale PID, reclaim
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True


def release_lock():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def process_topic(topic):
    """Trigger the Hermes discovery pipeline for a single topic.

    For Phase A, this is a stub that sets the topic to in_progress.
    Phase B will implement the actual discovery agents.
    """
    topic_id = topic["id"]
    title = topic["title"]
    description = topic.get("description", "")

    print(f"Processing topic: {title} (ID: {topic_id})")

    # Update status to in_progress
    topic["status"] = STATUS_IN_PROGRESS
    topic["started_at"] = datetime.now(timezone.utc).isoformat()
    save_queue(load_queue())  # Re-read to avoid race, then update

    try:
        # TODO Phase B: spawn discovery agents here
        # For now, simulate a successful pipeline run
        print(f"  Discovery agents searching for connections...")
        time.sleep(1)  # Simulate work

        # On success
        topic["status"] = STATUS_PUBLISHED
        topic["completed_at"] = datetime.now(timezone.utc).isoformat()
        topic["publication_url"] = None  # Will be set when actually published
        print(f"  ✓ Published: {title}")

    except Exception as e:
        topic["status"] = STATUS_FAILED
        topic["failed_at"] = datetime.now(timezone.utc).isoformat()
        topic["error"] = str(e)
        print(f"  ✗ Failed: {e}")

    return topic


def main():
    once = "--once" in sys.argv

    if not acquire_lock():
        return 1

    try:
        data = load_queue()
        pending = [t for t in data.get("topics", []) if t.get("status") == STATUS_PENDING]

        if not pending:
            print("No pending topics.")
            return 0

        print(f"Found {len(pending)} pending topic(s)")

        for topic in pending:
            process_topic(topic)
            save_queue(load_queue())  # Persist after each topic
            if once:
                break  # Only process one topic per cron tick

    finally:
        release_lock()

    return 0


if __name__ == "__main__":
    sys.exit(main())
