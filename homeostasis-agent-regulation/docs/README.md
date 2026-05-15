# Homeostasis Agent Regulation — Documentation

## Publication Metadata

---
title: Homeostasis as Agent Self-Regulation — The Homeostatic Agent
type: publication
format: module
source_type: discovery
source_id: DISC-HOMEOSTASIS-AGENT
novelty: 0.92
value_alignment: 0.97
status: draft
created: 2026-05-15
tags:
  - agent-architecture
  - homeostasis
  - self-regulation
  - control-theory
  - phase-15
---

## Key Concepts

### The Four-Component Homeostatic Loop

Analogous to biological homeostasis (Cannon, 1929):

| Component  | Function                                      | Biological Analog               |
|------------|-----------------------------------------------|---------------------------------|
| Sensor     | Measures current state metrics                | Thermoreceptors, baroreceptors  |
| Comparator | Computes error = set_point - sensed_value     | Hypothalamic integrating center |
| Effector   | Applies self-modification to reduce error     | Sweat glands, shivering muscles |
| Feedback   | Observes post-action state to close the loop  | Afferent nerve signals          |

### Allostatic Load (Set Point Drift)

When error is chronic and sustained beyond tolerance, the set point
drifts toward the error — the system "accommodates" the pathology.
This is allostatic load (Sterling & Eyer, 1988). In agents, this
manifests as degraded performance over time, requiring reset or
intervention.

### Positive Feedback Escape

When the effector amplifies error instead of dampening it, the loop
enters an unstable positive-feedback regime. The agent detects this
when correction and error share the same sign. Bounded effectors
(pre-configured min/max ranges) prevent catastrophic runaway.

### Nested Timescales

Three concurrent homeostatic loops match different biological rhythms:

| Timescale       | Frequency     | Biological Analog          | Agent Function                     |
|-----------------|---------------|----------------------------|------------------------------------|
| Per-turn        | Every step    | Spinal/reflex arcs         | Immediate sensorimotor regulation  |
| Per-session     | Session end   | Circadian / hormonal       | Behavioral pattern regulation      |
| Cross-session   | Across runs   | Epigenetic / developmental | Meta-learning, architecture tuning |

## API Reference

### `HomeostaticLoop(config, sensor_fn, effector_fn, feedback_fn)`

A single four-component negative-feedback loop.

- `step() -> LoopState` — execute one iteration
- `reset()` — restore initial set points and clear state
- `set_points` — current (possibly drifted) set points

### `HomeostaticAgent(name)`

An agent governed by nested homeostatic loops at three timescales.

- `add_loop(name, loop, timescale)` — register a loop
- `step() -> Dict[str, LoopState]` — run per-turn loops
- `end_session() -> Dict[str, LoopState]` — run per-session loops
- `cross_session_update() -> Dict[str, LoopState]` — run cross-session loops
- `get_allostatic_load_report()` — inspect chronic error accumulation
- `has_positive_feedback_escape()` — check for unstable loops
- `get_set_points()` — view current (drifted) targets
- `reset()` — full reset

### `create_default_agent(name) -> HomeostaticAgent`

Factory that creates an agent with one loop per timescale using
sensible default parameters for demonstration and testing.

## Homeostatic Skill Lifecycle

1. **Onboarding** — agent registers a new loop via `add_loop()`
2. **Regulation** — loops execute at their designated timescale
3. **Load accumulation** — chronic error causes set point drift
4. **Escape detection** — positive feedback triggers intervention
5. **Reset/Recalibration** — `reset()` restores homeostasis
