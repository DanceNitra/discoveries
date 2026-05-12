---
pattern_id: PL-7ECDE9A0
name: Stigmergic Coordination
also_known_as: "Environment-Mediated Coordination"
layer: coordination
confidence: 0.8
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - coordination
  - coordination
---

# Stigmergic Coordination

## Also Known As
Environment-Mediated Coordination

## Problem
Centralized coordination creates a single point of failure and limits scalability. Agents need to coordinate without a central orchestrator or direct communication channels.

## Context
Large-scale multi-agent systems, swarm robotics, any system where agents need to self-organize without central control.

## Forces
Direct communication scales poorly (O(n^2)). Central orchestrators are single points of failure. Agents need to coordinate but may not trust each other or share a common language beyond the environment.

## Solution
Agents coordinate indirectly by modifying and sensing a shared environment. Agent A modifies the environment; Agent B observes the modification and adapts. No direct agent-to-agent communication is required.

## Resulting Context
Extremely resilient and scalable. Coordination is emergent and can produce unexpected global patterns. Debugging is harder because coordination traces are distributed across environment state.

## Examples
- [[04 Resources/Concepts/Swarm Intelligence.md]] — Swarm Intelligence
- [[04 Resources/Concepts/Stigmergy.md]] — Stigmergy
- [[04 Resources/Concepts/Emergence.md]] — Emergence



## Related Patterns
- **alternative** → Protocol-Mediated Discovery: Both enable coordination; stigmergy is implicit, protocol is explicit


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
