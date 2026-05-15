# Neurobiology of Agent Memory — Theory

---

title: Neurobiology of Agent Memory — 5-Tier Hierarchy
type: theory
tags:
  - complementary-learning-systems
  - memory
  - hippocampus
  - neocortex
  - consolidation

---

## The 5-Tier Agent Memory Hierarchy

| Tier | Name | Neural Substrate | Agent Analog | Timescale |
|------|------|------------------|-------------|-----------|
| 1 | Working Memory | Prefrontal Cortex (PFC) | Scratchpad dict | seconds |
| 2 | Episodic Buffer | Hippocampus (DG + CA3) | `EpisodicBuffer` | minutes–hours |
| 3 | Semantic Store | Neocortex (distributed) | `SemanticStore` | days–years |
| 4 | Procedural | Basal Ganglia (striatum) | Action-chunk registry | persistent |
| 5 | Meta-Memory | PFC metacognition | Introspective stats | ongoing |

## Complementary Learning Systems (CLS)

**McClelland, McNaughton & O'Reilly (1995)** proposed that the brain solves the stability-plasticity dilemma with two complementary systems:

- **Hippocampus** — fast learning rate, pattern-separated representations, temporary storage. Avoids catastrophic interference because patterns are sparse and non-overlapping.
- **Neocortex** — slow learning rate, overlapping distributed representations, permanent storage. Gradual integration prevents disruption of existing knowledge.

## The Binding Problem

How does the brain bind features (color, shape, location, sound) into a unified episodic memory? In our implementation, content-addressable hashing produces a deterministic episode id from the feature set — a simplified binding mechanism.

## Strategic Forgetting

TTL-based expiration models the metabolic cost of maintaining synaptic connections. Salience-based pruning (weakest memories removed first) mirrors activity-dependent apoptosis and the fact that low-salience memories are preferentially forgotten.

## Sleep Consolidation

Hippocampal sharp-wave ripples during NREM (non-rapid eye movement) sleep replay recent experiences into neocortex. Our `MemoryConsolidator` runs a replay cycle that transfers episodic patterns to the semantic store with salience-weighted strength increments.

## Stress Cascade

Under stress, cortisol biases encoding and consolidation toward survival-salient events. We model this by modulating the replay sorting: episodes with high salience are replayed first and more frequently when `stress_level > 0`.

## Usage

See the main module docstring and tests for example usage. Quick start:

```python
from neurobiology_agent_memory import MemoryAgent

agent = MemoryAgent(episodic_capacity=100, replay_rate=0.3)
agent.observe({"location": "library", "book": "CLS theory"}, salience=0.8)
results = agent.run_cycle()
print(agent.summary())
```
