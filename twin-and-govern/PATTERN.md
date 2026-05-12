---
pattern_id: PL-803B841C
name: Twin-and-Govern
also_known_as: "Cognitive Twin with Governance Gate"
layer: meta
confidence: 0.8
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - meta
  - meta
---

# Twin-and-Govern

## Also Known As
Cognitive Twin with Governance Gate

## Problem
An autonomous system must act on behalf of a human, but unchecked autonomy can produce harmful or misaligned outputs. The system needs a model of the human's preferences and a gate that decides when to act vs. when to ask.

## Context
Any system that makes decisions affecting human interests: content generation, code modification, financial decisions, email replies.

## Forces
Full autonomy is fast but risky. Full human-in-the-loop is safe but slow. The system needs to build trust over time and escalate when uncertainty is high.

## Solution
Maintain a twin — a model of the human's reasoning patterns, values, and preferences (Phase 10). Before acting, check against value alignment, trust boundaries, and crisis state (Phase 11). Green zone = act autonomously. Yellow zone = propose and wait. Red zone = blocked.

## Resulting Context
Trust builds gradually as the twin improves. The governance gate prevents catastrophic errors but can cause delays when the human is unavailable. Requires ongoing calibration.

## Examples
- [[90 Meta/SDEAS Phase 10 — Cognitive Replication.md]] — Sdeas Phase 10 — Cognitive Replication
- [[90 Meta/SDEAS Phase 11 — Adaptive Governance.md]] — Sdeas Phase 11 — Adaptive Governance



## Related Patterns
- **composes_into** → Distill-and-Publish: Governance gate ensures publications are value-aligned


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
