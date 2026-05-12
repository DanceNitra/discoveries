---
pattern_id: PL-CEE9187E
name: Crisis Circuit Breaker
also_known_as: "Fail-Spiral Detection, Governance Lockdown"
layer: meta
confidence: 0.85
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - meta
  - meta
---

# Crisis Circuit Breaker

## Also Known As
Fail-Spiral Detection, Governance Lockdown

## Problem
Autonomous systems can enter failure cascades where one error triggers more errors. Without detection and containment, the system spirals into unrecoverable states.

## Context
Any autonomous system with multiple interdependent components: agent swarms, pipeline orchestrators, self-modifying code, multi-phase knowledge workflows.

## Forces
Every system fails eventually. Fast detection requires monitoring overhead. Too-sensitive breakers cause false alarms; too-lenient breakers miss cascades. Recovery must be automatic for common failures and human-escalated for novel ones.

## Solution
Implement circuit breakers that track specific failure types (CPU spikes, API failures, write floods, orphan accumulation, general fail spirals). When a breaker trips, log a crisis event, raise all trust boundaries (more conservative), block non-read actions, and auto-resolve after a configurable cooldown. Severity levels: 1 (warning, single breaker), 2 (multiple breakers), 3 (fail spiral, human notification required).

## Resulting Context
Failure cascades are contained before they damage the system. False alarms are acceptable — they degrade performance temporarily but prevent permanent damage. Some crises require human intervention, creating latency in recovery.

## Examples
- [[06 System/Scripts/adaptive_crisis_protocol.py]] — Adaptive_Crisis_Protocol
- [[06 System/Scripts/immune_system.py]] — Immune_System
- [[06 System/Scripts/phase14_fail_spiral_detector.py]] — Phase14_Fail_Spiral_Detector



## Related Patterns
- **refines** → Homeostatic Regulation: Circuit breakers implement homeostatic regulation for system-level failures


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
