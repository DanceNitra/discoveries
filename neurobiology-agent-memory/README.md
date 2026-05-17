# Neurobiology of Agent Memory — 5-Tier Memory Architecture

## Overview

---

title: Neurobiology of Agent Memory — 5-Tier Hierarchy
type: publication
format: artifact
source_type: discovery
source_id: DISC-AGENTMEM1
novelty: 0.92
value_alignment: 0.96
status: draft
created: 2026-05-15
tags:
  - memory-systems
  - neurobiology
  - agent-architecture
  - cls-theory
  - phase-15

---

## Origin

Synthesis of complementary learning systems (CLS) theory, mammalian memory neuroscience, and agent memory architecture. Maps the 5-tier agent memory hierarchy (working → episodic → semantic → procedural → meta-memory) onto neurobiological substrates (PFC, hippocampus, neocortex, basal ganglia, prefrontal metacognition).

## Core Thesis

Agent memory systems benefit from biologically-inspired constraints:

1. **Dual-store separation** — Fast, temporary episodic buffers (hippocampus) and slow, permanent semantic stores (neocortex) with complementary learning rates prevent catastrophic forgetting.
2. **Consolidation via replay** — Offline replay of episodic patterns into semantic memory mirrors hippocampal sharp-wave ripples during sleep.
3. **Strategic forgetting** — TTL-based expiration and salience-pruning prevent memory saturation, analogous to synaptic pruning and the binding problem.
4. **Stress cascade** — Prioritized memory encoding under simulated stress (cortisol analog) shifts the system toward survival-salient retention.

## Architecture

```
neurobiology-agent-memory/
+-- README.md
+-- src/neurobiology_agent_memory/
|   +-- __init__.py
|   +-- main.py
+-- docs/README.md
+-- tests/test_main.py
+-- requirements.txt
```

## Getting Started

```bash
cd neurobiology-agent-memory
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```
