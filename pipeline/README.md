# Discovery Pipeline

Autonomous agent pipeline for cross-domain discovery.

## Structure

- `poller.py` — Reads the queue, processes pending topics, updates status
- `(coming) query_classifier.py` — Classifies new topics → discovery strategy
- `(coming) discovery_agent.py` — Serendipity + causal + gap detection agents
- `(coming) writer_agent.py` — Synthesizes findings into bridge publications
- `(coming) validator_agent.py` — Quality gate before publication

## Queue Flow

1. Researcher submits topic via web app → API → queue.json (status: pending)
2. Cron polls every 15min → poller.py picks up pending topics
3. Discovery agents run → bridge publication drafted → validated
4. On success → publication added to vault + web app, status: published
5. On failure → status: failed, logged for review

## Running

```bash
# Poll once (cron mode)
python3 poller.py --once

# Poll all pending (manual batch)
python3 poller.py
```
