---
pattern_id: PL-4BEEFD06
name: Checkpoint-and-Resume
also_known_as: "Fail-Spiral Recovery, Session Persistence"
layer: meta
confidence: 0.75
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - meta
  - meta
---

# Checkpoint-and-Resume

## Also Known As
Fail-Spiral Recovery, Session Persistence

## Problem
Long-running autonomous processes are vulnerable to crashes and corruption. Without recovery, hours of work are lost.

## Context
Any system executing multi-step processes spanning minutes or hours: batch processing, multi-agent orchestration, creative cycles.

## Forces
Checkpoints add overhead. Too-frequent checkpoints waste resources. Too-infrequent checkpoints lose work.

## Solution
Periodically persist minimal state: phase identifier, step number, intermediate results as JSON, checksum of critical files. On restart, verify state integrity, then resume from the last complete checkpoint.

## Resulting Context
Resilience to crash failures. Recovery time proportional to checkpoint granularity. Schema must be versioned.

## Examples
- [[90 Meta/SDEAS Phase 14 -- Resilience Engine.md]] — Sdeas Phase 14    Resilience Engine
- [[06 System/Scripts/phase14_checkpoint_manager.py]] — Phase14_Checkpoint_Manager



## Related Patterns
- **composes_into** → ReAct Loop: Checkpoints allow long ReAct chains to survive crashes


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
