---
pattern_id: PL-F7F28128
name: Bounded Context for Agents
also_known_as: "Agent Context, Capability Boundary"
layer: structure
confidence: 0.8
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - structure
  - structure
---

# Bounded Context for Agents

## Also Known As
Agent Context, Capability Boundary

## Problem
In multi-agent systems, agents leak state across boundaries, producing unpredictable behavior and making the system hard to reason about. Without explicit boundaries, agent capabilities collide.

## Context
Systems with multiple agents that share access to tools, memory, or state. Particularly acute in systems where agents can spawn other agents.

## Forces
Agents need access to shared resources but must not corrupt each other's state. Boundaries that are too strict prevent useful collaboration; boundaries too loose produce chaos.

## Solution
Define each agent's capability as a bounded context with explicit upstream/downstream contracts. All state mutations route through an aggregate root. Cross-context communication happens through events, not direct state access.

## Resulting Context
Agents become independently testable and swappable. Collaboration requires explicit event contracts, which increases boilerplate but prevents cascade failures.

## Examples
- [[04 Resources/Concepts/Domain-Driven Design.md]] — Domain Driven Design
- [[04 Resources/Concepts/Software Architecture for Agentic Systems.md]] — Software Architecture For Agentic Systems
- [[04 Resources/Concepts/Design Patterns.md]] — Design Patterns



## Related Patterns
- **prerequisite** → Stigmergic Coordination: Agents need clear boundaries before they can coordinate via environment


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
